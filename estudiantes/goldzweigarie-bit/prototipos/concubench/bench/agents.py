"""Agentes. Tres de referencia (sin modelo) y adaptadores externos.

Contrato de un adaptador externo (adapters/<nombre>/run.sh):

    run.sh <container> <prompt_file>

- Actúa SOLO a través de `docker exec <container> ...` (cwd /workspace).
- Variables: BENCH_CONTAINER, BENCH_PROMPT, BENCH_TIMEOUT, BENCH_WORKDIR,
  BENCH_ARTIFACTS (directorio del host donde puede dejar trajectory.json y
  meta.json con {"model": ..., "steps": ..., "tokens_in": ..., "tokens_out": ...}).
- Hereda el entorno, así que OPENAI_BASE_URL / OPENAI_MODEL apuntan a Ollama,
  llama.cpp o lo que sea. El benchmark nunca lee ni necesita llaves.
- El código de salida no califica; solo el estado final de /workspace.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from . import docker
from .task import Task


@dataclass
class AgentContext:
    task: Task
    container: str
    prompt_path: Path
    artifacts: Path
    log: Path
    timeout_s: int


@dataclass
class AgentResult:
    rc: int
    timed_out: bool
    wall_s: float
    meta: dict = field(default_factory=dict)


class Agent:
    name = "agent"
    reference = False

    def applies_to(self, task: Task) -> bool:
        return True

    async def act(self, ctx: AgentContext) -> AgentResult:  # pragma: no cover
        raise NotImplementedError


class NullAgent(Agent):
    """No hace nada. Si una tarea pasa con esto, la tarea está rota."""
    name = "null"
    reference = True

    async def act(self, ctx):
        return AgentResult(0, False, 0.0, {"model": "none"})


class ScriptAgent(Agent):
    """Corre <task>/<subdir>/solve.sh dentro del contenedor vía docker exec.

    Usa exactamente el mismo canal que un agente real, así que valida también
    la plomería del contenedor.
    """
    reference = True

    def __init__(self, name: str, subdir: str):
        self.name, self.subdir = name, subdir

    def applies_to(self, task):
        return (task.path / self.subdir / "solve.sh").is_file()

    async def act(self, ctx):
        script = ctx.task.path / self.subdir / "solve.sh"
        t0 = time.monotonic()
        rc, _, to = await docker.run(
            [docker.DOCKER, "exec", "-i", "-w", "/workspace", ctx.container, "bash", "-s"],
            stdin=script, log=ctx.log, timeout=ctx.timeout_s,
        )
        return AgentResult(rc, to, time.monotonic() - t0, {"model": "none"})


class ExternalAdapter(Agent):
    def __init__(self, path: Path):
        self.path = path.resolve()
        self.name = self.path.name

    async def act(self, ctx):
        env = dict(os.environ)
        env.update(
            BENCH_CONTAINER=ctx.container,
            BENCH_PROMPT=str(ctx.prompt_path),
            BENCH_TIMEOUT=str(ctx.timeout_s),
            BENCH_WORKDIR="/workspace",
            BENCH_ARTIFACTS=str(ctx.artifacts),
            BENCH_TASK_ID=ctx.task.id,
        )
        t0 = time.monotonic()
        rc, _, to = await docker.run(
            ["bash", str(self.path / "run.sh"), ctx.container, str(ctx.prompt_path)],
            env=env, log=ctx.log, timeout=ctx.timeout_s, new_session=True,
        )
        meta = {}
        meta_file = ctx.artifacts / "meta.json"
        if meta_file.is_file():
            try:
                raw = json.loads(meta_file.read_text())
                meta = {k: raw[k] for k in ("model", "steps", "tokens_in", "tokens_out") if k in raw}
            except (ValueError, OSError):
                meta = {"meta_error": "meta.json inválido"}
        return AgentResult(rc, to, time.monotonic() - t0, meta)


def resolve(spec: str, repo: Path) -> Agent:
    if spec == "null":
        return NullAgent()
    if spec == "oracle":
        return ScriptAgent("oracle", "solution")
    if spec == "naive":
        return ScriptAgent("naive", "naive")
    for cand in (Path(spec), repo / "adapters" / spec):
        if (cand / "run.sh").is_file():
            return ExternalAdapter(cand)
    raise SystemExit(f"agente desconocido: {spec} (usa null|oracle|naive o adapters/<x> con run.sh)")
