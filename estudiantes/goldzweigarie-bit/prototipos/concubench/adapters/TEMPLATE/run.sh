#!/usr/bin/env bash
# Plantilla de adaptador. Copia a adapters/<tu-harness>/run.sh.
#
#   $1 = nombre del contenedor (actúa solo con: docker exec "$1" ...)
#   $2 = ruta del prompt en el host
#
# El benchmark no sabe ni le importa qué modelo usas. Ejemplos:
#   - tu harness propio:   python3 -m harness.run --container "$1" --prompt "$2"
#   - modelo local gratis: OPENAI_BASE_URL=http://localhost:11434/v1 OPENAI_MODEL=qwen2.5-coder:7b
set -euo pipefail
CONTAINER="$1"
PROMPT="$2"

# Ejemplo trivial: mostrar el workspace y terminar (equivale a null).
docker exec "$CONTAINER" ls -la /workspace

# Opcional: metadatos para la tabla de resultados.
cat > "$BENCH_ARTIFACTS/meta.json" <<JSON
{"model": "${OPENAI_MODEL:-none}", "steps": 0}
JSON
