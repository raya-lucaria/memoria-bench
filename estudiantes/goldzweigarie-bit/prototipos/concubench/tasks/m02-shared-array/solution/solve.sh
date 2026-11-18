#!/usr/bin/env bash
# Oráculo: cada worker mapea el archivo (mmap_mode="r") y procesa SU rango por
# sub-bloques. Nada se copia entre procesos; solo viajan (inicio, fin) y 2 números.
set -euo pipefail
cat > compute.py <<'PY'
"""Estadísticas de un arreglo grande con 4 workers, sin copiarlo.

Uso: python3 compute.py lecturas.npy
"""
import json
import sys
from multiprocessing import Pool

import numpy as np

WORKERS = 4
SUB = 1_000_000  # 8 MB por sub-bloque


def work(args):
    path, start, stop = args
    x = np.load(path, mmap_mode="r")          # vista mapeada: page cache, no anon
    total, count = 0.0, 0
    for i in range(start, stop, SUB):
        blk = np.asarray(x[i:min(i + SUB, stop)])
        total += float(np.sqrt(np.abs(blk)).sum())
        count += int((blk > 2.0).sum())
    return total, count


def main(path):
    n = np.load(path, mmap_mode="r").shape[0]
    edges = np.linspace(0, n, WORKERS * 4 + 1, dtype=np.int64)
    tasks = [(path, int(a), int(b)) for a, b in zip(edges[:-1], edges[1:])]
    with Pool(WORKERS) as pool:
        parts = pool.map(work, tasks)
    print(json.dumps({"suma_raiz_abs": sum(p[0] for p in parts), "mayores_a_2": sum(p[1] for p in parts)}))


if __name__ == "__main__":
    main(sys.argv[1])
PY
