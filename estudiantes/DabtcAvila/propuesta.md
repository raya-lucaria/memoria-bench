---
# Copia este archivo a estudiantes/<tu-login>/propuesta.md.
#
# PARTE ESTÁNDAR (este bloque): igual para todos. Con ella juntamos las
# propuestas, acordamos qué hacemos y repartimos el trabajo. Llena todo lo que
# puedas; si no sabes algo, pon "no-se". Usa los ids de AGENTS.md cuando
# encajen; si no, escribe el nombre como tú lo llames.
#
# PARTE LIBRE (debajo del bloque): escribe como quieras.

login: "DabtcAvila"
harnesses: [claude-code]
suscripciones: ["Claude (suscripción)"]
sistema_operativo: "macos"

# Una entrada por memoria que investigaste.
memorias:
  - id: "ninguna"
    tipo: [ninguna]
    fuente: ""
    sin_api_key: si
    facilidad: facil
    interes: 3            # es el baseline de todo

  - id: "claude-md-manual"
    tipo: [archivo-instrucciones]
    fuente: "https://code.claude.com/docs/en/memory"
    sin_api_key: si
    facilidad: facil
    interes: 3

  - id: "nativa-claude-code"
    tipo: [nativa, notas]
    fuente: "https://code.claude.com/docs/en/memory"
    sin_api_key: si
    facilidad: facil      # viene activada; es la que uso a diario
    interes: 3

  - id: "optmem"
    tipo: [notas, resumen-jerarquico]
    fuente: "https://github.com/VictorTaelin/OptMem"
    sin_api_key: si       # un script sin dependencias; el propio agente resume. Sin verificar instalándolo
    facilidad: no-se
    interes: 3

  - id: "llm-wiki"
    tipo: [notas]
    fuente: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
    sin_api_key: si       # es un patrón de archivos markdown, no un producto
    facilidad: no-se
    interes: 2

  - id: "logs-crudos-grep"
    tipo: [logs-crudos]
    fuente: "https://arxiv.org/abs/2610.29823"   # MemoryTax: harness + historial en un archivo
    sin_api_key: si
    facilidad: facil
    interes: 3

  - id: "bm25"
    tipo: [logs-crudos]   # búsqueda léxica sobre texto crudo; baseline "tonto" de recuperación
    fuente: "https://arxiv.org/html/2507.05257v3"
    sin_api_key: si
    facilidad: no-se
    interes: 2

  - id: "mempalace"
    tipo: [vectorial]
    fuente: "https://github.com/MemPalace/mempalace"
    sin_api_key: no-se    # ChromaDB local por defecto; sin verificar
    facilidad: no-se
    interes: 2

  - id: "mem0"
    tipo: [vectorial, grafo]
    fuente: "https://github.com/mem0ai/mem0"
    sin_api_key: "no"     # extrae con un LLM; API key por defecto. Sin verificar con Ollama
    facilidad: no-se
    interes: 1

  - id: "letta"
    tipo: [notas, nativa]  # desde feb-2026 su memoria son archivos markdown en git (MemFS)
    fuente: "https://www.letta.com/blog/context-repositories"
    sin_api_key: no-se
    facilidad: no-se
    interes: 1

  - id: "graphiti"
    tipo: [grafo]
    fuente: "https://github.com/getzep/graphiti"
    sin_api_key: no-se    # construir el grafo usa un LLM; sin verificar con modelo local
    facilidad: no-se
    interes: 1

  - id: "hindsight"
    tipo: [grafo, vectorial]
    fuente: "https://github.com/vectorize-io/hindsight"
    sin_api_key: no-se
    facilidad: no-se
    interes: 1

  - id: "mastra-memoria-observacional"
    tipo: [resumen-jerarquico]   # un observador convierte mensajes en observaciones fechadas; solo texto
    fuente: "https://mastra.ai/research/observational-memory"
    sin_api_key: no-se
    facilidad: no-se
    interes: 1

  - id: "claude-mem"
    tipo: [logs-crudos, vectorial]   # hooks que capturan todo + observador que resume
    fuente: "https://github.com/thedotmack/claude-mem"
    sin_api_key: no-se
    facilidad: no-se
    interes: 1

