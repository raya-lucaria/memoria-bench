#!/usr/bin/env python3
"""Copy this file and fill in the two methods. That is the whole integration.

Rules:
  * stdout carries ONLY protocol lines (print debug output to stderr).
  * You get plain text. You decide what to store and how to answer
    (database, vector store, LLM harness, plain text file, ...).
  * Answer "UNKNOWN" when the history does not establish the answer.
  * format "value" -> a string; "list" -> a list of strings; "count" -> a number.
"""
import json
import sys


class MemorySystem:
    def __init__(self):
        pass  # a fresh process is started for every episode: start empty

    def ingest(self, text: str) -> None:
        raise NotImplementedError

    def answer(self, question: str, fmt: str):
        raise NotImplementedError


def main():
    system = MemorySystem()
    for line in sys.stdin:
        msg = json.loads(line)
        if msg["op"] == "ingest":
            system.ingest(msg["text"])
            reply = {"ok": True}
        else:
            reply = {"answer": system.answer(msg["q"], msg["format"])}
        sys.stdout.write(json.dumps(reply) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
