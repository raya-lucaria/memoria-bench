---
login: "RobertoUribeClemente"
harnesses: [claude-code, opencode]
suscripciones: ["Claude (plan de pago)", "OpenCode (modelos gratis)"]
sistema_operativo: "linux"

memorias:
  - id: nativa-claude-code
    tipo: [archivo-instrucciones, nativa]
    fuente: "https://code.claude.com/docs/en/memory"
    sin_api_key: si
    facilidad: facil
    interes: 2
  - id: nativa-gemini-cli
    tipo: [archivo-instrucciones, nativa]
    fuente: "https://geminicli.com/docs/tools/memory"
    sin_api_key: si
    facilidad: no-se
    interes: 2
  - id: second-brain-obsidian
    tipo: [notas]
    fuente: "https://www.mindstudio.ai/blog/ai-second-brain-claude-code-obsidian-architecture"
    sin_api_key: si
    facilidad: no-se
    interes: 2
  - id: optmem
    tipo: [notas, resumen-jerarquico]
    fuente: "https://raw.githubusercontent.com/VictorTaelin/OptMem/main/README.md"
    sin_api_key: si
    facilidad: no-se
    interes: 2
  - id: mempalace
    tipo: [vectorial]
    fuente: "https://vectorize.io/articles/mempalace-review"
    sin_api_key: si
    facilidad: no-se
    interes: 2
  - id: hermes-markdown
    tipo: [notas, nativa]
    fuente: "https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers"
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: hindsight
    tipo: [grafo]
    fuente: "https://hindsight.vectorize.io/blog/2026/04/06/hermes-native-memory-provider"
    sin_api_key: "no"
    facilidad: no-se
    interes: 2
  - id: honcho
    tipo: [vectorial]
    fuente: "https://honcho.dev/docs/v3/guides/integrations/hermes"
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: mem0
    tipo: [hechos-extraidos]
    fuente: "https://docs.mem0.ai/integrations/hermes"
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: supermemory
    tipo: [no-se]
    fuente: "https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers"
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: zep
    tipo: [no-se]
    fuente: "https://automem.ai/blog/agent-memory-in-2026-an-honest-comparison-of-mem0-zep-letta-and-the-rest"
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: claude-mem
    tipo: [no-se]
    fuente: "https://alternativeto.net/software/claude-mem/about"
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: bm25
    tipo: [logs-crudos]
    fuente: "propio: memory_bench/benchmarks/longmemeval/retrieve.py"
    sin_api_key: si
    facilidad: facil
    interes: 2
  - id: minilm
    tipo: [vectorial, logs-crudos]
    fuente: "https://github.com/qdrant/fastembed"
    sin_api_key: si
    facilidad: facil
    interes: 2
  - id: bge-small
    tipo: [vectorial, logs-crudos]
    fuente: "https://github.com/qdrant/fastembed"
    sin_api_key: si
    facilidad: facil
    interes: 3

benchmarks:
  - id: longmemeval
    mide: "Recordar hechos en historiales largos de varias sesiones, incluidos cambios, fechas y abstención"
    fuente: "https://github.com/xiaowu0162/LongMemEval"
    calificacion: llm-juez
    casos: 500
    cabe_en_suscripcion: no-se   # el piloto de 30 preguntas sí cupo; las 500 no se han probado
    interes: 3
  - id: locomo
    mide: "Responder preguntas sobre conversaciones muy largas"
    fuente: "https://mem0.ai/library/agent-memory/ai-memory-benchmarks-in-2026"
    calificacion: no-se
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: beam
    mide: "Memoria a gran escala"
    fuente: "https://mem0.ai/library/agent-memory/ai-memory-benchmarks-in-2026"
    calificacion: no-se
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: memoryagentbench
    mide: "Aprendizaje incremental de memoria a lo largo de varios turnos"
    fuente: "https://arxiv.org/html/2507.05257v3"
    calificacion: no-se
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2

experimentos:
  - pregunta: "Con la misma memoria recuperada, ¿cuántos puntos de exactitud separan a Sonnet de Haiku en LongMemEval-S, y esa diferencia es mayor que la que hay entre usar memoria y no usarla?"
    memorias: [ninguna, bge-small, oracle]   # oracle = se le dan las sesiones correctas (techo)
    harnesses: [claude-code]
    benchmark: longmemeval
    por_que_interesa: "En mi piloto, Haiku bajó de 90 % a 70 % con memoria recuperada y Sonnet solo de 90 % a 86.7 %. Si el lector pesa tanto, comparar memorias sin fijar el modelo puede engañar."

