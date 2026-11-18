---
login: "goldzweigarie-bit"
harnesses: [claude-code]
suscripciones: ["Claude (plan: no-se)"]
sistema_operativo: macos

memorias:
  - id: ninguna
    tipo: [ninguna]
    fuente: "baseline"
    sin_api_key: si
    facilidad: facil
    interes: 3
  - id: claude-md-manual
    tipo: [archivo-instrucciones]
    fuente: "https://www.mariozechner.at/posts/2025-11-30-pi-coding-agent/"   # Pi usa AGENTS.md como contexto de proyecto
    sin_api_key: si
    facilidad: facil
    interes: 3
  - id: hermes-sesiones
    tipo: [logs-crudos, resumen-jerarquico]   # sesiones en SQLite+FTS5, compactación en sesiones hijas
    fuente: "https://arize.com/blog/how-hermes-implements-open-source-agent-harness-architecture/"
    sin_api_key: no-se
    facilidad: no-se
    interes: 2
  - id: prime-continual-harness
    tipo: [notas]               # sin verificar: el agente edita su propio harness (CRUD)
    fuente: "https://primeintellect.ai/blog/prime-agent"
    sin_api_key: no-se
    facilidad: no-se
    interes: 2

benchmarks:
  - id: propio-relevo
    mide: "si lo que el agente aprendió trabajando en la sesión 1 le sirve en una sesión 2 nueva (extracción, actualización, abstención)"
    fuente: "propio"
    calificacion: automatica
    casos: 12
    cabe_en_suscripcion: no-se
    interes: 3
  - id: propio-concubench
    mide: "no mide memoria del agente: mide si el agente reduce el uso de RAM de un programa (infra reutilizable para propio-relevo)"
    fuente: "propio"
    calificacion: automatica
    casos: 3
    cabe_en_suscripcion: si
    interes: 2

experimentos:
  - pregunta: "En propio-relevo, ¿qué fracción de la brecha entre ninguna y el oráculo (hechos escritos a mano en CLAUDE.md) cierra un CLAUDE.md que el propio agente actualiza al terminar la sesión 1?"
    memorias: [ninguna, claude-md-manual]
    harnesses: [claude-code]
    benchmark: propio-relevo
    por_que_interesa: "Es la memoria más barata que existe. Si cierra casi toda la brecha, las memorias complejas tienen que justificar su costo contra ella."
  - pregunta: "¿La ganancia de una misma memoria es igual en dos harnesses distintos, o depende del harness?"
    memorias: [ninguna, claude-md-manual]
    harnesses: [claude-code, nerv-harness]   # nerv-harness = mi harness propio, con modelo local (Ollama) para no usar API key
    benchmark: propio-relevo
    por_que_interesa: "Si cambia mucho entre harnesses, un número de memoria reportado sin decir el harness no significa nada."
  - pregunta: "Cuando un hecho cambia entre la sesión 1a y la 1b, ¿la memoria hace que el agente use el valor nuevo, o se queda con el viejo?"
    memorias: [ninguna, claude-md-manual, no-se]
    harnesses: [claude-code]
    benchmark: propio-relevo
    por_que_interesa: "Es la habilidad de actualización de LongMemEval, pero calificada con pruebas y no con un LLM juez."

roles: [motor-comun, armar-benchmark, integrar-harness]
quiero_encargarme_de: ["motor común: contenedores, semillas y baselines null/oráculo validados en CI", "armar propio-relevo"]
disponibilidad: media
---

# Propuesta de goldzweigarie-bit

## Mi scouting

- [`scouting/harness-handoff.md`](scouting/harness-handoff.md): notas de
  cuando investigué cuatro harnesses de referencia (Pi, mini-SWE-agent, Hermes
  Agent y Prime Agent) para construir uno propio. Para este proyecto lo
  relevante es cómo guarda memoria cada uno: Pi usa `AGENTS.md`, Hermes usa
  sesiones en SQLite con búsqueda FTS5 y compactación, y Prime deja que el agente
  edite su propio harness. Lo único que cambié fue quitar mi nombre.
- [`prototipos/concubench/`](prototipos/concubench/): el prototipo de un motor
  de benchmark que no depende del harness ni del modelo y no usa API keys.
  Mide RAM y no memoria del agente, pero la plomería es justo la que necesita
  `propio-relevo`. La única corrida real es la de sus agentes de referencia
  (ver abajo). Con agentes reales todavía no se ha corrido nada.

## Lo que encontré

Del motor (`concubench`) salió esto, y creo que sirve para memoria-bench:

