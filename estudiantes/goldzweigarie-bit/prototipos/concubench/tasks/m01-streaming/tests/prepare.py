"""Fase P: genera /data/trips.csv y /expected/expected.json.

Los valores se generan como enteros (centavos, centésimas de km) para que el
esperado sea exacto. Se genera con numpy por bloques: memoria acotada.
"""
import json
import os
from pathlib import Path

import numpy as np

ALCALDIAS = [
    "Álvaro Obregón", "Azcapotzalco", "Benito Juárez", "Coyoacán", "Cuajimalpa de Morelos",
    "Cuauhtémoc", "Gustavo A. Madero", "Iztacalco", "Iztapalapa", "La Magdalena Contreras",
    "Miguel Hidalgo", "Milpa Alta", "Tláhuac", "Tlalpan", "Venustiano Carranza", "Xochimilco",
]
# pesos aproximados por población
PESOS = np.array([7.6, 4.3, 4.6, 6.6, 2.4, 5.8, 12.6, 4.2, 19.8, 2.7, 4.0, 1.5, 4.0, 7.3, 4.6, 4.9])
PESOS = PESOS / PESOS.sum()
BLOQUE = 250_000


def main():
    seed = int(os.environ["BENCH_SEED"])
    scale = float(os.environ.get("BENCH_SCALE", "1"))
    data = Path(os.environ.get("BENCH_DATA", "/data"))
    exp = Path(os.environ.get("BENCH_EXPECTED", "/expected"))
    n = max(2_000, int(5_000_000 * scale))
    rng = np.random.default_rng(seed)

    viajes = np.zeros(len(ALCALDIAS), dtype=np.int64)
    tarifa = np.zeros(len(ALCALDIAS), dtype=np.int64)   # centavos
    dist = np.zeros(len(ALCALDIAS), dtype=np.int64)     # centésimas de km

    with open(data / "trips.csv", "w", encoding="utf-8", buffering=1 << 20) as f:
        f.write("trip_id,alcaldia,distance_km,duration_min,fare_mxn\n")
        for start in range(0, n, BLOQUE):
            m = min(BLOQUE, n - start)
            a = rng.choice(len(ALCALDIAS), size=m, p=PESOS)
            d = np.maximum(30, rng.lognormal(5.9, 0.7, m).astype(np.int64))
            dur = np.maximum(10, (d * rng.uniform(0.25, 0.6, m)).astype(np.int64))
            fare = 850 + d * 5 + dur * 9
            viajes += np.bincount(a, minlength=len(ALCALDIAS))
            tarifa += np.bincount(a, weights=fare, minlength=len(ALCALDIAS)).astype(np.int64)
            dist += np.bincount(a, weights=d, minlength=len(ALCALDIAS)).astype(np.int64)
            lines = [
                f"{start + i},{ALCALDIAS[ai]},{di // 100}.{di % 100:02d},{ui // 10}.{ui % 10},{fi // 100}.{fi % 100:02d}"
                for i, (ai, di, ui, fi) in enumerate(zip(a.tolist(), d.tolist(), dur.tolist(), fare.tolist()))
            ]
            f.write("\n".join(lines))
            f.write("\n")

    expected = {
        ALCALDIAS[i]: {
            "viajes": int(viajes[i]),
            "tarifa_total": int(tarifa[i]) / 100,
            "distancia_media_km": round(int(dist[i]) / 100 / int(viajes[i]), 4),
        }
        for i in range(len(ALCALDIAS)) if viajes[i] > 0
    }
    (exp / "expected.json").write_text(json.dumps(expected, ensure_ascii=False))


if __name__ == "__main__":
    main()
