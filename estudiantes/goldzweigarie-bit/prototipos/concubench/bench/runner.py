"""Ciclo de vida de un intento y ejecución concurrente con presupuesto.

Por intento (tarea × agente × repetición):

  1. agent    contenedor A con una copia de workspace/ montada en /workspace.
              El adaptador actúa con docker exec. Luego A se destruye.
  2. prepare  contenedor P (sin /workspace): genera /data y /expected con una
              semilla nueva. La solución nunca ve /expected.
  3. grade    contenedor G NUEVO: /workspace (solo lectura), /data (solo
              lectura), solve.sh y la sonda. Aquí se miden memoria, CPU, OOM.
  4. check    contenedor C (sin /workspace): compara /results con /expected.

Cada fase reserva su memoria/CPU del presupuesto y la libera al terminar.
"""
from __future__ import annotations

import asyncio
import json
import os
import secrets
import shutil
import time
from dataclasses import dataclass
from pathlib import Path

from . import docker
from .agents import Agent, AgentContext
from .budget import Budget
from .task import Limits, Task

PROBE = Path(__file__).with_name("probe.py")


@dataclass
class Job:
    task: Task
    agent: Agent
    attempt: int

    @property
    def cost(self) -> int:  # para ordenar: más grande primero (LPT)
        return max(self.task.grading.memory_mb, self.task.prepare.memory_mb)


def host_resources() -> tuple[int, float]:
    mem_mb = 4096
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                mem_mb = int(line.split()[1]) // 1024
    except OSError:
        pass
    return mem_mb, float(os.cpu_count() or 2)


def default_user() -> str:
    uid = os.getuid() if hasattr(os, "getuid") else 1000
    gid = os.getgid() if hasattr(os, "getgid") else 1000
    return "65534:65534" if uid == 0 else f"{uid}:{gid}"


def _open_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    os.chmod(p, 0o777)  # el usuario del contenedor puede no ser el del host
    return p


def _copy_workspace(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst)
    for root, dirs, files in os.walk(dst):
        os.chmod(root, 0o777)
        for f in files:
            fp = os.path.join(root, f)
            os.chmod(fp, os.stat(fp).st_mode | 0o666)


def _rmtree(p: Path) -> None:
    shutil.rmtree(p, ignore_errors=True)