# Una entrada por benchmark que investigaste o que propones.
benchmarks:
  - id: "longmemeval"
    mide: "recuerdo en historiales de chat largos: extracción, entre sesiones, temporal, actualización y abstención"
    fuente: "https://github.com/xiaowu0162/LongMemEval"
    calificacion: llm-juez
    casos: "500"
    cabe_en_suscripcion: no-se   # unos 115 mil tokens de historial por pregunta
    interes: 2

  - id: "locomo"
    mide: "preguntas sobre conversaciones largas entre dos personas (un dato, varios datos, temporal)"
    fuente: "https://github.com/snap-research/locomo"
    calificacion: llm-juez       # el artículo usa F1; los vendedores usan juez. 6.4 % de la clave está mal
    casos: "1540 útiles; una sola conversación = 152"
    cabe_en_suscripcion: no-se   # una conversación (152 preguntas) probablemente sí; sin verificar
    interes: 2

  - id: "longmemeval-v2"
    mide: "memoria de la experiencia de un agente: estado, flujos de trabajo, trampas del entorno"
    fuente: "https://xiaowu0162.github.io/longmemeval-v2/"
    calificacion: no-se
    casos: "451"
    cabe_en_suscripcion: "no"    # historiales de 25 a 115 millones de tokens
    interes: 1

  - id: "beam"
    mide: "diez habilidades de memoria en historiales de 100 mil a 10 millones de tokens"
    fuente: "https://arxiv.org/html/2510.27246v1"
    calificacion: llm-juez
    casos: "2000 preguntas sobre 100 conversaciones"
    cabe_en_suscripcion: no-se
    interes: 1

  - id: "memoryagentbench"
    mide: "recuperar, aprender sobre la marcha, entender a largo plazo y olvidar lo que cambió"
    fuente: "https://arxiv.org/html/2507.05257v3"
    calificacion: automatica     # exactitud, F1 y recall según la tarea
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2

  - id: "swe-contextbench"
    mide: "si un agente de código reutiliza la experiencia de un problema anterior relacionado"
    fuente: "https://arxiv.org/html/2602.08316v3"
    calificacion: automatica     # pruebas ejecutables
    casos: "1100 base + 376 relacionadas; versión Lite = 99"
    cabe_en_suscripcion: no-se
    interes: 2

  - id: "vibemembench"
    mide: "si un sistema de memoria ayuda a resolver tareas reales de repositorio"
    fuente: "https://arxiv.org/html/2609.23570"
    calificacion: automatica
    casos: "111 tareas, 3634 trayectorias de historia"
    cabe_en_suscripcion: no-se
    interes: 2

  - id: "dreambench-swe"
    mide: "higiene de memoria: tareas que dependen de algo dicho en sesiones anteriores"
    fuente: "https://arxiv.org/abs/2608.20664"
    calificacion: automatica     # oráculos ejecutables ocultos
    casos: "180"
    cabe_en_suscripcion: no-se
    interes: 2

  - id: "capa"
    mide: "si el asistente deja de preguntar lo que el mismo usuario ya aclaró en sesiones pasadas"
    fuente: "https://arxiv.org/html/2607.26611"
    calificacion: automatica
    casos: "600 sesiones, 300 de evaluación"
    cabe_en_suscripcion: no-se
    interes: 2

  - id: "coremem-chainswe"
    mide: "cadenas de tareas de código donde lo aprendido en una sirve en la siguiente"
    fuente: "https://arxiv.org/abs/2611.17316"
    calificacion: automatica
    casos: "48 cadenas en el conjunto de prueba"
    cabe_en_suscripcion: no-se
    interes: 2

  - id: "memorytax"
    mide: "acierto y costo por pregunta de cada forma de memoria, con el mismo modelo"
    fuente: "https://arxiv.org/abs/2610.29823"
    calificacion: llm-juez
    casos: "152 (una conversación de LoCoMo)"
    cabe_en_suscripcion: no-se   # es el más chico de todos; candidato a replicar
    interes: 3

  - id: "propio-continuidad"
    mide: "si el agente puede continuar un trabajo usando un dato que solo está en su memoria, y cuánto le cuesta encontrarlo"
    fuente: "propio"
    calificacion: automatica     # un script compara con la respuesta correcta
    casos: "20 preguntas (10 dentro de un proyecto, 10 que cruzan proyectos)"
    cabe_en_suscripcion: si      # 180 corridas cortas; consumo sin verificar
    interes: 3

