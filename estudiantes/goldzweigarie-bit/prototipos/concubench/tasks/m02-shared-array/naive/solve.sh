#!/usr/bin/env bash
# Arreglo plausible pero INCORRECTO: "quitar multiprocessing para no copiar".
# Carga todo y vectoriza sobre el arreglo entero: x + |x| + sqrt = 1.2 GB. OOM.
set -euo pipefail
cat > compute.py <<'PY'
import json
import sys

import numpy as np


def main(path):
    x = np.load(path)
    print(json.dumps({"suma_raiz_abs": float(np.sqrt(np.abs(x)).sum()), "mayores_a_2": int((x > 2.0).sum())}))


if __name__ == "__main__":
    main(sys.argv[1])
PY
