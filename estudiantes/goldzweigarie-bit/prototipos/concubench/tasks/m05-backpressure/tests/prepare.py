"""Fase P: escribe /data/params.json y calcula el esperado (secuencial)."""
import hashlib
import json
import os
from pathlib import Path


def payload(seed, i, size):
    h = hashlib.sha256(f"{seed}:{i}".encode()).digest()
    return h * (size // len(h))


def work(p, rounds):
    d = b""
    for _ in range(rounds):
        d = hashlib.sha256(d + p).digest()
    return d


def main():
    seed = int(os.environ["BENCH_SEED"])
    scale = float(os.environ.get("BENCH_SCALE", "1"))
    data = Path(os.environ.get("BENCH_DATA", "/data"))
    exp = Path(os.environ.get("BENCH_EXPECTED", "/expected"))
    prm = {"seed": seed, "n": max(2_000, int(100_000 * scale)), "size": 4096, "rounds": 20}
    x = 0
    for i in range(prm["n"]):
        x ^= int.from_bytes(work(payload(seed, i, prm["size"]), prm["rounds"])[:8], "big")
    (data / "params.json").write_text(json.dumps(prm))
    (exp / "expected.json").write_text(json.dumps({"procesados": prm["n"], "xor": f"{x:016x}"}))


if __name__ == "__main__":
    main()
