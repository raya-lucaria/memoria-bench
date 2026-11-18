#!/usr/bin/env python3
"""peakmem CMD...  — corre CMD y reporta el pico de RSS sumado de todo su árbol.

Para que el agente pruebe sus cambios dentro del contenedor del agente, que tiene
más memoria que el de calificación. Suma hijos (multiprocessing cuenta).
La calificación real no usa esto: usa el cgroup (ver bench/probe.py).
"""
import os
import subprocess
import sys
import time


def tree_rss_kb(root: int) -> int:
    parents = {}
    rss = {}
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            with open(f"/proc/{pid}/status") as f:
                ppid = vm = 0
                for line in f:
                    if line.startswith("PPid:"):
                        ppid = int(line.split()[1])
                    elif line.startswith("VmRSS:"):
                        vm = int(line.split()[1])
            parents[int(pid)] = ppid
            rss[int(pid)] = vm
        except (OSError, ValueError):
            continue
    total, stack = 0, [root]
    seen = set()
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        total += rss.get(p, 0)
        stack.extend(c for c, pp in parents.items() if pp == p)
    return total


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    t0 = time.monotonic()
    proc = subprocess.Popen(sys.argv[1:])
    peak = 0
    while proc.poll() is None:
        peak = max(peak, tree_rss_kb(proc.pid))
        time.sleep(0.02)
    print(f"[peakmem] pico RSS ≈ {peak / 1024:.1f} MB · {time.monotonic() - t0:.2f} s · rc={proc.returncode}",
          file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