1. **El benchmark no llama a ningún modelo.** Prepara un contenedor, le pasa un
   prompt a un adaptador (`run.sh <contenedor> <prompt>`) y califica cómo quedó
   el directorio de trabajo con pruebas deterministas. Así, cualquier harness
   entra escribiendo un adaptador, y el modelo es asunto del harness y de su
   suscripción.
2. **El benchmark se valida a sí mismo, antes de medir a nadie**, con tres
   agentes que no usan modelo. `null` no hace nada y debe sacar 0 %. `naive`
   aplica un arreglo plausible pero equivocado y debe fallar. `oracle` aplica la
   solución de referencia y debe sacar 100 %. Esto es la lección de MemPalace
   llevada al benchmark: si la tarea pasa con `null`, el número no mide nada.
3. **Las pruebas y los datos esperados nunca están en el contenedor del
   agente**, y se generan con una semilla nueva en cada intento.

Verificado en una máquina Linux con Docker (log en
[`prototipos/concubench-validacion.txt`](prototipos/concubench-validacion.txt)):
en las 3 tareas, `null` y `naive` fallan por OOM y `oracle` pasa 2/2, con un pico
de 18 / 89 / 19 MB contra límites de 96 / 600 / 96 MB. En macOS no está
probado: sin verificar.

## Experimentos que propongo

### `propio-relevo`: memoria que se gana trabajando

LongMemEval y LoCoMo miden si el agente recuerda **una conversación**. Lo que
más me interesa es otra cosa: si recuerda lo que **aprendió haciendo** una
tarea, como una restricción del entorno, una convención del proyecto o un
arreglo que funcionó, cuando abre una sesión nueva sobre otra tarea.

**Un caso tiene dos sesiones**, cada una en un workspace distinto. Lo único que
pasa de la sesión 1 a la 2 es el almacén de memoria (`/memory`, o el
`CLAUDE.md`, o la carpeta de la memoria nativa):

- **Sesión 1 (aprender):** el agente resuelve una tarea y en el camino se topa
  con hechos que no están en el prompt. Por ejemplo, el entorno de producción
  solo tiene 96 MB, el CSV viene en latin-1, las salidas van con `sort_keys` o
  la herramienta `peakmem` existe.
- **Sesión 2 (usar):** otra tarea, que solo sale a la primera si se acuerda de
  esos hechos. El prompt dice "mismo entorno que la vez pasada" y no los
  repite.
- Hay variantes para tres habilidades de LongMemEval:
  - **actualización:** una sesión 1b cambia un hecho y la sesión 2 debe usar el
    valor nuevo;
  - **abstención:** la sesión 2 pregunta algo que nunca se dijo y debe
    responder `null` en un `answers.json`;
  - **extracción:** el caso base de arriba.

**Calificación sin LLM juez:** pruebas sobre lo que deja la sesión 2 (archivos,
JSON, que el programa corra con el límite), con el mismo motor de
`concubench`.

**Baselines obligatorios en cada corrida:**

| memoria | qué es | para qué |
|---|---|---|
| `ninguna` | almacén vacío | piso |
| oráculo | los hechos correctos escritos a mano en `CLAUDE.md` | techo |
| memoria de otro caso | el almacén de un caso distinto | detecta ganancias que vienen de "calentar" al agente y no de recordar |

El número que se reporta es la **fracción de la brecha que se cierra**:
`(memoria − ninguna) / (oráculo − ninguna)`. Así se compara entre harnesses,
aunque cada modelo tenga un piso distinto.

**Tamaño:** 12 casos × 2 sesiones × (2 baselines + 2 memorias) = 96 sesiones
cortas por harness. Si cabe en la cuota de una suscripción está sin verificar;
lo primero sería medir cuánto consume una sesión.

**Harnesses en modo headless**, sin API key y con la sesión de la suscripción:
`claude -p`, `codex exec` y `gemini -p`. Sin verificar: hay que revisar las
banderas exactas con `--help` de cada versión.

### Cómo sabríamos si salió bien

- `validate` en CI: con `ninguna` y con la memoria de otro caso se falla la
  sesión 2, y con el oráculo se pasa. Si no, el caso se tira.
- Tres corridas por combinación (pass^3). Un resultado que cambia entre
  corridas se reporta como inestable y no como número.

## Preguntas y dudas

- Para correr el harness dentro de un contenedor hay que montar la sesión de la
  suscripción (por ejemplo `~/.claude`). ¿Lo permiten los términos de cada
  suscripción en uso automatizado? Sin verificar.
- La memoria nativa de cada harness guarda cosas fuera del workspace. Hay que
  ubicarla bien para poder vaciarla entre casos; si no, se contamina.
- Mem0 y Letta llaman a un LLM por dentro. Correrlas con Ollama cambia lo que se
  está midiendo.