# Una entrada por experimento que propones: una pregunta que se pueda contestar midiendo.
experimentos:
  - pregunta: "¿La memoria que trae Claude Code contesta más preguntas sobre trabajo de sesiones pasadas que un CLAUDE.md escrito a mano o que no tener memoria?"
    memorias: [ninguna, claude-md-manual, nativa-claude-code]
    harnesses: [claude-code]
    benchmark: "propio-continuidad"
    por_que_interesa: "Viene incluida y no se instala nada. Si no le gana a un archivo a mano, lo demás sobra. En SCLATE (sep-2026) subió el acierto de 48.0 a 60.6 % sin gastar más tokens, pero con modelos anteriores."

  - pregunta: "¿Juntar la memoria de todos los proyectos en una sola contesta mejor las preguntas que cruzan proyectos que tener una memoria por proyecto?"
    memorias: [nativa-claude-code, claude-md-manual, llm-wiki]
    harnesses: [claude-code]
    benchmark: "propio-continuidad"
    por_que_interesa: "Cuatro de ocho harness guardan una sola memoria global; Claude Code guarda una por proyecto. En mi uso real, 7.7 % de las sesiones necesitó la memoria de otro proyecto. Falta medir si juntarlas mejora el acierto."

  - pregunta: "¿Buscar con grep en el historial completo acierta igual que OptMem y que BM25 en una conversación de LoCoMo?"
    memorias: [ninguna, logs-crudos-grep, bm25, optmem]
    harnesses: [claude-code, codex, gemini-cli]
    benchmark: "locomo"
    por_que_interesa: "Repite MemoryTax (oct-2026) solo con suscripción y agrega OptMem, que no tiene ninguna evaluación publicada. Ahí Claude Code con el historial en un archivo sacó 97 %, Mem0 95 % y BM25 90 %. Son 152 preguntas."

  - pregunta: "Con la misma memoria, ¿cuánto cambia el acierto si solo se cambia el modelo?"
    memorias: [ninguna, logs-crudos-grep]
    harnesses: [claude-code]
    benchmark: "locomo"
    por_que_interesa: "Si el modelo pesa más que la memoria, comparar memorias con modelos distintos no sirve. En MemoryTax, Claude Code fue de 29 % a 97 % según el modelo."

  - pregunta: "¿Un resumen corto de la sesión anterior sirve más que la transcripción completa para continuar una tarea de código?"
    memorias: [ninguna, logs-crudos-grep, nativa-claude-code]
    harnesses: [claude-code]
    benchmark: "propio-continuidad"
    por_que_interesa: "En SWE-ContextBench el resumen correcto subió el acierto de 26.3 a 34.3 %; la transcripción completa lo dejó en 27.3 %."

# Para repartir. Elige de la lista; puedes poner varios.
roles: [armar-benchmark, analisis-y-graficas]
quiero_encargarme_de: ["armar el benchmark propio-continuidad", "tablas y web de números", "medir el uso real con medir.py"]
disponibilidad: media
---

# Propuesta de DabtcAvila

## Mi scouting

Busqué qué benchmarks de memoria existen, qué puntaje saca cada sistema, quién
lo midió y qué hay con los modelos de hoy (17-nov-2026). Está tal cual en
[`scouting/`](scouting/):

| Archivo | Qué es |
|---|---|
| [`numeros.html`](scouting/numeros.html) | 492 cifras en una tabla con filtros. Se abre en el navegador |
| [`informes/`](scouting/informes/) | Los cinco reportes originales de la búsqueda, con el enlace de cada cifra |
| [`medir.py`](scouting/medir.py) | Script que mide cómo se usa la memoria de Claude Code. Solo lee archivos |
| [`medicion-uso-real-2026-11-17.json`](scouting/medicion-uso-real-2026-11-17.json) | Su resultado en mi máquina, con los proyectos sin nombre |

Nadie ha corrido ningún benchmark. Lo único que medí yo es el uso real de la
memoria en mi máquina; lo demás son cifras de otros.

## Lo que encontré

**Las cifras hay que comprobarlas.** La búsqueda las hizo una IA que leyó cada
página resumida. En los informes, `[P]` o `[V]` es «leído en la página» y `[S]`
es «solo visto en un resultado de búsqueda». Casi todos los puntajes los
reporta el propio vendedor.

