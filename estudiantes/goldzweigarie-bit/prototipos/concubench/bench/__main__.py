"""CLI.

  python3 -m bench list
  python3 -m bench run --agent oracle [--tasks 'm0*'] [--attempts 3]
  python3 -m bench run --agent adapters/mi-harness --attempts 3
  python3 -m bench validate            # null=0 %, naive falla como se espera, oracle=100 %
  python3 -m bench summary runs/<id>/results.jsonl
"""
from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

from . import agents, docker
from .budget import Budget
from .runner import Job, Runner, host_resources
from .task import discover

REPO = Path(__file__).resolve().parent.parent


def _budget(args) -> Budget:
    mem, cpus = host_resources()
    mem_budget = args.mem_budget or int(mem * 0.75)  # 25 % para el SO y el daemon
    cpu_budget = args.cpu_budget or cpus
    return Budget(mem_budget, cpu_budget)


def _runner(args, budget) -> Runner:
    run_id = args.run_id or time.strftime("%Y%m%d-%H%M%S")
    return Runner(REPO, args.image, Path(args.out) / run_id, budget, scale=args.scale,
                  seed=args.seed, keep_data=args.keep_data)


async def _preflight(image: str) -> None:
    rc, tail, _ = await docker.run([docker.DOCKER, "info", "--format", "{{.ServerVersion}}"], timeout=30)
    if rc != 0:
        raise SystemExit(f"docker no responde: {tail.strip()}")
    if not await docker.image_exists(image):
        raise SystemExit(f"no existe la imagen {image}. Corre: make image")


def cmd_list(args):
    for t in discover(REPO / "tasks", args.tasks):
        print(f"{t.id:<22} {t.category:<13} d{t.difficulty}  grading={t.grading.memory_mb}MB/"
              f"{t.grading.cpus:g}cpu  naive={t.expect.naive}  {t.title}")


def cmd_run(args):
    tasks = discover(REPO / "tasks", args.tasks)
    agent = agents.resolve(args.agent, REPO)
    jobs = [Job(t, agent, a) for t in tasks if agent.applies_to(t) for a in range(1, args.attempts + 1)]
    if not jobs:
        raise SystemExit("no hay trabajos que correr")
    asyncio.run(_preflight(args.image))
    budget = _budget(args)
    runner = _runner(args, budget)
    print(f"{len(jobs)} intentos · presupuesto {budget.mem_total} MB / {budget.cpu_total:g} CPU → {runner.out_dir}")
    recs = asyncio.run(runner.run_all(jobs))
    print()
    print_summary(recs)


