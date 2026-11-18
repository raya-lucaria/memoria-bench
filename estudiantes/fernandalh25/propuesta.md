---
# PARTE ESTÁNDAR. Los valores "no-se" son datos que no están documentados en mi
# scouting ni en memprobe; no se inventaron.

login: "fernandalh25"
harnesses: [claude-code]
suscripciones: ["Claude Pro"]
sistema_operativo: "macos"

memorias:
  # Baselines de memprobe (memprobe/README.md, sección "Condiciones").
  - id: ninguna
    tipo: [ninguna]
    fuente: "propio (memprobe/README.md)"
    sin_api_key: si          # la condición solo usa al agente de la suscripción; sin verificar con un agente real
    facilidad: no-se
    interes: 2
  - id: contexto-completo
    tipo: [logs-crudos]      # todo el historial en una sola conversación
    fuente: "propio (memprobe/README.md)"
    sin_api_key: si          # sin verificar con un agente real
    facilidad: no-se
    interes: 2
  # Propuesta a futuro (hipótesis 3 del README de memprobe). No se ha evaluado.
  - id: claude-md-manual
    tipo: [archivo-instrucciones]
    fuente: no-se
    sin_api_key: si          # es un archivo de texto; sin verificar
    facilidad: no-se
    interes: 2

benchmarks:
  - id: propio-memprobe
    mide: "mantener un estado que cambia entre sesiones: recordar, actualizar, consultar por fecha, encadenar, agregar, abstenerse y olvidar"
    fuente: propio
    calificacion: automatica
    casos: 42                # por semilla en el tamaño chico (70 medio, 140 grande)
    cabe_en_suscripcion: no-se
    interes: 2
  - id: longmemeval
    mide: "extracción, razonamiento entre sesiones, razonamiento temporal, actualización de conocimiento y abstención"
    fuente: "https://arxiv.org/abs/2410.10813"
    calificacion: llm-juez   # el código oficial usa un juez GPT-4o (según mi scouting)
    casos: 500
    cabe_en_suscripcion: no-se
    interes: 2
  - id: locomo
    mide: "QA sobre conversaciones largas (un salto, multi-salto, temporal, sentido común, adversarial) y resumen de eventos"
    fuente: "https://arxiv.org/abs/2402.17753"
    calificacion: no-se      # F1 en el paper; muchos trabajos posteriores usan juez LLM
    casos: no-se             # 10 conversaciones en la versión pública (según mi scouting)
    cabe_en_suscripcion: no-se
    interes: 2
  - id: memoryagentbench
    mide: "recuperación precisa, aprendizaje en tiempo de prueba, comprensión de largo alcance y olvido selectivo / resolución de conflictos"
    fuente: "https://arxiv.org/abs/2507.05257"
    calificacion: no-se
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: beam
    mide: "memoria a largo plazo a escala (128K a 10M tokens)"
    fuente: "https://arxiv.org/abs/2510.27246"
    calificacion: no-se
    casos: 2000              # preguntas validadas, según mi scouting; sin verificar
    cabe_en_suscripcion: no-se
    interes: 2
  - id: memoryarena
    mide: "si la memoria de sesiones previas ayuda al agente a actuar después en tareas con subtareas interdependientes"
    fuente: "https://arxiv.org/abs/2602.16313"
    calificacion: no-se
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: dreambench-swe
    mide: "higiene de memoria para agentes de código en tareas de software de varias sesiones"
    fuente: "https://arxiv.org/pdf/2608.20664"
    calificacion: automatica # pruebas ejecutables ocultas, según mi scouting
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2

# Ninguno de estos experimentos se ha corrido con agentes reales. Todos salen del README de memprobe.
experimentos:
  - pregunta: "¿Un agente real en Claude Code supera el piso (ninguna) con contexto-completo en memprobe, y en qué habilidades falla?"
    memorias: [ninguna, contexto-completo]
    harnesses: [claude-code]
    benchmark: propio-memprobe
    por_que_interesa: "Es la primera corrida real de memprobe; calibra el benchmark antes de comparar memorias. Usa al menos 3 semillas."
  - pregunta: "¿Un CLAUDE.md hecho a mano recuerda mejor que ninguna en memprobe chico y se degrada con el tamaño grande?"
    memorias: [claude-md-manual, ninguna, contexto-completo]
    harnesses: [claude-code]
    benchmark: propio-memprobe
    por_que_interesa: "Hipótesis 3 del README de memprobe (sin verificar)."
  - pregunta: "¿Cambia la exactitud entre la pista prose y la pista code, con los mismos hechos y las mismas preguntas?"
    memorias: [ninguna, contexto-completo]
    harnesses: [claude-code]
    benchmark: propio-memprobe
    por_que_interesa: "Según el README, esa brecha muestra si un sistema favorece un tipo de contenido."

roles: [armar-benchmark, motor-comun, analisis-y-graficas]
quiero_encargarme_de: ["diseño, implementación y análisis de memprobe (propio-memprobe)"]
disponibilidad: media
---

# Propuesta de fernandalh25

## Mi scouting

