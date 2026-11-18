#!/usr/bin/env python3
"""Floor baseline: remembers nothing, always answers UNKNOWN."""
import json
import sys

for line in sys.stdin:
    msg = json.loads(line)
    out = {"ok": True} if msg["op"] == "ingest" else {"answer": "UNKNOWN"}
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()
