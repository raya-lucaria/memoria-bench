"""Fase P: genera /data/lecturas.npy (memmap, por bloques) y el esperado."""
import json
import os
from pathlib import Path

import numpy as np

BLOQUE = 2_000_000


def main():
    seed = int(os.environ["BENCH_SEED"])
    scale = float(os.environ.get("BENCH_SCALE", "1"))
    data = Path(os.environ.get("BENCH_DATA", "/data"))
    exp = Path(os.environ.get("BENCH_EXPECTED", "/expected"))
    n = max(100_000, int(50_000_000 * scale))
    rng = np.random.default_rng(seed)
    out = np.lib.format.open_memmap(data / "lecturas.npy", mode="w+", dtype=np.float64, shape=(n,))
    total, count = 0.0, 0
    for i in range(0, n, BLOQUE):
        blk = rng.standard_normal(min(BLOQUE, n - i)) * 1.5
        out[i:i + len(blk)] = blk
        total += float(np.sqrt(np.abs(blk)).sum())
        count += int((blk > 2.0).sum())
        out.flush()
    del out
    (exp / "expected.json").write_text(json.dumps({"suma_raiz_abs": total, "mayores_a_2": count}))


if __name__ == "__main__":
    main()
