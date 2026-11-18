"""Sonda de calificación. Corre DENTRO del contenedor de calificación (G).

Uso: python3 /bench/probe.py /bench/solve.sh

- Ejecuta solve.sh con timeout duro (BENCH_TIMEOUT).
- Muestrea el cgroup cada 50 ms: memoria no reclamable = anon + shmem
  (tmpfs y /dev/shm cuentan; la page cache NO, porque el kernel la libera).
- Cuenta OOM kills del cgroup (memory.events en v2, memory.oom_control en v1).
- Mide CPU del cgroup para estimar paralelismo = cpu_s / wall_s.
- Al terminar mata cualquier proceso que la solución haya dejado vivo y escribe
  /results/metrics.json al final (la solución no puede sobrescribirlo).

Solo stdlib; funciona con cgroup v1 y v2.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

CG = Path("/sys/fs/cgroup")
RESULTS = Path(os.environ.get("BENCH_RESULTS", "/results"))


def _kv(path: Path) -> dict[str, int]:
    out = {}
    try:
        for line in path.read_text().splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[1].lstrip("-").isdigit():
                out[parts[0]] = int(parts[1])
    except OSError:
        pass
    return out


def _int(path: Path) -> int | None:
    try:
        return int(path.read_text().split()[0])
    except (OSError, ValueError, IndexError):
        return None


class Cgroup:
    def __init__(self):
        if (CG / "memory.stat").exists():
            self.version = 2
            self.mem = CG
        elif (CG / "memory" / "memory.stat").exists():
            self.version = 1
            self.mem = CG / "memory"
        else:
            self.version = 0
            self.mem = None

    def unreclaimable_bytes(self) -> int | None:
        if not self.mem:
            return None
        s = _kv(self.mem / "memory.stat")
        if self.version == 2:
            return s.get("anon", 0) + s.get("shmem", 0)
        anon = s.get("total_rss", s.get("rss", 0))
        return anon + s.get("total_shmem", s.get("shmem", 0))

    def total_peak_bytes(self) -> int | None:
        if not self.mem:
            return None
        if self.version == 2:
            return _int(self.mem / "memory.peak")
        return _int(self.mem / "memory.max_usage_in_bytes")

    def oom_kills(self) -> int:
        if not self.mem:
            return 0
        if self.version == 2:
            return _kv(self.mem / "memory.events").get("oom_kill", 0)
        return _kv(self.mem / "memory.oom_control").get("oom_kill", 0)

    def cpu_seconds(self) -> float | None:
        if self.version == 2:
            usec = _kv(CG / "cpu.stat").get("usage_usec")
            return usec / 1e6 if usec is not None else None
        for d in ("cpuacct", "cpu,cpuacct", "cpu"):
            ns = _int(CG / d / "cpuacct.usage")
            if ns is not None:
                return ns / 1e9
        return None


def _raise_oom_score():
    # Hacemos que el OOM killer prefiera a la solución y no a la sonda.
    try:
        Path("/proc/self/oom_score_adj").write_text("1000")
    except OSError:
        pass
    os.setsid()


def main(script: str) -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    timeout = float(os.environ.get("BENCH_TIMEOUT", "120"))
    cg = Cgroup()
    oom0 = cg.oom_kills()
    cpu0 = cg.cpu_seconds()
    base = cg.unreclaimable_bytes() or 0  # la propia sonda ya ocupa algo
    peak = [base]
    stop = threading.Event()

    def sampler():
        while not stop.is_set():
            v = cg.unreclaimable_bytes()
            if v is not None and v > peak[0]:
                peak[0] = v
            stop.wait(0.05)

    t = threading.Thread(target=sampler, daemon=True)
    t.start()
    log = open(RESULTS / "solve.log", "wb")
    t0 = time.monotonic()
    timed_out = False
    proc = subprocess.Popen(
        ["bash", script], cwd="/workspace", stdout=log, stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL, preexec_fn=_raise_oom_score,
    )
    try:
        rc = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        rc = proc.wait()
    wall = time.monotonic() - t0
    stop.set()
    t.join(1)
    log.close()

    # Mata procesos sobrantes de la solución (demonios, dobles fork...).
    try:
        os.kill(-1, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass

    cpu1 = cg.cpu_seconds()
    cpu_s = (cpu1 - cpu0) if (cpu0 is not None and cpu1 is not None) else None
    oom = cg.oom_kills() - oom0
    total_peak = cg.total_peak_bytes()
    metrics = {
        "exit_code": rc,
        "timed_out": timed_out,
        "wall_s": round(wall, 3),
        "cpu_s": round(cpu_s, 3) if cpu_s is not None else None,
        "parallelism": round(cpu_s / wall, 2) if cpu_s and wall > 0 else None,
        "peak_unreclaimable_mb": round(peak[0] / 2**20, 1),
        "probe_baseline_mb": round(base / 2**20, 1),
        "peak_total_mb": round(total_peak / 2**20, 1) if total_peak else None,
        "oom_kills": oom,
        "cgroup_version": cg.version,
    }
    tmp = RESULTS / ".metrics.json.tmp"
    tmp.write_text(json.dumps(metrics))
    tmp.replace(RESULTS / "metrics.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "/bench/solve.sh"))
