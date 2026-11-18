# concubench

Es la infraestructura de un benchmark de agentes que **no depende del harness ni
del modelo** y **no usa API keys**. El benchmark nunca llama a un modelo. Arma
contenedores, le pasa un prompt a un adaptador y califica cómo quedó
`/workspace` con pruebas deterministas. No hay un LLM que haga de juez.

Por ahora trae 3 tareas de memoria RAM (categoría `memoria`). Están pensadas
como contenido de la materia de cómputo y concurrencia, y como base para
`propio-relevo` (ver `propuesta.md`).

## Requisitos

- Docker (Desktop en macOS, Engine en Linux)
- Python ≥ 3.11 en el host. Solo usa la stdlib; numpy va dentro de la imagen.

## Uso

```bash
make image                      # docker build -t concubench-base:latest images/base
make test                       # pruebas sin Docker (esquema + corrección a escala chica)
make validate                   # null = 0 %, naive falla como se espera, oracle = 100 %
python3 -m bench run --agent oracle --attempts 3
python3 -m bench run --agent adapters/<tu-harness> --attempts 3
python3 -m bench summary runs/<id>/results.jsonl
```

## Ciclo de un intento

| fase | contenedor | ve `/workspace` | qué hace |
|---|---|---|---|
| agent | A | sí, lectura/escritura | el adaptador actúa con `docker exec` |
| prepare | P | no | genera `/data` y `/expected` con una semilla nueva |
| grade | G (nuevo) | solo lectura | corre `tests/solve.sh` bajo la sonda; mide memoria, CPU y OOM |
| check | C | no | compara `/results` con `/expected` |

La solución nunca ve `/expected` ni las pruebas. Los datos se generan con una
semilla nueva en cada intento, así que no sirve escribir la respuesta a mano.

## Cómo se mide la memoria

- **Califica** el límite duro: `--memory = --memory-swap`. Morir por OOM es
  fallar. El kernel libera la page cache antes de matar al proceso, así que
  solo muere quien de verdad retiene memoria.
- **Se reporta, pero no califica**, el pico de memoria *no reclamable*: anónima
  más shmem (tmpfs y `/dev/shm` cuentan). La sonda (`bench/probe.py`) lo lee del
  cgroup cada 50 ms y funciona con cgroup v1 y v2.
- `ru_maxrss` no sirve para calificar: mide el hijo más grande y no la suma, así
  que repartir el trabajo en 8 procesos lo engaña.

## Agentes de referencia (validan al benchmark, no a un agente)

| agente | qué hace | debe sacar |
|---|---|---|
| `null` | nada | 0 % (si pasa, la prueba no detecta nada) |
| `naive` | aplica `naive/solve.sh`, un arreglo plausible pero mal hecho | falla con `expect.naive` (`oom`) |
| `oracle` | aplica `solution/solve.sh` | 100 % con pico ≤ 70 % del límite |

## Contrato del adaptador

```
adapters/<nombre>/run.sh <container> <prompt_file>
```

El adaptador actúa solo con `docker exec <container> …`. Recibe
`BENCH_CONTAINER`, `BENCH_PROMPT`, `BENCH_TIMEOUT`, `BENCH_ARTIFACTS` y hereda el
entorno, así que `OPENAI_BASE_URL` puede apuntar a Ollama o llama.cpp. Si
escribe `$BENCH_ARTIFACTS/meta.json` (`model`, `steps`, `tokens_in`,
`tokens_out`), esos datos salen en los resultados. Su código de salida no
cuenta: solo importa cómo queda `/workspace`. Hay una plantilla en
`adapters/TEMPLATE/`.

## Concurrencia del runner

Cada fase reserva la memoria y la CPU que declara su `task.toml` de un
presupuesto (75 % de la RAM del host). La admisión es FIFO estricta, sin
inanición, y los intentos más pesados van primero (LPT). `runs/<id>/run.json`
guarda el makespan y el pico reservado, que sirven para comparar este esquema
contra un semáforo por número de contenedores.

## Estructura de una tarea

```
tasks/<id>/
  task.toml          límites por fase y qué se espera de null/naive/oracle
  prompt.md          lo único que ve el agente
  workspace/         archivos iniciales
  tests/prepare.py   fase P
  tests/solve.sh     fase G: cómo se invoca la solución
  tests/check.py     fase C
  solution/solve.sh  oráculo
  naive/solve.sh     arreglo incorrecto conocido (opcional)
```
