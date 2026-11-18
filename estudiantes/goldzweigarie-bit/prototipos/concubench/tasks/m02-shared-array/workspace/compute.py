"""Estadísticas de un arreglo grande con 4 workers.

Uso: python3 compute.py lecturas.npy
"""
import json
import sys
from multiprocessing import Pool

import numpy as np

WORKERS = 4


def work(chunk: np.ndarray) -> tuple[float, int]:
    return float(np.sqrt(np.abs(chunk)).sum()), int((chunk > 2.0).sum())


def main(path: str) -> None:
    x = np.load(path)
    chunks = np.array_split(x, WORKERS * 4)
    with Pool(WORKERS) as pool:
        parts = pool.map(work, chunks)
    total = sum(p[0] for p in parts)
    count = sum(p[1] for p in parts)
    print(json.dumps({"suma_raiz_abs": total, "mayores_a_2": count}))


if __name__ == "__main__":
    main(sys.argv[1])
