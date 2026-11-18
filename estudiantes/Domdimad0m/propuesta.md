---
login: Domdimad0m
harnesses: []
modelos: []
suscripciones: "por confirmar"
sistema_operativo: "por confirmar"
memorias_probadas: []
benchmarks_usados: []
memorias_que_me_interesan:
  - second-brain
  - mempalace
  - claude-md-manual
  - mem0
benchmarks_que_propongo:
  - propio-handoff-portable
  - longmemeval
  - locomo
quiero_encargarme_de:
  - "Diseño de casos de transferencia de memoria entre sesiones y harnesses"
  - "Definición de métricas verificables sin LLM juez"
ids_nuevos:
  - second-brain
  - propio-handoff-portable
---

# Propuesta de Domdimad0m

## 1. Lo que hice

### Investigación preliminar y diseño de comparación (sin ejecución experimental)

- **Memoria:** `second-brain`, `mempalace`, `claude-md-manual`, `mem0` (candidatas; ninguna reportada como probada).
- **Harness y modelo:** no fijados; falta confirmar combinaciones compatibles y disponibles mediante suscripciones existentes.
- **Benchmark o tarea:** revisión conceptual de `longmemeval`, `locomo` y propuesta de `propio-handoff-portable`.
- **Qué hice:** investigué cómo comparar memorias persistentes, archivos de instrucciones y mecanismos de recuperación entre sesiones. Diseñé una pregunta experimental: si un agente puede recuperar decisiones relevantes y continuar una tarea interrumpida cuando cambia el harness o el modelo.
- **Qué salió:** **no medido**. No se han ejecutado benchmarks ni obtenido puntuaciones comparables.
- **Evidencia:** sin evidencia experimental. Este documento registra una propuesta, no resultados.
- **Cómo repetirlo:** revisar las fuentes de la sección 4; para reproducir resultados será necesario implementar el protocolo de la sección 2 y registrar versiones, configuración y salidas.
- **Qué salió mal o me sorprendió:** una buena puntuación de recuperación de información no demuestra por sí sola que una memoria permita continuar una tarea; además, algunos sistemas requieren componentes o modelos adicionales que pueden afectar coste y comparabilidad.

## 2. Lo que propongo

### Qué comparación quiero ver (memoria × harness × benchmark) y por qué me interesa

Comparar estas **condiciones de memoria**, no asumir que todas son productos intercambiables:

| ID | Condición | Qué se evaluaría | Precaución |
|---|---|---|---|
| `ninguna` | Sin memoria persistente | Línea base para estimar el beneficio de recordar | El repositorio y el enunciado siguen disponibles |
| `claude-md-manual` | Instrucciones y notas escritas manualmente | Persistencia, precisión y portabilidad de información explícita | `CLAUDE.md` es un formato asociado a Claude Code; otros harnesses necesitarán un adaptador equivalente |
| `second-brain` | Implementación de Second Brain por fijar | Organización, recuperación y transferencia de conocimiento | **Nombre ambiguo**: antes de ejecutar se debe elegir repositorio, versión y arquitectura concreta |
| `mempalace` | MemPalace | Recuperación de información y continuidad entre sesiones | Separar el efecto de MemPalace del motor de almacenamiento/búsqueda subyacente |
| `mem0` | Mem0 (opcional) | Extracción, actualización y recuperación de recuerdos | Verificar si se puede ejecutar sin pagar API keys, por ejemplo con componentes locales |

**Diseño agnóstico:** usar las mismas tareas, los mismos hechos disponibles, los mismos criterios de evaluación y un formato común de entrada/salida. Adaptar la interfaz a cada memoria sin dar a unas acceso privilegiado a información adicional. En una primera fase, fijar **un mismo harness y modelo** y variar solo la memoria. En una segunda fase, probar cambios de harness/modelo únicamente entre combinaciones compatibles.

**Benchmarks:** utilizar `longmemeval` y `locomo` como referencias para capacidades de recuerdo conversacional, y desarrollar `propio-handoff-portable` para medir transferencia de estado y continuación de trabajo. No comparar sus puntuaciones como si midieran exactamente lo mismo.

### Mi hipótesis

1. Una memoria persistente correctamente configurada superará a `ninguna` en tareas que exijan recordar decisiones de sesiones previas.
2. `claude-md-manual` puede resultar competitiva en tareas pequeñas con información explícita, por su simplicidad y facilidad de inspección.
3. Los sistemas de recuperación automática pueden mejorar el acceso a información distribuida, pero también introducir recuerdos irrelevantes, desactualizados o costes adicionales.
4. La mejor puntuación de recuerdo **no necesariamente** producirá la mejor tasa de continuación correcta después de cambiar de harness.

Son hipótesis **previas a la medición**, no conclusiones.

### Benchmark que propongo: `propio-handoff-portable`

**Qué mide:** si un agente nuevo puede recuperar información importante de sesiones anteriores y terminar una tarea sin contradecir decisiones previas. Se evalúan cuatro capacidades: recordar, actualizar, transferir y actuar.

**Casos propuestos:** 12 casos pequeños, distribuidos en cuatro categorías (3 por categoría):

