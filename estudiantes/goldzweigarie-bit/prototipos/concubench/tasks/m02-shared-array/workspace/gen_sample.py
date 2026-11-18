"""Genera un .npy de muestra. Uso: python3 gen_sample.py --n 20000000 /tmp/muestra.npy"""
import argparse

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--n", type=int, default=5_000_000)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    out = np.lib.format.open_memmap(a.out, mode="w+", dtype=np.float64, shape=(a.n,))
    step = 1_000_000
    for i in range(0, a.n, step):
        out[i:i + step] = rng.standard_normal(min(step, a.n - i)) * 1.5
    out.flush()


if __name__ == "__main__":
    main()
