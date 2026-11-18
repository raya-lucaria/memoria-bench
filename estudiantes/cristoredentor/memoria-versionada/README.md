# memoria-versionada

Memoria de proyecto para agentes de programación, hecha de **Markdown bajo git** y un CLI de un solo archivo
(`mem.py`, sólo biblioteca estándar). Está pensada para compararse con otras arquitecturas de memoria (OptMem,
MemPalace, Letta MemFS, LLM Wiki, auto memory de Claude Code).

Tiene tres objetivos: **costar pocos tokens**, **no envenenarse** y **aprender de los errores** sin perder la
trazabilidad de cómo evolucionó el `AGENTS.md`.

## En 30 segundos

```
memoria/
  INDICE.md            ← lo único que se empuja al prompt (generado, ≤1,500 tokens, sin fechas)
  LOG.md               ← bitácora append-only: fecha | acción | id | sha | por | motivo
  notas/               ← R-* reglas, H-* hechos, E-* errores aprendidos (aprobadas por un humano)
  propuestas/          ← P-* cuarentena: lo que el agente sugiere y aún nadie revisa
  agents/v001.md …     ← cada versión de AGENTS.md
  agents/TRANSICIONES.md ← una fila por versión: +/− líneas, secciones, por qué, qué notas la causaron
```

```bash
python3 mem.py contexto                       # qué entra al prompt y cuánto cuesta
python3 mem.py proponer --tipo hecho --resumen "..." --fuente agente --evidencia "pytest -q"
python3 mem.py aprobar P-0004 --por humano    # sólo humanos; mueve a notas/ y reindexa
python3 mem.py error rutas-fantasma --resumen "..." --evidencia "ls src → No such file"
python3 mem.py version AGENTS.md --motivo "mapa real" --refs E-0001   # versiona y obsoleta lo promovido
python3 mem.py transicion v001 v002           # diff por secciones, sólo lo que cambió
python3 mem.py buscar "fixtures" 3            # BM25 sobre notas vigentes (pull)
python3 mem.py lint                           # esquema, privacidad, inyección, hashes, presupuesto
```

Para integrarlo con un agente, pega [`BLOQUE_AGENTS.md`](BLOQUE_AGENTS.md) (~200 tokens) en tu `AGENTS.md`.

## Ciclo de vida de una nota

```
agente ──proponer──▶ propuestas/P-*  ──aprobar (humano)──▶ notas/{R,H,E}-*  ──▶ INDICE.md
              │  escaneo de privacidad              │                          │
              │  e inyección (rechaza)              ├─ obsoletar / reemplaza   ├─ revisar cada 90 días
              ▼                                     └─ olvidar (privacidad)    └─ error ×2 ⇒ regla en AGENTS.md
          LOG.md (sha de cada versión)                                              ⇒ `version --refs` la saca del índice
```

## Cómo pasar de un AGENTS.md a otro

1. Lee `agents/TRANSICIONES.md`: una fila por versión, con lo que cambió y por qué (≈30 tokens por fila).
2. `mem.py transicion vA vB`: sólo las secciones tocadas, con marcas `+` (nueva), `−` (borrada) y `~` (cambió).
3. Las notas citadas en `refs` (`mem.py ver E-0001`) explican la lección que causó el cambio.

En el ejemplo incluido, v001 era una plantilla heredada cuyo mapa apuntaba a carpetas inexistentes. El agente
falló dos veces (E-0001 ×2), la lección se volvió regla en v002 («verifica una ruta con `ls` antes de confiar
en este mapa») y E-0001 salió del índice porque ya vive en AGENTS.md.

## Compararlo con otras memorias

Con `memeval` (banco sintético propio, sin LLM ni red) o cualquier banco de pruebas que hable por CLI (`add {id} {texto}` /
`search {consulta} {k}` → una línea por resultado que empieza con el id):

```bash
python3 -m memeval --backends bm25 \
  --externo "python3 mem.py --raiz /tmp/bench nota {id} {texto}" \
            "python3 mem.py --raiz /tmp/bench buscar {consulta} {k}"
```

Resultado de referencia (banco sintético, semilla 7, 290 notas, 100 preguntas, k=5, lector extractivo, una corrida):

| backend | recall@5 | exactitud | tokens/pregunta | p50 |
|---|---|---|---|---|
| bm25 (de memeval) | 0.73 | 0.57 | 79 | 5 ms |
| mem.py `buscar` | 0.68 | 0.56 | 82 | 66 ms (un proceso por llamada) |

La recuperación es léxica a propósito: se puede auditar y no tiene dependencias. Con paráfrasis cae, y la
búsqueda multi-sesión es débil. Lo que esta arquitectura aporta no se ve en recall@k: está en la escritura
(cuarentena, procedencia, hashes) y en el costo fijo del índice. Esta tabla mide sólo la búsqueda (pull), no
el flujo propuesta → aprobación.

## Tests

```bash
pytest -q test_mem.py && ruff check .
```

Decisiones, amenazas y comparación con otras arquitecturas: [`DISENO.md`](DISENO.md).
