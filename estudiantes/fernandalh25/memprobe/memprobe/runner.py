"""Runs a system under test (SUT) as a subprocess speaking JSON lines on
stdin/stdout. Any language, any framework, any model (or none).

Runner -> SUT (one JSON object per line, strictly request/response):
    {"op":"ingest","seq":0,"text":"Day 1: ..."}            -> {"ok":true}
    {"op":"query","seq":0,"q":"...","format":"value"}      -> {"answer": "..." | ["..",".."] | 3}
The SUT is started fresh for every episode, so it never needs a reset op.
When the runner is done it closes the SUT's stdin.
"""
from __future__ import annotations

import json
import queue
import subprocess
import threading
import time
from dataclasses import dataclass, field
from typing import List, Optional

from .generate import Episode


class SutError(Exception):
    pass


class Sut:
    def __init__(self, argv: List[str], timeout: float, cwd: Optional[str] = None):
        self.timeout = timeout
        try:
            self.proc = subprocess.Popen(
                argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                encoding="utf-8", bufsize=1, cwd=cwd)
        except OSError as e:
            raise SutError("cannot start SUT: %s" % e)
        self.lines: "queue.Queue[Optional[str]]" = queue.Queue()
        self.pump = threading.Thread(target=self._pump, daemon=True)
        self.pump.start()

    def _pump(self) -> None:
        for line in self.proc.stdout:
            self.lines.put(line)
        self.lines.put(None)

    def call(self, msg: dict) -> dict:
        try:
            self.proc.stdin.write(json.dumps(msg, ensure_ascii=True) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            raise SutError("SUT closed its stdin (crashed?)")
        try:
            line = self.lines.get(timeout=self.timeout)
        except queue.Empty:
            raise SutError("timeout after %ss" % self.timeout)
        if line is None:
            raise SutError("SUT exited")
        try:
            resp = json.loads(line)
        except ValueError:
            raise SutError("non-JSON line on stdout (stdout is protocol-only): %r" % line[:80])
        if not isinstance(resp, dict):
            raise SutError("response is not a JSON object")
        return resp

    def close(self) -> None:
        try:
            self.proc.stdin.close()
        except Exception:
            pass
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()
        self.pump.join(timeout=2)
        try:
            self.proc.stdout.close()
        except Exception:
            pass


@dataclass
class EpisodeResult:
    episode: Episode
    answers: List[object]  # raw answer per question (None = no answer)
    crashed: Optional[str] = None
    ingest_errors: int = 0
    t_ingest: float = 0.0
    t_query: float = 0.0


def run_episode(argv: List[str], ep: Episode, timeout: float = 60.0, cwd: Optional[str] = None) -> EpisodeResult:
    qs = ep.questions
    order = sorted(range(len(qs)), key=lambda i: qs[i].after_seq)  # stable
    res = EpisodeResult(ep, [None] * len(qs))
    try:
        sut = Sut(argv, timeout, cwd)
    except SutError as e:
        res.crashed = str(e)
        return res
    try:
        oi = 0

        def ask_due(upto: int) -> None:
            nonlocal oi
            while oi < len(order) and qs[order[oi]].after_seq <= upto:
                i = order[oi]
                t = time.time()
                r = sut.call({"op": "query", "seq": i, "q": qs[i].q, "format": qs[i].fmt})
                res.t_query += time.time() - t
                res.answers[i] = r.get("answer")
                oi += 1

        for seq, text in enumerate(ep.events):
            ask_due(seq)
            t = time.time()
            r = sut.call({"op": "ingest", "seq": seq, "text": text})
            res.t_ingest += time.time() - t
            if r.get("ok") is False:
                res.ingest_errors += 1
        ask_due(len(ep.events))
    except SutError as e:
        res.crashed = str(e)
    finally:
        sut.close()
    return res
