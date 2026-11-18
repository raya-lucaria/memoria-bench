---
login: geraVillV
harnesses: []
suscripciones: ["ChatGPT, suscripción de entrada; nombre exacto no confirmado"]
sistema_operativo: linux

memorias:
  - id: optmem
    tipo: [notas, resumen-jerarquico]
    fuente: https://github.com/VictorTaelin/OptMem
    sin_api_key: si
    facilidad: no-se
    interes: 2
  - id: mempalace
    tipo: [vectorial, logs-crudos, grafo]
    fuente: https://github.com/MemPalace/mempalace
    sin_api_key: si
    facilidad: no-se
    interes: 3
  - id: nativa-hermes
    tipo: [nativa, notas, logs-crudos]
    fuente: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: open-second-brain
    tipo: [notas, logs-crudos, vectorial]
    fuente: https://github.com/itechmeat/open-second-brain
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: obsidian-second-brain
    tipo: [notas, vectorial]
    fuente: https://github.com/eugeniughelbur/obsidian-second-brain
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: hindsight
    tipo: [vectorial, grafo, notas]
    fuente: https://github.com/vectorize-io/hindsight
    sin_api_key: si
    facilidad: no-se
    interes: 2
  - id: mastra-observational-memory
    tipo: [notas, resumen-jerarquico]
    fuente: https://mastra.ai/research/observational-memory
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: mem0
    tipo: [vectorial, grafo]
    fuente: https://github.com/mem0ai/mem0
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: graphiti
    tipo: [grafo, logs-crudos]
    fuente: https://github.com/getzep/graphiti
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: openviking
    tipo: [notas, resumen-jerarquico, vectorial]
    fuente: https://github.com/volcengine/OpenViking
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: memos
    tipo: [vectorial, grafo]
    fuente: https://github.com/MemTensor/MemOS
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: letta
    tipo: [resumen-jerarquico, vectorial]
    fuente: https://github.com/letta-ai/letta
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: archivo-instrucciones-manual
    tipo: [archivo-instrucciones]
    fuente: https://github.com/raya-lucaria/memoria-bench/blob/main/AGENTS.md
    sin_api_key: si
    facilidad: no-se
    interes: 2

benchmarks:
  - id: longmemeval
    mide: Recuerdo, actualización, tiempo y abstención en conversaciones.
    fuente: https://github.com/xiaowu0162/LongMemEval
    calificacion: llm-juez
    casos: 500
    cabe_en_suscripcion: no-se
    interes: 3
  - id: locomo
    mide: Recuerdo y razonamiento temporal entre sesiones de conversación.
    fuente: https://github.com/snap-research/locomo
    calificacion: automatica
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: longmemeval-v2
    mide: Conocimiento de procedimientos, cambios de estado y errores de agentes.
    fuente: https://github.com/xiaowu0162/LongMemEval-V2
    calificacion: llm-juez
    casos: 451
    cabe_en_suscripcion: no-se
    interes: 2
  - id: dmr
    mide: Recuperación de hechos de conversaciones anteriores.
    fuente: https://arxiv.org/abs/2310.08560
    calificacion: llm-juez
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: omnimemeval
    mide: Memoria de usuario y transferencia a tareas de agentes.
    fuente: https://github.com/MemTensor/OmniMemEval
    calificacion: no-se
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 3
  - id: tau2-bench
    mide: Éxito en tareas de agentes con experiencia previa.
    fuente: https://github.com/sierra-research/tau2-bench
    calificacion: no-se
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: terminal-bench
    mide: Ejecución de tareas verificables en terminal.
    fuente: https://github.com/laude-institute/terminal-bench
    calificacion: automatica
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: swe-bench-verified
    mide: Resolución verificable de incidencias reales de código.
    fuente: https://github.com/SWE-bench/SWE-bench
    calificacion: automatica
    casos: 500
    cabe_en_suscripcion: no-se
    interes: 3
  - id: livecodebench
    mide: Implementación de soluciones de programación con pruebas.
    fuente: https://github.com/LiveCodeBench/LiveCodeBench
    calificacion: automatica
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: sdebench
    mide: Tareas de repositorios y correcciones del usuario con memoria.
    fuente: https://agentmemorybenchmark.ai/dataset/sdebench
    calificacion: no-se
    casos: 61
    cabe_en_suscripcion: no-se
    interes: 2
  - id: convomem
    mide: Recuperación de información en conversaciones.
    fuente: https://github.com/MemPalace/mempalace/blob/develop/benchmarks/BENCHMARKS.md
    calificacion: automatica
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 2
  - id: membench
    mide: Recuperación de hechos y manejo de información distractora.
    fuente: https://github.com/MemPalace/mempalace/blob/develop/benchmarks/BENCHMARKS.md
    calificacion: automatica
    casos: 8500
    cabe_en_suscripcion: no-se
    interes: 2

