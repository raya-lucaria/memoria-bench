#!/usr/bin/env bash
# Arreglo plausible pero INCORRECTO: cambia DictReader por readlines()+split.
# Sigue cargando todo el archivo en memoria. Debe morir por OOM.
set -euo pipefail
cat > agg.py <<'PY'
import json
import sys


def main(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()[1:]
    out = {}
    for line in lines:
        _, a, d, _, fare = line.rstrip("\n").split(",")
        v = out.setdefault(a, [0, 0.0, 0.0])
        v[0] += 1; v[1] += float(fare); v[2] += float(d)
    json.dump({a: {"viajes": n, "tarifa_total": round(t, 2), "distancia_media_km": round(d / n, 4)}
               for a, (n, t, d) in out.items()}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1])
PY
