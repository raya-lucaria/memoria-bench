"""Load LongMemEval-S (cleaned) and draw the fixed, stratified pilot sample."""
import json
import random
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data"
TYPES = ["single-session-user", "single-session-assistant", "single-session-preference",
         "multi-session", "knowledge-update", "temporal-reasoning"]


def load(name: str = "longmemeval_s_cleaned.json") -> list[dict]:
    return json.loads((DATA / name).read_text())


def sample(items: list[dict], n: int, seed: int = 42) -> list[dict]:
    """n // 6 questions per question type, same seed for every harness."""
    by_type = defaultdict(list)
    for it in items:
        by_type[it["question_type"]].append(it)
    rng = random.Random(seed)
    per = max(1, n // len(TYPES))
    out = []
    for t in TYPES:
        pool = sorted(by_type[t], key=lambda x: x["question_id"])
        out += rng.sample(pool, min(per, len(pool)))
    return out


def is_abstention(item: dict) -> bool:
    return item["question_id"].endswith("_abs")
