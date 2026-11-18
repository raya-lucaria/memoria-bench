"""Fase C: compara /results/output.json con /expected/expected.json."""
import json
import math
import os
import sys
from pathlib import Path

EXP = Path(os.environ.get("BENCH_EXPECTED", "/expected"))
RES = Path(os.environ.get("BENCH_RESULTS", "/results"))


def verdict(ok: bool, msg: str) -> int:
    (RES / "detail.json").write_text(json.dumps({"passed": ok, "message": msg}, ensure_ascii=False))
    print(msg)
    return 0 if ok else 1


def main() -> int:
    expected = json.loads((EXP / "expected.json").read_text())
    try:
        got = json.loads((RES / "output.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return verdict(False, f"salida ilegible: {e}")
    if not isinstance(got, dict):
        return verdict(False, "la salida no es un objeto JSON")
    if set(got) != set(expected):
        return verdict(False, f"alcaldías distintas: faltan {sorted(set(expected) - set(got))[:3]}, "
                              f"sobran {sorted(set(got) - set(expected))[:3]}")
    for a, e in expected.items():
        g = got[a]
        try:
            if int(g["viajes"]) != e["viajes"]:
                return verdict(False, f"{a}: viajes {g['viajes']} != {e['viajes']}")
            for k in ("tarifa_total", "distancia_media_km"):
                if not math.isclose(float(g[k]), e[k], rel_tol=1e-6, abs_tol=1e-4):
                    return verdict(False, f"{a}: {k} {g[k]} != {e[k]}")
        except (KeyError, TypeError, ValueError) as ex:
            return verdict(False, f"{a}: formato inválido ({ex!r})")
    return verdict(True, f"ok: {len(expected)} alcaldías")


if __name__ == "__main__":
    sys.exit(main())
