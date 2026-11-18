"""Fase C: comparación exacta."""
import json
import os
import sys
from pathlib import Path

EXP = Path(os.environ.get("BENCH_EXPECTED", "/expected"))
RES = Path(os.environ.get("BENCH_RESULTS", "/results"))


def verdict(ok, msg):
    (RES / "detail.json").write_text(json.dumps({"passed": ok, "message": msg}, ensure_ascii=False))
    print(msg)
    return 0 if ok else 1


def main():
    e = json.loads((EXP / "expected.json").read_text())
    try:
        g = json.loads((RES / "output.json").read_text())
    except (OSError, ValueError) as ex:
        return verdict(False, f"salida ilegible: {ex!r}")
    if not isinstance(g, dict):
        return verdict(False, "la salida no es un objeto JSON")
    if g.get("procesados") != e["procesados"]:
        return verdict(False, f"procesados {g.get('procesados')} != {e['procesados']}")
    if str(g.get("xor", "")).lower() != e["xor"]:
        return verdict(False, f"xor {g.get('xor')} != {e['xor']}")
    return verdict(True, "ok")


if __name__ == "__main__":
    sys.exit(main())