roles: [armar-benchmark]
quiero_encargarme_de: ["ampliar mi runner de LongMemEval para este experimento"]
disponibilidad: media
---

# Propuesta de RobertoUribeClemente

## Mi scouting

Investigué cómo recuerdan las cosas los harnesses de programación entre sesiones:
la memoria nativa de Claude Code y Gemini CLI, el patrón de "second brain",
OptMem, MemPalace y los proveedores de memoria de Hermes Agent. También revisé
qué tan creíbles son los números que publica cada proyecto.

- Guía completa, con fuentes: [`scouting/memorias_harness.html`](scouting/memorias_harness.html)
- Código y resultados del piloto: [`memory_bench/`](memory_bench/)

Las opiniones de Reddit de la guía son de segunda mano: no pude consultar los
hilos directamente, así que vienen de artículos que los citan.

## Lo que encontré

**Los números de los proveedores no se pueden comparar directamente.** Unos reportan
recall (si el pasaje correcto apareció) y otros exactitud juzgada (si la respuesta
fue correcta), con modelos y jueces distintos. Según las fuentes de mi guía, Mem0
pasa de 94.4 % declarado a 56.0 % en un harness independiente, y el 96.6 % de
MemPalace es recall@5, no exactitud de respuesta. No reproduje esas cifras.

**Corrí un piloto propio** con LongMemEval-S: 30 preguntas, semilla 42, top 5 de
sesiones, y Claude Sonnet como juez fijo.

| Lector | Sesiones correctas (oracle) | Memoria recuperada (bge-small) |
|---|---|---|
| Claude Haiku | 90.0 % ± 10.7 | 70.0 % ± 16.4 |
| Claude Sonnet | 90.0 % ± 10.7 | 86.7 % ± 12.2 |
| DeepSeek V4.1 Flash (OpenCode) | 86.7 % ± 12.2 | incompleto: 2 de 30 |

En recuperación (29 preguntas, sin contar la de abstención), la evidencia completa
quedó en el top 5 en 82.8 % de los casos con BM25 y en 89.7 % con MiniLM y con
bge-small.

**De lo que desconfío en mi propio piloto:**

- Son 30 preguntas, una semilla y una sola corrida, así que los intervalos son amplios.
- El juez es Sonnet, de la misma familia que dos lectores, y puede favorecerlos.
- Los modelos gratis de OpenCode dejaron de responder a medio camino, así que no sirven
  como banco de pruebas confiable.
- Los resultados por pregunta (`results/raw/`) no están en este PR; sí está el resumen
  en `results/summary.json`.

## Experimentos que propongo

**¿Pesa más el modelo lector o la memoria?** Es una hipótesis, **sin verificar**: la
memoria recuperada le cuesta más a un lector débil que a uno fuerte.

Diseño:

- Lectores: Haiku y Sonnet, ambos en Claude Code.
- Condiciones: sin memoria (`ninguna`, baseline que hay que agregar al runner),
  `bge-small` top 5 y `oracle`.
- Muestra: empezar con 60 preguntas (10 por tipo) y subir a 180 (30 por tipo) si alcanza
  la cuota. Con 180 serían 1,080 respuestas y 1,080 juicios. No sé si eso cabe en una
  suscripción.
- Mismas preguntas para todos, para poder comparar por pares.
- Revisar a mano una muestra de los juicios, para detectar sesgo del juez.

Sabríamos que salió bien si podemos reportar, con intervalo de 95 % por pares, la
diferencia Sonnet − Haiku con memoria recuperada y la pérdida `oracle` − `bge-small`
de cada modelo. La hipótesis se sostiene si la pérdida de Haiku es claramente mayor que
la de Sonnet. Si los intervalos se traslapan, el resultado honesto es que no alcanza
para concluirlo.

## Preguntas y dudas

- ¿Cuántas corridas caben en las suscripciones del grupo? ¿Conviene repartir las preguntas?
- ¿Usamos un segundo juez de otra familia? Con mis accesos solo tengo Claude y modelos
  gratis poco estables.
- En el piloto, Haiku respondió "no sé" en varias preguntas de preferencias aunque tenía
  las sesiones relevantes. ¿Conviene probar otra instrucción, o eso rompe la comparación
  con el prompt oficial?
