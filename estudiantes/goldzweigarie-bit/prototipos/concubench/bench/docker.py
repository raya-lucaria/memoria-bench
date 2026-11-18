"""Envoltura mínima y asíncrona del CLI de docker (sin SDK, sin dependencias)."""
from __future__ import annotations

import asyncio
import os
import signal
from pathlib import Path

from .task import Limits

DOCKER = os.environ.get("BENCH_DOCKER", "docker")


async def run(
    argv: list[str],
    *,
    timeout: float | None = None,
    stdin: Path | None = None,
    log: Path | None = None,
    env: dict | None = None,
    new_session: bool = False,
) -> tuple[int, str, bool]:
    """Corre un proceso. Devuelve (código, cola_de_salida, se_agotó_el_tiempo).

    Con `log`, stdout+stderr van a disco (nunca se acumulan en RAM).
    """
    out_f = open(log, "ab") if log else None
    in_f = open(stdin, "rb") if stdin else None
    try:
        proc = await asyncio.create_subprocess_exec(
            *argv,
            stdin=in_f or asyncio.subprocess.DEVNULL,
            stdout=out_f or asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=env,
            start_new_session=new_session,
        )
        timed_out = False
        try:
            data, _ = await asyncio.wait_for(proc.communicate(), timeout)
        except asyncio.TimeoutError:
            timed_out = True
            _kill(proc, new_session)
            data, _ = await proc.communicate()
    finally:
        if out_f:
            out_f.close()
        if in_f:
            in_f.close()
    if log:
        tail = _tail(log)
    else:
        tail = (data or b"").decode(errors="replace")[-4000:]
    return proc.returncode, tail, timed_out


def _kill(proc, group: bool) -> None:
    try:
        if group:
            os.killpg(proc.pid, signal.SIGKILL)
        else:
            proc.kill()
    except ProcessLookupError:
        pass


def _tail(path: Path, n: int = 4000) -> str:
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - n))
            return f.read().decode(errors="replace")
    except OSError:
        return ""


def limit_flags(lim: Limits, user: str) -> list[str]:
    """Banderas de aislamiento comunes a todas las fases."""
    return [
        "--init",
        "--network", lim.network,
        "--cpus", f"{lim.cpus:g}",
        "--memory", f"{lim.memory_mb}m",
        "--memory-swap", f"{lim.memory_mb}m",   # = memory: sin swap, OOM real
        "--shm-size", f"{lim.memory_mb}m",      # /dev/shm cuenta contra el cgroup de todos modos
        "--pids-limit", str(lim.pids),
        "--user", user,
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--read-only",
        "--tmpfs", f"/tmp:rw,size={lim.tmpfs_mb}m,mode=1777",
        "-e", "HOME=/tmp",
        "-e", "PYTHONDONTWRITEBYTECODE=1",
    ]


async def rm_force(name: str) -> None:
    await run([DOCKER, "rm", "-f", name], timeout=60)


async def image_exists(tag: str) -> bool:
    rc, _, _ = await run([DOCKER, "image", "inspect", tag], timeout=60)
    return rc == 0


async def build(context: Path, tag: str, base: str, log: Path) -> None:
    rc, tail, _ = await run(
        [DOCKER, "build", "-t", tag, "--build-arg", f"BASE={base}", str(context)],
        timeout=1800,
        log=log,
    )
    if rc != 0:
        raise RuntimeError(f"docker build {tag} falló:\n{tail}")
