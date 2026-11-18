"""Deterministic scoring. No model, no judge, no network."""
from __future__ import annotations

import re
from typing import Dict, Iterable, List, Optional, Tuple

from .generate import ABILITIES, UNKNOWN, Question
from .rng import Rng

AGE_BUCKETS = (("<10%", 0.0, 0.10), ("10-25%", 0.10, 0.25), ("25-50%", 0.25, 0.50), (">50%", 0.50, 1.01))


def norm(x) -> str:
    s = str(x).strip().rstrip(".").strip()
    while len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'`":
        s = s[1:-1].strip().rstrip(".").strip()
    return " ".join(s.casefold().split())


def as_items(ans) -> List[str]:
    if ans is None:
        return []
    if isinstance(ans, (list, tuple)):
        parts = ans
    else:
        parts = re.split(r"[,;\n]", str(ans))
    return [n for n in (norm(p) for p in parts) if n]


def score_one(fmt: str, gold, ans) -> float:
    """1.0 = exact. Lists use set F1. A missing answer (None) scores 0."""
    if ans is None:
        return 0.0
    if fmt == "list":
        p, g = set(as_items(ans)), set(norm(x) for x in gold)
        if not p and not g:
            return 1.0
        tp = len(p & g)
        if tp == 0:
            return 0.0
        pr, rc = tp / len(p), tp / len(g)
        return 2 * pr * rc / (pr + rc)
    if isinstance(ans, (list, tuple)):
        if len(ans) != 1:
            return 0.0
        ans = ans[0]
    if fmt == "count":
        try:
            return 1.0 if int(norm(ans)) == int(gold) else 0.0
        except ValueError:
            return 0.0
    return 1.0 if norm(ans) == norm(gold) else 0.0


def _mean(xs: List[float]) -> Optional[float]:
    return sum(xs) / len(xs) if xs else None


def summarize(items: Iterable[Tuple[Question, float, object]], boot: int = 400) -> Dict:
    """items: (question, score, raw_answer). Returns the per-track report block."""
    items = list(items)
    by_ab: Dict[str, List[float]] = {ab: [] for ab in ABILITIES}
    by_age: Dict[str, List[float]] = {b[0]: [] for b in AGE_BUCKETS}
    gold_unknown = halluc = answerable = false_abstain = 0
    for q, s, ans in items:
        by_ab[q.ability].append(s)
        if q.age_frac is not None:
            for name, lo, hi in AGE_BUCKETS:
                if lo <= q.age_frac < hi:
                    by_age[name].append(s)
                    break
        if q.gold == UNKNOWN:
            gold_unknown += 1
            if ans is not None and norm(ans) != norm(UNKNOWN):
                halluc += 1
        elif q.fmt == "value":
            answerable += 1
            if ans is not None and norm(ans) == norm(UNKNOWN):
                false_abstain += 1

    abilities = {ab: {"score": _mean(v), "n": len(v)} for ab, v in by_ab.items() if v}
    macro = _mean([a["score"] for a in abilities.values()])

    ci = None
    if macro is not None and boot:
        rng = Rng(12345)
        strata = [v for v in by_ab.values() if v]
        stats = []
        for _ in range(boot):
            stats.append(_mean([_mean([v[rng.below(len(v))] for _ in range(len(v))]) for v in strata]))
        stats.sort()
        ci = [stats[int(0.025 * boot)], stats[min(boot - 1, int(0.975 * boot))]]

    return {
        "macro": macro,
        "ci95": ci,
        "abilities": abilities,
        "age": {k: {"score": _mean(v), "n": len(v)} for k, v in by_age.items() if v},
        "hallucination_rate": (halluc / gold_unknown) if gold_unknown else None,
        "false_abstain_rate": (false_abstain / answerable) if answerable else None,
        "n_questions": len(items),
    }


def piso(questions: List[Question]) -> Optional[float]:
    """Macro de un sistema que siempre responde UNKNOWN: se calcula sin ningún agente."""
    return summarize([(q, score_one(q.fmt, q.gold, UNKNOWN), UNKNOWN) for q in questions], boot=0)["macro"]
