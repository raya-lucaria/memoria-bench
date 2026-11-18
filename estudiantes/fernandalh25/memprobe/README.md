# memprobe

Benchmark de memoria para agentes que se **califica solo**: sin LLM juez, sin API keys, sin embeddings y sin red.
Pensado para `memoria-bench`: compara **sistemas de memoria** dentro de **harnesses** (Claude Code, Codex, Gemini CLI, Antigravity, ...) usando solo la suscripción que ya se tiene.

Solo usa la biblioteca estándar de Python (3.9 o más). El nombre `memprobe` es el id del benchmark: `propio-memprobe`.

## Estado: qué está verificado y qué no

- **Verificado (con pruebas automáticas en este repo):** la generación es determinista, cada pregunta se puede contestar solo con el flujo de eventos, la calificación es exacta, y un sistema de reglas con una habilidad rota falla justo en esa habilidad (tabla más abajo).
- **No verificado:** **nadie ha corrido memprobe con un harness real ni con un sistema de memoria real.** No hay ningún resultado de OptMem, MemPalace, `CLAUDE.md`, Claude Code, Codex, etc. Lo que se dice abajo de ellos son hipótesis, marcadas como tales.
- **No medido:** cuánto cuesta cada kit en la suscripción de cada harness. Solo hay estimaciones de tamaño (caracteres / 4).
- **Sin verificar:** cómo se desactiva la memoria nativa en cada harness, y si cada harness se puede manejar sin interfaz. Por eso el camino principal es manual y los comandos por harness no se afirman.

## Cómo encaja con las reglas de memoria-bench

| Regla del repo | Cómo la cumple memprobe |
|---|---|
| Nadie paga API keys | Generar y calificar no usan ningún modelo ni red (hay una prueba que lo comprueba). Todo corre en tu máquina; el agente usa tu suscripción. |
| Todo se puede repetir | Los datos salen de una semilla con un generador propio (no el `random` de Python). Cada kit lleva `dataset_id` y `kit_id`; si no coinciden, no se compara. Los ids dorados están fijados en `tests/pruebas.py`. |
| Todo número va contra un baseline tonto | Cada resultado se compara contra `ninguna` (piso) y `contexto-completo` con la misma semilla. El piso (siempre `UNKNOWN`) sale en el reporte sin correr ningún agente. |
| Distinguir lo verificado de lo que no | Esta sección y la de limitaciones. |
| Nada de datos personales | La tarjeta de corrida se rechaza si trae rutas personales, correos o llaves. Los reportes cambian el directorio personal por `~`. |

### Por qué no basta con LongMemEval

