"""Aggregate results/ into results/summary.json and print it."""
import json
import math
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent / "results"


def ci95(p: float, n: int) -> float:
    return 1.96 * math.sqrt(p * (1 - p) / n) if n else 0.0


def main():
    summary = {"retrieval": {}, "qa": {}}
    rows = [json.loads(l) for l in (OUT / "retrieval.jsonl").read_text().splitlines() if l]
    by = defaultdict(list)
    for r in rows:
        by[r["method"]].append(r)
    for m, rs in by.items():
        summary["retrieval"][m] = {k: round(100 * sum(r[k] for r in rs) / len(rs), 1)
                                   for k in ("any@5", "all@5", "any@10", "all@10")} | {"n": len(rs)}
    for f in sorted((OUT / "raw").glob("*.jsonl")):
        rs = [json.loads(l) for l in f.read_text().splitlines() if l]
        acc = sum(r["correct"] for r in rs) / len(rs)
        types = defaultdict(list)
        for r in rs:
            types["abstention" if r["abstention"] else r["type"]].append(r["correct"])
        summary["qa"][f.stem] = {"n": len(rs), "acc": round(100 * acc, 1),
                                 "ci95": round(100 * ci95(acc, len(rs)), 1),
                                 "by_type": {t: f"{sum(v)}/{len(v)}" for t, v in sorted(types.items())}}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
