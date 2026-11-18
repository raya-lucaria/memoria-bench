#!/usr/bin/env bash
set -euo pipefail
python3 /workspace/compute.py "${BENCH_DATA:-/data}/lecturas.npy" > "${BENCH_RESULTS:-/results}/output.json"
