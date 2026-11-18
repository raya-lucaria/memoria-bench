"""Agrega viajes por alcaldía.

Uso: python3 agg.py viajes.csv > salida.json
"""
import csv
import json
import sys


def main(path: str) -> None:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    out = {}
    for r in rows:
        a = r["alcaldia"]
        if a not in out:
            out[a] = {"viajes": 0, "tarifa_total": 0.0, "_dist": 0.0}
        out[a]["viajes"] += 1
        out[a]["tarifa_total"] += float(r["fare_mxn"])
        out[a]["_dist"] += float(r["distance_km"])

    for a, v in out.items():
        v["tarifa_total"] = round(v["tarifa_total"], 2)
        v["distancia_media_km"] = round(v.pop("_dist") / v["viajes"], 4)

    json.dump(out, sys.stdout, ensure_ascii=False, indent=1, sort_keys=True)
    print()


if __name__ == "__main__":
    main(sys.argv[1])
