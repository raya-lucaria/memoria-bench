"""Genera un CSV de muestra con el mismo formato que el de calificación.

Uso: python3 gen_sample.py --rows 300000 /tmp/muestra.csv
"""
import argparse
import random

ALCALDIAS = [
    "Álvaro Obregón", "Azcapotzalco", "Benito Juárez", "Coyoacán", "Cuajimalpa de Morelos",
    "Cuauhtémoc", "Gustavo A. Madero", "Iztacalco", "Iztapalapa", "La Magdalena Contreras",
    "Miguel Hidalgo", "Milpa Alta", "Tláhuac", "Tlalpan", "Venustiano Carranza", "Xochimilco",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--rows", type=int, default=100_000)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("trip_id,alcaldia,distance_km,duration_min,fare_mxn\n")
        for i in range(a.rows):
            d = max(30, int(rng.lognormvariate(5.9, 0.7)))      # centésimas de km
            dur = max(10, int(d * rng.uniform(0.25, 0.6)))      # décimas de minuto
            fare = 850 + d * 5 + dur * 9                        # centavos
            f.write(f"{i},{rng.choice(ALCALDIAS)},{d // 100}.{d % 100:02d},"
                    f"{dur // 10}.{dur % 10},{fare // 100}.{fare % 100:02d}\n")


if __name__ == "__main__":
    main()
