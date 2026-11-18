#!/usr/bin/env bash
# Fase G: así se invoca la solución. La sonda mide todo lo que pase aquí.
set -euo pipefail
python3 /workspace/agg.py "${BENCH_DATA:-/data}/trips.csv" > "${BENCH_RESULTS:-/results}/output.json"