LongMemEval es una referencia importante, pero su calificación oficial usa un LLM como juez: su README indica `export OPENAI_API_KEY=...` y `python3 evaluate_qa.py gpt-4o ...` (https://github.com/xiaowu0162/LongMemEval). Eso choca con la regla 1. memprobe **no lo sustituye**: lo complementa con una calificación `automatica`, y mide otra cosa (mantener un estado que cambia: actualizar, olvidar, agregar) con historiales sintéticos en vez de chats naturales.

## Qué mide

Un flujo de eventos con fechas sobre entidades inventadas, mezclado con distractores, repartido en **sesiones**. Después, en una conversación nueva, se hacen preguntas. Siete habilidades, con el mismo número de preguntas cada una:

| Habilidad (id) | Ejemplo de pregunta | Qué detecta |
|---|---|---|
| `recall` | What is the current city of X? (dicho una vez) | Olvidar o descartar |
| `update` | La misma, tras varios cambios | Valores viejos, quedarse con el primero |
| `temporal` | What was the role of X at the end of day 12? | Guardar solo el valor más reciente |
| `multi_hop` | What is the city of the lead of X? | No poder encadenar dos hechos |
| `aggregate` | Which entities currently have team Y? / How many ...? | Buscar uno por uno sin poder agregar |
| `abstain` | Atributo nunca dicho; nombre casi igual que no existe; fecha anterior al primer dato | Alucinar, emparejar nombres por parecido |
| `forget` | Algo que se pidió olvidar | Ignorar los borrados |

Los nombres y valores son palabras inventadas (`Brakelor`, `Zarste`): el modelo no puede contestar con lo que ya sabe ni adivinando. Los distractores incluyen frases que mencionan algo sin afirmarlo ("Rumours that X would be linked to Y were denied", `# TODO maybe X.city = "Y"`) y nombres que difieren en una letra.

**Datos y preguntas están en inglés** (los ids de habilidad también); la documentación, el kit y los reportes están en español.

### Pistas

`prose` -> `Day 12: Brakelor relocated to Zarste.`
`code` -> `Brakelor.city = "Zarste"  # day 12` (también `set_attr(...)` y `config[...][...]`)
`mixed` -> al azar por evento.

`prose` y `code` de la misma semilla tienen **los mismos hechos y las mismas preguntas**; solo cambia cómo se escriben. La brecha entre las dos muestra si un sistema favorece un tipo de contenido.

## Cómo correrlo con un harness

```bash
python3 -m memprobe kit --tier chico --pista prose --seed 1 --salida corridas/chico-prose-1
# lee corridas/chico-prose-1/kit/LEEME.md: trae los pasos y los textos exactos que se pegan
```

El kit tiene `kit/fase-1-sesiones/` (una sesión por archivo), `kit/fase-2-preguntas/` (las preguntas y el formato de respuesta), `kit/referencia/` (el baseline de contexto completo) y `kit/LEEME.md`. **Fuera** de `kit/` quedan `gold.jsonl` (las respuestas correctas, que el agente no debe ver), `manifest.json` y `corrida-plantilla.json`.

| tamaño | sesiones x eventos | preguntas | fase 1 (est.) | fase 2 (est.) |
|---|---|---|---|---|
| `chico` | 8 x 35 | 42 | ~3.4k tokens | ~0.9k |
| `medio` | 12 x 50 | 70 | ~7.3k | ~1.4k |
| `grande` | 24 x 100 | 140 | ~29.8k | ~2.9k |

Son estimaciones de tamaño (caracteres / 4), **no de costo**. Contando conversaciones, `chico` son 8 (sesiones) + 1 (preguntas) por condición y semilla. `chico` se eligió porque con menos eventos algunas habilidades se quedaban sin suficientes preguntas (se comprobó con 50 semillas).

### Condiciones

| condición | qué es |
|---|---|
| `ninguna` | piso: conversación nueva, sin memoria, solo las preguntas |
| `contexto-completo` | baseline tonto: todo el historial y las preguntas en una sola conversación |
| `memoria` | el sistema que pruebas: las sesiones una por una (conversaciones nuevas, misma carpeta) y luego las preguntas en otra conversación nueva |

Las sesiones y las preguntas son siempre las mismas para todas las condiciones, con el mismo texto fijo.

### Puntuar y comparar

```bash
python3 -m memprobe revisar-respuestas --dir corridas/chico-prose-1 --respuestas respuestas.jsonl
python3 -m memprobe puntuar --dir corridas/chico-prose-1 --respuestas respuestas.jsonl \
    --corrida corrida.json --salida resultado.json
python3 -m memprobe comparar --a ninguna-*.json --b memoria-*.json
```

- **`corrida.json`** (se parte de `corrida-plantilla.json`): harness y versión, modelo que reporta el harness, tipo de suscripción, id y versión de la memoria (ids de `AGENTS.md`), condición, memoria nativa activada o no, aislamiento, repetición, fecha y sistema operativo. Lo que no sepas, `no-se`. Sin esto no se puntúa como corrida oficial (`--sin-corrida` calcula sin tarjeta y lo marca como no oficial).
- **`revisar-respuestas`** cuenta líneas inválidas, ids repetidos (gana el último), ids fuera de rango y preguntas sin respuesta. Nada se corrige en silencio: lo ilegible puntúa 0 y aparece en el reporte.
- **`comparar`** empareja por `dataset_id` (misma semilla y mismo kit), muestra la diferencia por semilla y por habilidad, y se niega a comparar si no hay datasets en común. Los agentes no son deterministas: usa **al menos 3 semillas** y repite.

### Cómo leer el reporte

- **Cifra principal: promedio macro de las siete habilidades** (cada una pesa igual), con un intervalo bootstrap **aproximado** que trata las preguntas como independientes. Con varias semillas, mira la diferencia por semilla.
- **Un sistema que no guarda nada saca 100 % en `abstain` y `forget`** (y 28.6 % macro). Por eso esas dos son solo dos séptimos del macro, y por eso siempre se imprimen la **tasa de alucinación** (respondió algo cuando debía ser `UNKNOWN`) y la de **falso `UNKNOWN`** (dijo `UNKNOWN` habiendo respuesta). Léelas juntas.
- **Por distancia al hecho necesario:** exactitud según qué tan atrás en el historial estaba lo que se necesitaba. Una caída con la distancia apunta a límites de capacidad o descarte, no a errores de razonamiento.

## Validación con un sistema de reglas

`examples/reference-sut.py` es una memoria de expresiones regulares y un diccionario. **No es un harness ni un agente**; sirve para validar el benchmark. Sin banderas saca 100 % en las tres pistas (cada pregunta se puede contestar solo con el flujo). Cada bandera rompe una conducta. Medido con `correr --suite estandar` (2000 eventos, 3 semillas), pista `prose` (la pista `code` dio los mismos números):

| Variante | recall | update | temporal | multi_hop | aggregate | abstain | forget | **macro** |
|---|---|---|---|---|---|---|---|---|
| referencia | 100 | 100 | 100 | 100 | 100 | 100 | 100 | **100** |
| `--window 500` (solo recuerda los últimos 500 eventos) | 80 | 70 | 22 | 67 | 75 | 100 | 100 | **73** |
| `--no-forget` | 100 | 100 | 100 | 100 | 89 | 100 | **0** | **84** |
| `--first-write-wins` | 100 | **0** | 45 | 23 | 31 | 100 | 100 | **57** |
| `--no-history` | 100 | 100 | **0** | 100 | 100 | 100 | 100 | **86** |
| `--fuzzy` (nombre más parecido) | 100 | 100 | 100 | 100 | 100 | **95** | 100 | **99** |
| `--guess` (nunca dice UNKNOWN) | 100 | 100 | 100 | 100 | 100 | **0** | **0** | **71** |
| siempre `UNKNOWN` (`null-sut.py`) | 0 | 0 | 0 | 0 | 0 | 100 | 100 | **29** |

Con `--window 500`, la exactitud por distancia al hecho es 100 % (<10 %), 100 % (10-25 %), 70 % (25-50 %) y 31 % (>50 %).
El sistema de reglas lee las plantillas exactas, así que **no dice nada sobre comprensión de lenguaje** (ver limitaciones). Las pruebas fijan estas firmas de fallo.

## Hipótesis sin verificar

Lo que sigue **no se ha medido**; es lo que memprobe permitiría contrastar:

- Una memoria `vectorial` podría recuperar el hecho viejo en vez del nuevo (`update`, `temporal`) y fallar en `aggregate`.
- Un `grafo` podría ir bien en `multi_hop` y peor en `forget` si no maneja borrados.
- Un `archivo-instrucciones` (`CLAUDE.md` a mano) podría ir bien con pocos datos y degradarse con el tamaño `grande`.
- Un `resumen-jerarquico` podría perder detalles precisos (`recall`, `aggregate`) a cambio de entrar en poco espacio.

## Limitaciones

- **Lenguaje sintético y de plantillas.** Un programa de reglas lo resuelve (el de referencia lo hace). Mide qué tan bien se conserva, actualiza, olvida y agrega información, no la comprensión abierta ni la robustez a paráfrasis. Agregar variedad de paráfrasis es la mejora más valiosa.
- **Un solo dominio:** hechos sobre entidades y atributos; sin narraciones, preferencias ni procedimientos.
- **El aislamiento entre fases depende de quien opera.** Nada impide que un agente vea archivos que se quedaron en la carpeta de trabajo; por eso la corrida declara `aislamiento`.
- **`abstain` y `forget` se aprueban sin memoria** (ver arriba).
- **Costo en la suscripción sin medir**, y no se sabe si Antigravity (que es un IDE) se puede manejar sin interfaz.
- Los agentes no son deterministas: una sola corrida no es evidencia.
- El flujo va en orden; no hay eventos atrasados, fuentes en conflicto ni historiales de meses.
- Los ids dorados se fijaron con una versión de Python; no se ha probado en otras plataformas.

## Camino secundario: un programa por stdin/stdout

Para CI, baselines de reglas, o cualquier sistema que se pueda manejar por línea de comandos (si tu harness lo permite, **sin verificar**):

```bash
python3 -m memprobe correr --sut "python3 examples/reference-sut.py" --suite humo
```

Protocolo (un JSON por línea, petición y respuesta, proceso nuevo por episodio):

```
-> {"op":"ingest","seq":0,"text":"Day 1: Brakelor relocated to Zarste."}   <- {"ok":true}
-> {"op":"query","seq":0,"q":"What is the current city of Brakelor?","format":"value"}   <- {"answer":"Zarste"}
```

`format` es `value` (texto), `list` (arreglo) o `count` (número). Se responde `"UNKNOWN"` cuando el historial no lo establece. stdout solo lleva líneas del protocolo. `examples/adapter-template.py` es la plantilla (completa `ingest` y `answer`); `null-sut.py` es el piso. Suites: `humo`, `estandar`, `estres`; en este camino las preguntas se hacen en cuatro puntos del flujo (40, 60, 80 y 100 %).

## Entrada para `propuesta.md`

Borrador de la entrada de `benchmarks:` (el campo `interes` y lo demás de la propuesta lo decide quien la escribe; `cabe_en_suscripcion` queda en `no-se` porque no se ha medido):

```yaml
  - id: propio-memprobe
    mide: "mantener un estado que cambia entre sesiones: recordar, actualizar, consultar por fecha, encadenar, agregar, abstenerse y olvidar"
    fuente: propio
    calificacion: automatica
    casos: 42          # por semilla en el tamaño chico (70 medio, 140 grande); se pueden generar más semillas
    cabe_en_suscripcion: no-se
    interes: 2
```

## Estructura

```
memprobe/generate.py     simulación del mundo, render prose/code, preguntas, dataset_id
memprobe/kit.py          escribe el kit para harnesses
memprobe/score.py        calificación exacta, resumen, piso
memprobe/respuestas.py   lectura estricta de respuestas.jsonl
memprobe/corrida.py      tarjeta de corrida y revisión de datos personales
memprobe/runner.py       camino secundario por stdin/stdout
memprobe/cli.py          kit | revisar-respuestas | puntuar | comparar | correr
examples/                reference-sut.py (con banderas), null-sut.py, adapter-template.py
tests/pruebas.py         python3 -m unittest discover -s tests -p pruebas.py
```

## Versiones

Cualquier cambio al generador o a la calificación cambia los `dataset_id`: sube `BENCH_VERSION` en `generate.py`, actualiza los ids dorados de `tests/pruebas.py` y no compares resultados entre versiones. Versión actual del benchmark: 0.2.

## Licencia

Sin elegir todavía; el repo `memoria-bench` decide la suya.
