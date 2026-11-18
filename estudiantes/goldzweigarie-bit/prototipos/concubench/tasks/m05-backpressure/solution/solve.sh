#!/usr/bin/env bash
# Oráculo: cola acotada. put() bloquea al productor cuando hay MAXQ paquetes
# en vuelo → memoria O(MAXQ × 4 KB), independiente de n.
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
p = Path("pipeline.py")
src = p.read_text()
assert "q = queue.Queue()" in src
src = src.replace("CONSUMERS = 2\n", "CONSUMERS = 2\nMAXQ = 256  # paquetes en vuelo; acota la memoria\n", 1)
src = src.replace("q = queue.Queue()", "q = queue.Queue(maxsize=MAXQ)", 1)
p.write_text(src)
PY
