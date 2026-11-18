#!/usr/bin/env bash
# Arreglo plausible pero INCORRECTO: "acotar" la cola a n. Es lo mismo que no acotarla.
set -euo pipefail
sed -i 's/q = queue.Queue()/q = queue.Queue(maxsize=prm["n"])/' pipeline.py