Está en `scouting/`, tal cual lo escribí, sin reescribir:

- `scouting/memory-benchmarks.html`: cómo funcionan los benchmarks de memoria
  para agentes (LoCoMo, LongMemEval, MemoryAgentBench, BEAM, MemoryArena,
  DreamBench-SWE), qué mide cada uno, cómo califica y qué debilidades se les
  reportan. Es un resumen de búsquedas; no corrí ningún benchmark.
- `scouting/harness-research.html`: notas de lectura de código de seis
  harnesses (Claude Code vía su SDK abierto, pi, Hermes Agent, SWE-agent,
  mini-swe-agent y la pila de Prime Intellect). Nada se ejecutó; el código del
  loop de Claude Code es cerrado, así que solo se revisó su SDK y docs públicas.
  Ahí cada afirmación lleva una etiqueta (verificado / documentado / inferido).

Lo que me llevó a `memprobe`: según mi scouting, el código oficial de
LongMemEval califica con un LLM juez (requiere API key), y un baseline de
"todo el contexto en el prompt" se reporta competitivo en LoCoMo y LongMemEval
(sin verificar de forma independiente). Eso choca con la regla de que nadie
paga API keys y con la de comparar contra un baseline tonto.

## Lo que está verificado

Solo esto, y solo de memprobe (`memprobe/`):

- Las 31 pruebas de `memprobe/tests/pruebas.py` pasan
  (`python3 -m unittest discover -s tests -p pruebas.py`; corridas el
  2026-11-17 en macOS).
- Según el README (no lo volví a correr para esta propuesta): la generación es
  determinista, cada pregunta se contesta solo con el flujo de eventos, la
  calificación es exacta, y un sistema de reglas (`examples/reference-sut.py`)
  con una habilidad rota falla justo en esa habilidad. Ese sistema **no es un
  agente ni un harness**; solo valida el benchmark.

## Lo que NO está verificado

- **Nadie ha corrido memprobe con un agente real ni con un sistema de memoria
  real.** No hay resultados de Claude Code, `CLAUDE.md`, OptMem, MemPalace, etc.
- No se ha medido cuánto cuesta un kit en la suscripción
  (`cabe_en_suscripcion: no-se`; solo hay estimaciones de tamaño).
- No sé cómo se desactiva la memoria nativa de Claude Code ni si se puede
  manejar sin interfaz; por eso el camino principal de memprobe es manual.
- Las cifras de mi scouting sobre otros benchmarks (por ejemplo errores en el
  answer key de LoCoMo, o que MemoryArena reporta que los agentes que van bien
  en LoCoMo van mal en tareas agénticas) vienen de fuentes de terceros; son
  pistas para revisar, no hechos.

## `propio-memprobe`: benchmark propuesto

Benchmark de memoria con calificación automática: sin LLM juez, sin API keys,
sin embeddings y sin red; solo biblioteca estándar de Python. Genera con una
semilla un flujo de eventos con fechas sobre entidades inventadas, mezclado con
distractores y repartido en sesiones; después hace preguntas en una
conversación nueva. Siete habilidades: `recall`, `update`, `temporal`,
`multi_hop`, `aggregate`, `abstain` y `forget`. Tres condiciones: `ninguna`
(piso), `contexto-completo` (baseline tonto) y `memoria` (el sistema a probar).
Datos y preguntas en inglés; documentación en español.

Limitaciones (del README): lenguaje sintético y de plantillas, un solo dominio,
el aislamiento entre fases depende de quien opera, `abstain` y `forget` se
aprueban sin memoria (un sistema que no guarda nada saca 28.6 % macro), y los
agentes no son deterministas (hay que usar al menos 3 semillas).

## Experimentos que propongo (ninguno corrido)

Los tres del YAML usan solo Claude Code y los baselines de memprobe. Todos son
preguntas contestables midiendo, con el comando `python3 -m memprobe comparar`.

1. **Agente real contra el piso.** Calibra memprobe: si `contexto-completo` no
   supera a `ninguna`, el problema es el benchmark o el procedimiento, no la
   memoria.
2. **`CLAUDE.md` a mano.** Contrasta la hipótesis 3 del README.
3. **Pista prose contra code.** Mismos hechos, distinta escritura.

Posibles pruebas futuras, **no propuestas todavía** (hipótesis del README, y
sistemas de `LECTURAS.md` que no he investigado ni instalado): un
`resumen-jerarquico` como OptMem podría perder precisión en `recall` y
`aggregate`; una memoria `vectorial` como MemPalace podría recuperar el hecho
viejo en `update`/`temporal`; un `grafo` podría ir bien en `multi_hop` y mal en
`forget`. Mem0, Letta y Graphiti llaman a un LLM por dentro; habría que ver si
corren con un modelo local.

## Preguntas y dudas

- ¿Se acepta un benchmark propio junto a LongMemEval y LoCoMo?
- ¿Cómo medimos el costo en suscripción de cada kit?
- Falta decidir si memprobe necesita paráfrasis para no ser resoluble por
  reglas (la mejora que el README considera más valiosa).