**LoCoMo ya no sirve para comparar sistemas**
(<https://github.com/dial481/locomo-audit>):

- 99 de sus 1,540 respuestas correctas están mal.
- Su juez automático aceptó 63 % de respuestas falsas.
- Un modelo sin memoria, con toda la conversación a la vista, sacó 92.6 %.

**Cuando mide alguien sin producto que vender, lo simple empata o gana.**

| Estudio | Resultado |
|---|---|
| [MemoryAgentBench](https://arxiv.org/html/2507.05257v3), 2025 | Búsqueda por palabras 41.5, Mem0 21.1, Zep 24.0 |
| [VibeMemBench](https://arxiv.org/html/2609.23570), sep-2026 | En 11 de 12 pruebas, el agente con un producto de memoria resolvió menos que sin memoria |
| [MemoryTax](https://arxiv.org/abs/2610.29823), oct-2026, Opus 5.5 | Claude Code con el historial en un archivo 97 %, Mem0 95 %, Zep 87 % |
| [CoReMem](https://arxiv.org/abs/2611.17316), nov-2026, Opus 5.5 | Sin memoria 38.5 %, Mem0 39.6 %, historial completo 40.6 % |

**Cargar más texto fijo cuesta y no mejora.** Con un AGENTS.md generado, el
costo sube 20 a 23 % y el acierto cambia entre −2.0 y +2.4 puntos
(<https://arxiv.org/html/2602.11988>).

**El modelo pesa más que la memoria.** En MemoryTax, el mismo harness va de
29 % a 97 % solo por cambiar de modelo.

**Faltan datos con los modelos de hoy.** GPT-6.2 salió hoy y no tiene ninguna
medición de memoria. OptMem no tiene ninguna evaluación publicada.

**Mi uso real** (183 sesiones, del 15-oct al 17-nov-2026):

| Métrica | Valor |
|---|---|
| Sesiones que leyeron la memoria de otro proyecto | 14 de 183 (7.7 %) |
| Tamaño de un índice único con todas las memorias | 160 KB; Claude Code solo carga 25 KB |
| Texto cargado al abrir una sesión | 62,630 tokens (mediana) |
| Memorias que se abrieron al menos una vez | 330 de 605, como mínimo |

El script cuenta lo que el agente buscó. No cuenta lo que le faltó y no buscó.

**De qué desconfío:** del 73.3 % de FrontierMemory (lo publica Letta y gana su
producto), de los 98 % de vendedores nuevos, y de mis propias tablas hasta que
alguien repita las cifras desde la fuente.

## Experimentos que propongo

**Un benchmark propio, `propio-continuidad`.** Los públicos preguntan
«¿recuerdas el dato?». Este pregunta «¿puedes continuar el trabajo?».

- **Preguntas:** 20, con respuesta que solo está en la memoria. 10 dentro de un
  proyecto y 10 que cruzan proyectos, sobre proyectos inventados que cualquiera
  pueda descargar.
- **Calificación:** un script compara con la respuesta correcta. Sin juez
  automático.
- **Se mide:** aciertos, datos que faltaron, pasos hasta el primer dato
  correcto, tokens y tiempo.
- **Tamaño:** 180 corridas (20 preguntas × 3 formas de memoria × 3
  repeticiones).
- **Sirve para cualquier harness:** la memoria es una carpeta de texto.

**Cuándo gana una memoria:** si sube los aciertos más de 5 puntos sin cargar
20 % más de texto al abrir la sesión. Es mi propuesta; se ajusta al homologar.

**Por dónde empezar:** repetir MemoryTax con suscripción (experimento 3). Son
152 preguntas, compara harness entre sí y daría la primera cifra de OptMem. Yo
solo tengo Claude Code; Codex y Gemini CLI los tendría que correr alguien más.

## Preguntas y dudas

- ¿Cuántas corridas aguanta una suscripción antes del límite? No lo he medido.
- ¿Calificamos LoCoMo contra la clave ya corregida, sin juez automático?
- ¿Fijamos un modelo por harness para todo el grupo? Sin eso, las cifras no se
  pueden comparar.
- `medir.py` solo lee el formato de Claude Code. ¿Alguien adapta uno para Codex
  o Gemini CLI?
