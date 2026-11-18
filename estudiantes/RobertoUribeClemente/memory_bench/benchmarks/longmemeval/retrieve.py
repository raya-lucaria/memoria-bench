"""The memory layer under test: local retrieval only (BM25 or a local embedder).

Keys are rounds (one user turn + the assistant reply). A session scores the max
of its rounds, and the top-k sessions are what the reader gets to see.
"""
from __future__ import annotations

import re

import numpy as np

EMBEDDERS = {
    "bge-small": "BAAI/bge-small-en-v1.5",
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
}
_models: dict = {}


def rounds(item: dict) -> tuple[list[str], list[int]]:
    texts, owner = [], []
    for si, session in enumerate(item["haystack_sessions"]):
        for i in range(0, len(session), 2):
            pair = session[i:i + 2]
            texts.append(" ".join(f"{t['role']}: {t['content']}" for t in pair)[:2000])
            owner.append(si)
    return texts, owner


def _tok(s: str) -> list[str]:
    return re.findall(r"\w+", s.lower())


def _scores(method: str, query: str, texts: list[str]) -> np.ndarray:
    if method == "bm25":
        from rank_bm25 import BM25Okapi
        return np.asarray(BM25Okapi([_tok(t) for t in texts]).get_scores(_tok(query)))
    from fastembed import TextEmbedding
    if method not in _models:
        _models[method] = TextEmbedding(EMBEDDERS[method], threads=8)
    m = _models[method]
    q = np.asarray(list(m.query_embed([query]))[0])
    d = np.asarray(list(m.passage_embed(texts, batch_size=64)))
    return d @ q / (np.linalg.norm(d, axis=1) * np.linalg.norm(q) + 1e-9)


def rank_sessions(method: str, item: dict) -> list[int]:
    texts, owner = rounds(item)
    s = _scores(method, item["question"], texts)
    best: dict[int, float] = {}
    for score, si in zip(s, owner):
        best[si] = max(best.get(si, -1e9), float(score))
    return sorted(best, key=best.get, reverse=True)


def recall_any(ranked: list[int], item: dict, k: int) -> float:
    ids = item["haystack_session_ids"]
    gold = set(item["answer_session_ids"])
    return float(any(ids[i] in gold for i in ranked[:k]))


def recall_all(ranked: list[int], item: dict, k: int) -> float:
    ids = item["haystack_session_ids"]
    gold = set(item["answer_session_ids"])
    return float(gold <= {ids[i] for i in ranked[:k]})
