#!/usr/bin/env bash
# Oráculo: lectura en streaming con csv.reader; memoria O(#alcaldías).
set -euo pipefail
cat > agg.py <<'PY'
"""Agrega viajes por alcaldía en streaming.

Uso: python3 agg.py viajes.csv > salida.json
"""
import csv
import json
import sys


def main(path: str) -> None:
    acc = {}  # alcaldía -> [viajes, tarifa, distancia]
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        ia, idist, ifare = header.index("alcaldia"), header.index("distance_km"), header.index("fare_mxn")
        for row in reader:
            v = acc.get(row[ia])
            if v is None:
                v = acc[row[ia]] = [0, 0.0, 0.0]
            v[0] += 1
            v[1] += float(row[ifare])
            v[2] += float(row[idist])
    out = {
        a: {"viajes": n, "tarifa_total": round(t, 2), "distancia_media_km": round(d / n, 4)}
        for a, (n, t, d) in acc.items()
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1, sort_keys=True)
    print()


if __name__ == "__main__":
    main(sys.argv[1])
PY