1. **Recuerdo factual:** recuperar una restricción o decisión registrada anteriormente.
2. **Actualización:** reconocer que una decisión antigua fue sustituida por otra más reciente.
3. **Transferencia:** continuar desde un estado guardado sin acceso al historial privado del agente anterior.
4. **Acción verificable:** modificar un proyecto mínimo respetando requisitos previos y pasando pruebas automatizadas.

**Procedimiento por caso:**

1. Restaurar un proyecto y una secuencia de eventos idénticos para todas las condiciones.
2. Entregar los eventos al mecanismo de memoria siguiendo una interfaz documentada (`write`, `read`, `export` cuando esté disponible).
3. Reiniciar la sesión del agente; en los casos de transferencia, cambiar a otro harness compatible y proporcionarle solo el estado permitido.
4. Formular una consulta o una tarea con el mismo enunciado para todas las condiciones.
5. Calificar mediante respuestas estructuradas, archivos esperados, comparaciones exactas y tests automáticos; **no usar un LLM como juez**.
6. Guardar versión, configuración, logs saneados, tiempo, tokens cuando estén disponibles, resultados y errores.

**Calificación:**

- **Exactitud de recuerdo:** respuestas correctas / preguntas de recuerdo.
- **Actualización correcta:** casos que usan la versión vigente / casos de actualización.
- **Éxito de continuación:** tareas completadas con todos los tests / tareas intentadas.
- **Violaciones de restricciones:** número de decisiones críticas contradichas.
- **Coste y latencia:** tokens reportados por el harness y segundos de ejecución; declarar `no medido` cuando no se puedan obtener de forma comparable.
- **Portabilidad:** combinaciones compatibles de origen → destino completadas correctamente / combinaciones compatibles evaluadas.

**Controles:** incluir `ninguna` y `claude-md-manual`; mantener iguales enunciados, límites de tiempo, permisos y recursos. Registrar qué información está presente en el repositorio base para evitar atribuir a la memoria algo que el agente podía leer directamente. Ejecutar primero un piloto de **12 casos × 3 condiciones (`ninguna`, `claude-md-manual`, una memoria adicional) = 36 ejecuciones**, una vez cada una; después repetir los casos o ampliar condiciones si alcanza la cuota. Esta cifra es una **propuesta de presupuesto**, no un resultado.

**Reproducibilidad y suscripciones:** no comprar API keys. Priorizar herramientas ya disponibles por suscripción o componentes locales; si una memoria requiere un servicio de pago no disponible, registrarla como **no ejecutada** y no atribuirle una puntuación. Publicar datos sintéticos, tests, configuración y pasos para repetir; no publicar credenciales ni transcripciones privadas.

### De qué me quiero encargar

- Definir los 12 casos de `propio-handoff-portable`, sus respuestas esperadas y pruebas automáticas.
- Documentar la interfaz mínima de comparación para que las memorias reciban información equivalente.
- Preparar la plantilla de resultados con métricas y campos de reproducibilidad.
- Investigar y fijar la implementación concreta de `second-brain` antes de realizar pruebas.

## 3. Lo que no sé o me preocupa

- **Identidad de Second Brain:** hay proyectos distintos con ese nombre. Debemos fijar URL, commit y comportamiento antes de considerarlo un sistema evaluable.
- **Compatibilidad real:** una memoria integrada en un harness no necesariamente puede exportarse o importarse en otro. El experimento debe distinguir interoperabilidad nativa de adaptadores creados para la prueba.
- **Equidad:** comparar un archivo manual breve con una base de datos automática puede introducir diferencias de tamaño, preparación y coste. Se deben reportar esas diferencias.
- **Dependencias ocultas:** motores vectoriales, bases de datos, modelos de embeddings o servicios externos pueden explicar parte del resultado. Hay que registrar todos los componentes.
- **Presupuesto:** algunas configuraciones de Mem0 y otros sistemas usan llamadas a modelos; no se debe asumir que funcionarán dentro de una suscripción sin API key adicional.
- **Resultados reproducibles:** versiones, seeds, prompts, permisos y criterios de parada deben quedar registrados; una sola ejecución no demuestra superioridad estadística.
- **Alcance:** `longmemeval` y `locomo` miden aspectos de recuerdo, pero no sustituyen una prueba específica de continuidad de tareas.
- **Datos no confirmados:** harnesses utilizados, modelos, suscripciones y sistema operativo se dejan pendientes de confirmar antes de enviar el PR.

## 4. Fuentes

- Reglas y flujo de entrega: https://github.com/raya-lucaria/memoria-bench (consultado 2026-11-17).
- Plantilla de propuesta: https://github.com/raya-lucaria/memoria-bench/blob/main/plantillas/propuesta.md (consultado 2026-11-17).
- IDs y reglas de homologación: https://github.com/raya-lucaria/memoria-bench/blob/main/AGENTS.md (consultado 2026-11-17).
- MemPalace: https://github.com/MemPalace/mempalace (versión por fijar).
- Mem0: https://github.com/mem0ai/mem0 (versión por fijar).
- Claude Code, documentación de memoria: https://code.claude.com/docs/en/memory (versión por fijar).
- LongMemEval: https://github.com/xiaowu0162/LongMemEval (versión por fijar).
- LoCoMo: https://github.com/snap-research/locomo (versión por fijar).
- Second Brain: **implementación por confirmar**; no se atribuyen características técnicas a un proyecto sin identificar.
