#!/usr/bin/env bash
set -euo pipefail
python3 /workspace/pipeline.py "${BENCH_DATA:-/data}/params.json" > "${BENCH_RESULTS:-/results}/output.json"
