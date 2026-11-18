"""Fase C: compara la salida con el esperado."""
import json
import math
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
        s, c = float(g["suma_raiz_abs"]), int(g["mayores_a_2"])
    except (OSError, ValueError, KeyError, TypeError) as ex:
        return verdict(False, f"salida inválida: {ex!r}")
    if c != e["mayores_a_2"]:
        return verdict(False, f"mayores_a_2 {c} != {e['mayores_a_2']}")
    if not math.isclose(s, e["suma_raiz_abs"], rel_tol=1e-9):
        return verdict(False, f"suma_raiz_abs {s} != {e['suma_raiz_abs']}")
    return verdict(True, "ok")


if __name__ == "__main__":
    sys.exit(main())
