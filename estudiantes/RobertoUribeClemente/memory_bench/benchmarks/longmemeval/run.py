"""LongMemEval pilot runner. Self-contained: its own data, retrieval, prompts and judge.

  uv run python -m benchmarks.longmemeval.run retrieval --n 30
  uv run python -m benchmarks.longmemeval.run qa --harness claude_code:haiku --condition retrieved
  uv run python -m benchmarks.longmemeval.run qa --harness opencode:deepseek-v4.1-flash-free --condition oracle
"""
from __future__ import annotations

import argparse
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from harnesses.base import load as load_harness

from . import data, prompts, retrieve

OUT = Path(__file__).resolve().parents[2] / "results"
JUDGE = "claude_code:sonnet"   # fixed by the benchmark, the same for every harness
K = 5                          # sessions handed to the reader
METHOD = "bge-small"           # memory used in the 'retrieved' condition
N, SEED = 30, 42


def cmd_retrieval(args):
    items = data.sample(data.load(), args.n, SEED)
    rows, ranks = [], {}
    for method in ["bm25", "minilm", "bge-small"]:
        t0 = time.time()
        for it in items:
            r = retrieve.rank_sessions(method, it)
            ranks.setdefault(method, {})[it["question_id"]] = r
            if data.is_abstention(it):
                continue
            rows.append({"method": method, "qid": it["question_id"], "type": it["question_type"],
                         **{f"{m}@{k}": f(r, it, k) for k in (5, 10)
                            for m, f in (("any", retrieve.recall_any), ("all", retrieve.recall_all))}})
        print(f"{method}: {time.time() - t0:.0f}s")
    OUT.mkdir(exist_ok=True)
    (OUT / "retrieval_ranks.json").write_text(json.dumps(ranks))
    (OUT / "retrieval.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def _yes(text: str) -> bool:
    return text.strip().lower().lstrip("*\"' ").startswith("yes")


def cmd_qa(args):
    items = data.sample(data.load(), args.n, SEED)
    oracle = {o["question_id"]: o for o in data.load("longmemeval_oracle.json")}
    ranks = (json.loads((OUT / "retrieval_ranks.json").read_text())[METHOD]
             if args.condition == "retrieved" else {})
    reader, judge = load_harness(args.harness), load_harness(JUDGE)
    path = OUT / "raw" / f"{args.harness.replace(':', '__').replace('/', '_')}__{args.condition}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["qid"] for l in path.read_text().splitlines()} if path.exists() else set()
    lock = threading.Lock()

    def one(it):
        if args.condition == "oracle":
            o = oracle[it["question_id"]]
            hist = prompts.history(o, list(range(len(o["haystack_sessions"]))))
        else:
            hist = prompts.history(it, ranks[it["question_id"]][:K])
        p = prompts.READER.format(history=hist, date=it["question_date"], question=it["question"])
        try:
            hyp = reader.ask(p)
            verdict = judge.ask(prompts.judge(it["question_type"], it["question"], it["answer"],
                                              hyp, data.is_abstention(it)))
            row = {"qid": it["question_id"], "type": it["question_type"],
                   "abstention": data.is_abstention(it), "hypothesis": hyp,
                   "verdict": verdict, "correct": _yes(verdict), "prompt_chars": len(p)}
        except Exception as e:  # keep going; rerun later resumes the missing ones
            print(f"ERR {it['question_id']}: {e}")
            return
        with lock, path.open("a") as f:
            f.write(json.dumps(row) + "\n")
        print(f"{it['question_id']:<24} {'OK ' if row['correct'] else 'no '} {hyp[:70]!r}")

    todo = [it for it in items if it["question_id"] not in done]
    with ThreadPoolExecutor(args.workers) as ex:
        list(ex.map(one, todo))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("retrieval"); r.add_argument("--n", type=int, default=N)
    q = sub.add_parser("qa"); q.add_argument("--harness", required=True)
    q.add_argument("--condition", choices=["retrieved", "oracle"], default="retrieved")
    q.add_argument("--n", type=int, default=N); q.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    {"retrieval": cmd_retrieval, "qa": cmd_qa}[a.cmd](a)


if __name__ == "__main__":
    main()