def cmd_validate(args):
    """Valida el benchmark, no a un agente. Corre en CI en cada PR."""
    tasks = discover(REPO / "tasks", args.tasks)
    null, oracle, naive = agents.resolve("null", REPO), agents.resolve("oracle", REPO), agents.resolve("naive", REPO)
    jobs = []
    for t in tasks:
        jobs.append(Job(t, null, 1))
        if t.expect.naive != "skip" and naive.applies_to(t):
            jobs.append(Job(t, naive, 1))
        reps = args.oracle_repeats or max(3, t.repeats)
        jobs += [Job(t, oracle, i) for i in range(1, reps + 1)]
    asyncio.run(_preflight(args.image))
    budget = _budget(args)
    runner = _runner(args, budget)
    print(f"validando {len(tasks)} tareas ({len(jobs)} intentos) → {runner.out_dir}")
    recs = asyncio.run(runner.run_all(jobs))

    by = defaultdict(list)
    for r in recs:
        by[(r["task"], r["agent"])].append(r)
    problems = []
    print("\ntarea                   null     naive        oracle      pico oracle / límite")
    for t in tasks:
        n = by[(t.id, "null")]
        nv = by.get((t.id, "naive"), [])
        o = by[(t.id, "oracle")]
        if any(r["passed"] for r in n):
            problems.append(f"{t.id}: el agente null PASA → la prueba no detecta que no se hizo nada")
        if nv:
            want = t.expect.naive
            got = nv[0]["exit_reason"]
            if nv[0]["passed"] or (want in {"oom", "timeout"} and got != want):
                problems.append(f"{t.id}: naive debía fallar por '{want}' y terminó en '{got}'")
        ok = sum(r["passed"] for r in o)
        if ok != len(o):
            reasons = sorted({r["exit_reason"] for r in o if not r["passed"]})
            problems.append(f"{t.id}: oracle pasó {ok}/{len(o)} ({', '.join(reasons)}) → tarea irresoluble o inestable")
        peaks = [r["peak_mb"] for r in o if r.get("peak_mb") is not None]
        peak = max(peaks) if peaks else None
        limit = t.grading.memory_mb
        if peak is not None and peak > t.expect.oracle_max_mem_frac * limit:
            problems.append(f"{t.id}: oracle usa {peak} MB > {t.expect.oracle_max_mem_frac:.0%} de {limit} MB → límite demasiado justo")
        nv_s = nv[0]["exit_reason"] if nv else "—"
        print(f"{t.id:<22} {n[0]['exit_reason']:<8} {nv_s:<12} {ok}/{len(o):<10} "
              f"{peak if peak is not None else '?'} / {limit} MB")
    if problems:
        print("\nPROBLEMAS:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("\nbenchmark válido ✔")


def print_summary(recs: list[dict]) -> None:
    by_agent = defaultdict(list)
    for r in recs:
        by_agent[r["agent"]].append(r)
    for agent, rs in sorted(by_agent.items()):
        per_task = defaultdict(list)
        for r in rs:
            per_task[r["task"]].append(r["passed"])
        pass1 = statistics.mean(r["passed"] for r in rs)
        passk = statistics.mean(all(v) for v in per_task.values())
        k = max(len(v) for v in per_task.values())
        walls = [r["grade_wall_s"] for r in rs if r.get("grade_wall_s") is not None]
        model = next((r.get("model") for r in rs if r.get("model")), "?")
        print(f"{agent} (modelo: {model})  pass@1={pass1:.0%}  pass^{k}={passk:.0%}  "
              f"wall mediano={statistics.median(walls) if walls else '?'} s")
        cats = defaultdict(list)
        for r in rs:
            cats[r["category"]].append(r["passed"])
        for c, v in sorted(cats.items()):
            print(f"    {c:<14} {sum(v)}/{len(v)}")
        reasons = defaultdict(int)
        for r in rs:
            if not r["passed"]:
                reasons[r["exit_reason"]] += 1
        if reasons:
            print("    fallas: " + ", ".join(f"{k}={v}" for k, v in sorted(reasons.items())))


def cmd_summary(args):
    recs = [json.loads(l) for l in Path(args.results).read_text().splitlines() if l.strip()]
    print_summary(recs)


def main(argv=None):
    p = argparse.ArgumentParser(prog="bench", description="concubench")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--tasks", nargs="*", help="patrones glob de ids, p. ej. 'm0*'")
        sp.add_argument("--image", default="concubench-base:latest")
        sp.add_argument("--out", default=str(REPO / "runs"))
        sp.add_argument("--run-id")
        sp.add_argument("--scale", type=float, default=1.0, help="solo para depurar; <1 rompe la discriminación de memoria")
        sp.add_argument("--seed", type=int, help="semilla fija (por defecto, aleatoria por intento)")
        sp.add_argument("--mem-budget", type=int, help="MB para todas las fases simultáneas (def: 75 %% de la RAM)")
        sp.add_argument("--cpu-budget", type=float, help="CPUs para todas las fases simultáneas (def: todas)")
        sp.add_argument("--keep-data", action="store_true")

    sp = sub.add_parser("list"); sp.add_argument("--tasks", nargs="*"); sp.set_defaults(fn=cmd_list)
    sp = sub.add_parser("run"); common(sp)
    sp.add_argument("--agent", required=True); sp.add_argument("--attempts", type=int, default=1)
    sp.set_defaults(fn=cmd_run)
    sp = sub.add_parser("validate"); common(sp)
    sp.add_argument("--oracle-repeats", type=int); sp.set_defaults(fn=cmd_validate)
    sp = sub.add_parser("summary"); sp.add_argument("results"); sp.set_defaults(fn=cmd_summary)
    args = p.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