experimentos:
  - pregunta: "¿MemPalace recupera más evidencia que OptMem y la búsqueda textual de archivos en LongMemEval con el mismo conjunto de consultas?"
    memorias: [mempalace, optmem, archivo-instrucciones-manual, ninguna]
    harnesses: [codex, opencode]
    benchmark: longmemeval
    por_que_interesa: Comparar recuperación y consumo sin atribuir la contribución de ChromaDB a la organización de MemPalace.
  - pregunta: "¿Una memoria compartida mejora la resolución de incidencias de código frente a no usar memoria en el mismo harness?"
    memorias: [mempalace, hindsight, ninguna]
    harnesses: [codex, opencode]
    benchmark: swe-bench-verified
    por_que_interesa: Relacionar el recuerdo de decisiones previas con cambios de código verificables.
  - pregunta: "¿MemPalace, OptMem y Open Second Brain conservan recuerdos utilizables al cambiar de modelo o harness frente a comenzar sin memoria?"
    memorias: [mempalace, optmem, open-second-brain, ninguna]
    harnesses: [codex, opencode]
    benchmark: longmemeval
    por_que_interesa: Evaluar portabilidad entre modelos y herramientas sin API keys.

roles: []
quiero_encargarme_de: []
disponibilidad: media
---

# Propuesta de geraVillV

## Mi scouting

Investigué memorias para agentes, benchmarks de lenguaje natural y código, compatibilidad con distintos harnesses, uso de modelos y embeddings locales y costo de contexto. La investigación original está en [scouting/comparativa-memorias.md](scouting/comparativa-memorias.md). Su fecha de corte es el 17 de noviembre de 2026. No he ejecutado benchmarks ni probado personalmente los sistemas: todos los resultados citados son de terceros.

Me interesa una memoria que sea agnóstica al modelo y al harness, no requiera API keys y consuma pocos tokens. He señalado MemPalace con interés alto por su recuperación local y evidencia pública, no como ganadora demostrada. Los intereses medios de las demás entradas son provisionales, no una preferencia confirmada individualmente.

## Lo que encontré

MemPalace publica 96.6 % R@5 en LongMemEval con embeddings locales; es recuperación de sesiones, no porcentaje de respuestas correctas. Un análisis independiente atribuye principalmente ese resultado al texto literal y a los embeddings predeterminados de ChromaDB, no a la metáfora de palacio: https://arxiv.org/abs/2604.21284. Por eso el baseline de búsqueda simple es importante. El propio proyecto reconoce que un 100 % posterior se ajustó a errores observados y que su antiguo 100 % de LoCoMo con top 50 cubría todas las sesiones: https://github.com/MemPalace/mempalace/blob/develop/benchmarks/BENCHMARKS.md.

OptMem utiliza notas y resúmenes jerárquicos; no encontré resultados comparables que permitan clasificarlo frente a MemPalace. Open Second Brain y Obsidian Second Brain son proyectos distintos. Hindsight admite modelos locales y, según su documentación, algunos accesos por suscripción, pero puede llamar a un modelo auxiliar para procesar recuerdos: https://hindsight.vectorize.io/developer/models. La viabilidad sin API key depende de la configuración concreta, no únicamente del nombre del sistema. Las fuentes de cada entrada figuran en el bloque estándar y en el scouting.

## Experimentos que propongo

Las preguntas del bloque estándar son propuestas para discusión, no pruebas ejecutadas ni un compromiso de que yo las realice. Se compararía cada memoria con sus baselines usando el mismo harness, modelo, datos y presupuesto, y se medirían recuperación de evidencia, resolución de tareas, latencia y consumo total de tokens, incluyendo procesamiento auxiliar. El uso de SWE-bench convencional no demuestra memoria entre sesiones por sí solo; habría que definir cómo se proporcionan experiencias previas. La comparación entre modelos debe conservar los mismos recuerdos sin depender de un modelo concreto. Usar embeddings locales y, donde haga falta un modelo de lenguaje, una suscripción disponible o ejecución local sin API keys. La calificación automática de recuperación o las pruebas de código evitan un LLM juez cuando sea posible; cualquier cambio a un juez local debe declararse y no asumirse equivalente al oficial.

## Preguntas y dudas

- Nombre exacto de la suscripción de entrada de ChatGPT y disponibilidad de Codex: no confirmados. La lista de harnesses disponibles por suscripción se deja vacía hasta confirmarlo; `opencode` y `codex` en los experimentos son candidatos, no herramientas cuya suscripción se haya acreditado.
- Disponibilidad declarada: media. Roles y encargos: sin decidir; no se asume que vaya a ejecutar pruebas.
- Facilidad de instalación, consumo real de tokens y compatibilidad exacta entre memorias y harnesses: sin verificar personalmente.
- El tamaño y costo final del conjunto de casos deben acordarse para que quepa en la suscripción; no se afirma que los benchmarks completos quepan.