class Runner:
    def __init__(
        self,
        repo: Path,
        image: str,
        out_dir: Path,
        budget: Budget,
        *,
        scale: float = 1.0,
        seed: int | None = None,
        user: str | None = None,
        keep_data: bool = False,
        verbose: bool = True,
    ):
        self.repo, self.image, self.out_dir, self.budget = repo, image, out_dir, budget
        self.scale, self.seed, self.user = scale, seed, user or default_user()
        self.keep_data, self.verbose = keep_data, verbose
        self.run_id = out_dir.name
        self._images: dict[str, str] = {}
        self._image_lock = asyncio.Lock()
        self.results_path = out_dir / "results.jsonl"
        self._write_lock = asyncio.Lock()

    # ------------------------------------------------------------------ util
    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg, flush=True)

    def _clamp(self, lim: Limits) -> tuple[Limits, bool]:
        if lim.cpus > self.budget.cpu_total:
            from dataclasses import replace
            return replace(lim, cpus=self.budget.cpu_total), True
        return lim, False

    async def _image_for(self, task: Task) -> str:
        if not task.dockerfile:
            return self.image
        async with self._image_lock:
            if task.id not in self._images:
                tag = f"concubench-task-{task.id}:latest"
                await docker.build(task.path, tag, self.image, self.out_dir / f"build-{task.id}.log")
                self._images[task.id] = tag
            return self._images[task.id]

    async def _phase(self, name: str, lim: Limits, mounts: list[str], env: dict, cmd: list[str],
                     image: str, log: Path, extra_timeout: int = 30) -> tuple[int, bool]:
        argv = [docker.DOCKER, "run", "--rm", "--name", name, *docker.limit_flags(lim, self.user)]
        for m in mounts:
            argv += ["-v", m]
        for k, v in env.items():
            argv += ["-e", f"{k}={v}"]
        argv += [image, *cmd]
        async with self.budget.hold(lim.memory_mb, lim.cpus):
            rc, _, to = await docker.run(argv, timeout=lim.timeout_s + extra_timeout, log=log)
            if to:
                await docker.rm_force(name)
        return rc, to

    # -------------------------------------------------------------- attempt
    async def run_job(self, job: Job) -> dict:
        task, agent = job.task, job.agent
        seed = (self.seed + job.attempt) if self.seed is not None else secrets.randbits(31)
        adir = self.out_dir / task.id / f"{agent.name}-{job.attempt}"
        if adir.exists():
            _rmtree(adir)
        adir.mkdir(parents=True)
        ws = adir / "workspace"
        _copy_workspace(task.path / "workspace", ws)
        artifacts = _open_dir(adir / "agent")
        data, expected, results = (_open_dir(adir / d) for d in ("data", "expected", "results"))
        tests = task.path / "tests"
        image = await self._image_for(task)
        base = f"cb-{self.run_id}-{task.id}-{agent.name}-{job.attempt}".replace("_", "-").lower()
        rec = {
            "run_id": self.run_id, "task": task.id, "category": task.category, "agent": agent.name,
            "attempt": job.attempt, "seed": seed, "scale": self.scale,
        }
        t_start = time.monotonic()

        # 1) agente ------------------------------------------------------
        alim, clamped_a = self._clamp(task.agent)
        cname = f"{base}-a"
        argv = [docker.DOCKER, "run", "-d", "--name", cname, *docker.limit_flags(alim, self.user),
                "-v", f"{ws}:/workspace", "-w", "/workspace", image, "sleep", "infinity"]
        async with self.budget.hold(alim.memory_mb, alim.cpus):
            rc, tail, _ = await docker.run(argv, timeout=120)
            if rc != 0:
                rec.update(passed=False, exit_reason="infra", error=f"no arrancó el contenedor A: {tail[-500:]}")
                return await self._record(rec)
            try:
                res = await agent.act(AgentContext(task, cname, task.prompt_path, artifacts,
                                                   adir / "agent.log", alim.timeout_s))
            finally:
                await docker.rm_force(cname)
        rec.update(agent_rc=res.rc, agent_timed_out=res.timed_out, agent_wall_s=round(res.wall_s, 2), **res.meta)

        # 2) prepare -----------------------------------------------------
        plim, _ = self._clamp(task.prepare)
        rc, to = await self._phase(
            f"{base}-p", plim,
            [f"{tests}:/bench/tests:ro", f"{data}:/data", f"{expected}:/expected"],
            {"BENCH_SEED": seed, "BENCH_SCALE": self.scale, "BENCH_DATA": "/data", "BENCH_EXPECTED": "/expected"},
            ["python3", "/bench/tests/prepare.py"], image, adir / "prepare.log",
        )
        if rc != 0 or to:
            rec.update(passed=False, exit_reason="infra", error=f"prepare falló (rc={rc}, timeout={to})")
            return await self._record(rec, data)

        # 3) grade (medido) ----------------------------------------------
        glim, clamped_g = self._clamp(task.grading)
        rc, to = await self._phase(
            f"{base}-g", glim,
            [f"{ws}:/workspace:ro", f"{data}:/data:ro", f"{results}:/results",
             f"{tests / 'solve.sh'}:/bench/solve.sh:ro", f"{PROBE}:/bench/probe.py:ro"],
            {"BENCH_TIMEOUT": glim.timeout_s, "BENCH_DATA": "/data", "BENCH_RESULTS": "/results"},
            ["python3", "/bench/probe.py", "/bench/solve.sh"], image, adir / "grade.log",
        )
        metrics = {}
        mfile = results / "metrics.json"
        if mfile.is_file():
            metrics = json.loads(mfile.read_text())
        if not metrics:
            # La sonda misma murió (p. ej. OOM que se llevó todo).
            metrics = {"exit_code": rc, "timed_out": to, "oom_kills": 1 if rc == 137 else 0}

        # 4) check --------------------------------------------------------
        clim, _ = self._clamp(task.check)
        crc, cto = await self._phase(
            f"{base}-c", clim,
            [f"{tests / 'check.py'}:/bench/check.py:ro", f"{expected}:/expected:ro", f"{results}:/results"],
            {"BENCH_EXPECTED": "/expected", "BENCH_RESULTS": "/results"},
            ["python3", "/bench/check.py"], image, adir / "check.log",
        )
        detail = {}
        dfile = results / "detail.json"
        if dfile.is_file():
            try:
                detail = json.loads(dfile.read_text())
            except ValueError:
                pass

        oom = metrics.get("oom_kills", 0) > 0
        if oom:
            reason = "oom"
        elif metrics.get("timed_out"):
            reason = "timeout"
        elif metrics.get("exit_code") not in (0, None):
            reason = "solve_error"
        elif crc != 0 or cto:
            reason = "wrong"
        else:
            reason = "ok"
        rec.update(
            passed=reason == "ok",
            exit_reason=reason,
            grade_wall_s=metrics.get("wall_s"),
            cpu_s=metrics.get("cpu_s"),
            parallelism=metrics.get("parallelism"),
            peak_mb=metrics.get("peak_unreclaimable_mb"),
            peak_total_mb=metrics.get("peak_total_mb"),
            limit_mb=glim.memory_mb,
            cpus=glim.cpus,
            cpus_clamped=clamped_a or clamped_g,
            oom_kills=metrics.get("oom_kills"),
            cgroup=metrics.get("cgroup_version"),
            check=detail.get("message"),
            total_wall_s=round(time.monotonic() - t_start, 2),
        )
        return await self._record(rec, data)

    async def _record(self, rec: dict, data: Path | None = None) -> dict:
        if data is not None and not self.keep_data:
            _rmtree(data)  # los datos de prueba pueden pesar cientos de MB
        async with self._write_lock:
            with open(self.results_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        mark = "✔" if rec.get("passed") else "✘"
        extra = f" pico={rec.get('peak_mb')}MB/{rec.get('limit_mb')}MB" if rec.get("peak_mb") is not None else ""
        self._log(f"  {mark} {rec['task']:<22} {rec['agent']:<10} #{rec['attempt']} {rec.get('exit_reason')}{extra}")
        return rec

    async def run_all(self, jobs: list[Job]) -> list[dict]:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        jobs = sorted(jobs, key=lambda j: -j.cost)  # LPT: los más pesados primero
        for j in jobs:
            for lim in (j.task.prepare, j.task.grading, j.task.check):
                if lim.memory_mb > self.budget.mem_total:
                    raise SystemExit(f"{j.task.id}: pide {lim.memory_mb} MB y el presupuesto es {self.budget.mem_total} MB")
        t0 = time.monotonic()
        out = await asyncio.gather(*(self.run_job(j) for j in jobs))
        stats = {**self.budget.stats(), "jobs": len(jobs), "makespan_s": round(time.monotonic() - t0, 2)}
        (self.out_dir / "run.json").write_text(json.dumps(stats, indent=2))
        self._log(f"\nmakespan {stats['makespan_s']} s · pico reservado {stats['peak_mem_reserved_mb']} MB "
                  f"de {stats['mem_budget_mb']} · {stats['max_concurrent_phases']} fases simultáneas máx.")
        return out
