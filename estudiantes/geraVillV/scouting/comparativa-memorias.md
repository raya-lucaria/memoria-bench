---
title: "Memoria para harnesses de agentes: investigación comparativa"
date: 2026-11-17
tags:
  - inteligencia-artificial
  - agentes
  - memoria
  - benchmarks
  - obsidian
status: investigación documental
---

# Memoria para harnesses de agentes: investigación comparativa

> [!summary] Conclusión ejecutiva
> No hay evidencia suficiente para declarar una memoria universalmente superior para OpenCode u otros harnesses. La mejor opción depende de si se priorizan notas editables, recuperación literal de conversaciones, automatización, razonamiento temporal o infraestructura mínima. Para un usuario que trabaja con Obsidian y varios agentes, **Open Second Brain** merece entrar en la primera ronda junto con una línea base de archivos y búsqueda. **MemPalace** es candidato para recuperar transcripciones originales; **Hindsight** y **OpenViking** son candidatos más complejos para recuperación estructurada; **OptMem** permite probar una arquitectura ligera. Estas son hipótesis para evaluar, no resultados de una prueba propia.

**Corte:** 17 de noviembre de 2026. **Alcance:** fuentes primarias abiertas, artículos, documentación y resultados publicados. No se instalaron sistemas ni se ejecutaron benchmarks para esta investigación. Los repositorios evolucionan: las características descritas corresponden a las páginas consultadas, no necesariamente a versiones anteriores. Las cifras publicadas por los fabricantes se atribuyen a ellos y no equivalen a una validación independiente.

## 1. Qué necesita recordar un harness

Un harness conecta un modelo con herramientas, archivos, ejecución y sesiones. La memoria es el mecanismo que selecciona información para utilizarla después de que una conversación se reinicia o se comprime. Conviene distinguir **qué se recuerda** de **cómo se almacena**.

| Tipo funcional | Ejemplo | Horizonte y riesgo |
|---|---|---|
| Trabajo | Objetivo actual, errores de una prueba, tareas pendientes | Corto; si se comprime puede perder restricciones. |
| Semántica | Preferencias, convenciones de proyecto, hechos vigentes | Largo; puede quedar obsoleta o confundirse entre proyectos. |
| Episódica | Una conversación, intento fallido o decisión con fecha | Largo; requiere localizar el episodio y conservar su contexto. |
| Procedimental | Un procedimiento validado, una skill o instrucciones de uso | Reutilizable; una instrucción incorrecta puede repetirse. |
| Estado y decisiones | Qué se decidió, alternativas rechazadas, vigencia y fuente | Cambiante; requiere distinguir versión actual de antecedentes. |

Un archivo Markdown, una búsqueda vectorial y un grafo no son tipos funcionales equivalentes: son **formas de implementar** una o varias memorias. La calidad depende de toda la cadena: captura, selección, almacenamiento, actualización, recuperación y aplicación a la tarea.

## 2. Lectura rápida de las alternativas

| Sistema | Organización y recuperación | Dónde vive y encaje | Principal fortaleza | Principal límite |
|---|---|---|---|---|
| **Archivos + búsqueda** | `AGENTS.md`, notas y búsqueda textual | Archivos locales, compatibles con distintos harnesses | Transparencia, control y línea base barata | Captura y recuperación dependen de convenciones e integración. |
| **OptMem** | Registro acumulativo, árbol de resúmenes y búsqueda regex | Python local; instrucciones en archivos del agente | Ligero; conserva el registro de notas | Depende de que el agente anote y sepa buscar; sin comparación sólida localizada. |
| **Hermes nativo** | Archivos curados siempre cargados y búsqueda FTS5 del historial | Integrado en Hermes | Preferencias frecuentes más acceso al historial | No es un proveedor genérico para otros harnesses; presupuesto de memoria limitado. |
| **MemPalace** | Texto original, embeddings, búsqueda híbrida y grafo opcional | Local; MCP; complementos de terceros | Conserva evidencia textual sin resumirla | Índice y dependencias; resultados principales son de recuperación, no de tareas. |
| **Open Second Brain** | Markdown en bóveda, SQLite reconstruible, búsqueda y reglas | Local; integración anunciada para OpenCode, Hermes y otros | Obsidian como fuente editable; corrección y reversión documentadas | Sistema amplio; no se identificó un benchmark público comparable para sus resultados de extremo a extremo. |
| **Obsidian Second Brain** | Notas enlazadas y skills para guardar, buscar y reescribir | Bóveda local; varios agentes | Gestión de conocimiento centrada en Obsidian | Es otro proyecto; no se identificó un benchmark comparable. La automatización varía por integración. |
| **Hindsight** | Hechos, experiencias, observaciones, índices híbridos y grafo | Autoalojado o servicio; integración para agentes | Búsqueda combinada y evidencia estructurada | LLM y componentes adicionales; complejidad y costos de ingesta. |
| **Mastra Observational Memory** | Observador y reflector condensan eventos fechados | Parte del framework Mastra | Contexto estable y observaciones cronológicas | La compresión puede perder detalles; no se verificó integración nativa con OpenCode. |
| **Mem0** | Hechos extraídos, recuperación híbrida y entidades | SDK autoalojable o plataforma administrada | API y opciones de despliegue | Las cifras de plataforma incluyen optimizaciones propietarias. |
| **Zep / Graphiti** | Episodios y grafo de entidades y relaciones bitemporales | Servicio Zep y motor Graphiti | Historial y vigencia de relaciones | Más infraestructura y extracción; los resultados históricos dependen de configuración. |
| **OpenViking** | Sistema de archivos virtual, jerarquía de resúmenes y búsqueda | Servicio local o alojado; plugin anunciado para OpenCode | Contexto navegable por proyecto y carga progresiva | Requiere servidor y modelos; la evaluación disponible es de sus autores. |
| **MemOS** | Memorias, grafo y recuperación híbrida; plugin local separado | Servicio, nube o plugins locales para otros agentes | Opciones locales y evaluación de tareas de agente | No extrapolar resultados del servicio al plugin local; integración OpenCode no verificada. |
| **MemGPT / Letta** | Contexto activo y almacenamiento externo administrados por el agente | Framework orientado a agentes con estado | Diseño explícito de memoria por niveles | Es una arquitectura de agente, no un simple reemplazo universal de memoria. |

Fuentes principales: [OptMem](https://github.com/VictorTaelin/OptMem), [Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/), [MemPalace](https://github.com/MemPalace/mempalace), [Open Second Brain](https://github.com/itechmeat/open-second-brain), [Obsidian Second Brain](https://github.com/eugeniughelbur/obsidian-second-brain), [Hindsight](https://github.com/vectorize-io/hindsight), [Mastra](https://mastra.ai/research/observational-memory), [Mem0](https://github.com/mem0ai/mem0), [Zep](https://arxiv.org/abs/2501.13956), [OpenViking](https://github.com/volcengine/OpenViking), [MemOS](https://github.com/MemTensor/MemOS) y [MemGPT](https://arxiv.org/abs/2310.08560).

## 3. Arquitecturas y diferencias prácticas

### 3.1 Archivos y búsqueda: la línea base indispensable

Un archivo con preferencias estables, otro con convenciones por proyecto y un historial buscable ya proporcionan memoria externa. Pueden versionarse y editarse sin una base de datos específica. Su principal problema es de operación: si nadie captura una decisión, si la información está bajo otro nombre o si se inyectan demasiadas notas, la memoria puede fallar aunque los archivos existan. Es la comparación mínima contra la cual deben medirse los sistemas especializados.

### 3.2 OptMem: registro y resúmenes jerárquicos

El [proyecto](https://github.com/VictorTaelin/OptMem) describe un script Python sin dependencias, un `LOG.txt` de notas acumulativas y un árbol de resúmenes reconstruible. `wake` presenta una selección, `recall` busca expresiones regulares en las notas y `zoom` permite navegar el árbol. Cada nota tiene un límite de 280 bytes. El modelo debe decidir qué registrar y generar los resúmenes solicitados: **conservar todas las notas no equivale a conservar toda la conversación**.

La cifra de 0.03 segundos para `wake` con un millón de recuerdos es una medición de velocidad declarada por el autor, no una medición de precisión ni de calidad de respuesta. No se localizó en el README un resultado comparable de LongMemEval o LoCoMo. No se identificó un archivo `LICENSE` en la ubicación consultada; verificar la licencia y condiciones directamente antes de reutilizar o redistribuir.

### 3.3 Hermes nativo: memoria siempre visible más archivo histórico

Según la [documentación oficial](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/), Hermes mantiene `MEMORY.md` con 2,200 caracteres y `USER.md` con 1,375 por defecto; los incorpora al inicio de la sesión. La búsqueda de sesiones utiliza SQLite FTS5 y devuelve mensajes históricos. Las actualizaciones de los archivos persistentes aparecen en la instantánea de la siguiente sesión, no automáticamente en el prompt de una sesión ya iniciada.

La solución es apropiada como comparación de una memoria pequeña y visible más historial consultable. La propia documentación advierte que afirmar «lo recordé» no demuestra que la herramienta haya escrito el dato. Hermes admite además proveedores externos: los resultados de uno de ellos no deben atribuirse a la memoria nativa de Hermes.

### 3.4 MemPalace: preservar las palabras originales

El [README](https://github.com/MemPalace/mempalace) describe almacenamiento textual literal, búsqueda semántica y organización por espacios y temas. El backend predeterminado es ChromaDB, con alternativas configurables. Dispone de MCP, herramientas para importar sesiones y opciones de embeddings locales. Su grafo temporal es una función adicional, no la explicación de todos los resultados publicados.

La principal ventaja conceptual es que la extracción de hechos no descarta el texto original. El intercambio es más material para indexar y filtrar: una coincidencia semántica puede recuperar la sesión correcta y aun así presentar demasiado ruido o no entregar al modelo todos los fragmentos necesarios. La integración con OpenCode aparece en proyectos de terceros; su funcionamiento y mantenimiento deben comprobarse en la versión elegida.

### 3.5 Los dos Second Brain para Obsidian

**[Open Second Brain](https://github.com/itechmeat/open-second-brain)**, de `itechmeat`, guarda memoria en Markdown bajo `Brain/` y mantiene un índice SQLite reconstruible. Documenta integración con OpenCode mediante plugin y MCP, y con Hermes mediante plugin y proveedor de memoria. Su proceso `dream` transforma señales en reglas de forma determinista, sin ejecutar un modelo dentro de ese algoritmo; otras funciones sí pueden depender del agente o de modelos opcionales. Documenta capturas de estado, rollback, búsqueda, correcciones, seguimiento de vigencia e importación de sesiones. Estas son características declaradas, no garantías evaluadas aquí. No se localizó una cifra pública comparable de precisión integral en las fuentes revisadas.

**[Obsidian Second Brain](https://github.com/eugeniughelbur/obsidian-second-brain)**, de `eugeniughelbur`, organiza notas enlazadas y ofrece comandos o skills para guardar conversaciones, ingerir fuentes, buscar y actualizar notas. Su documentación declara soporte para varios harnesses y recomienda la distribución basada en Agent Skills para OpenCode y Codex; el funcionamiento de funciones específicas, como hooks o tareas programadas, depende de la integración. Cuenta con una herramienta de evaluación de búsqueda sobre la propia bóveda, pero no se encontró en las fuentes consultadas un resultado público homogéneo frente a los otros sistemas.

**No se puede saber cuál de los dos era el Second Brain mencionado originalmente.** Ambos merecen evaluación separada. Una bóveda de notas propia no implica automáticamente que todas las llamadas a modelos sean locales: el proveedor elegido por el harness determina qué contenido sale del equipo.

### 3.6 Hindsight: hechos, episodios y relaciones

[Hindsight](https://github.com/vectorize-io/hindsight) distingue hechos, experiencias y observaciones, y combina búsqueda semántica, palabras clave, relaciones y tiempo. Su operación `retain` usa un modelo para extraer información; `recall` recupera y ordena; `reflect` ejecuta un análisis adicional. Admite despliegue propio y proveedores locales o remotos, con requisitos y resultados que dependen de la configuración.

La [integración anterior de OpenCode](https://hindsight.vectorize.io/sdks/integrations/opencode) figura como retirada y sustituida por el plugin unificado de coding agents; la documentación indica que el historial de la integración antigua no se importa automáticamente. La ventaja es la recuperación estructurada; los costos incluyen procesamiento de ingesta, mantenimiento y posibles llamadas a modelos. El artículo de sus autores describe resultados de respuesta, no simples porcentajes de recuperación.

### 3.7 Mastra: observaciones compactas en lugar de búsqueda dinámica

[Observational Memory](https://mastra.ai/research/observational-memory) usa un observador que transforma el historial en observaciones fechadas y un reflector que las reorganiza cuando crecen. El contexto reciente y el registro compacto se presentan al agente. Esto favorece un prefijo de prompt relativamente estable y la reutilización de caché entre cambios de observaciones; la reflexión puede reescribir ese prefijo. La contrapartida es que un dato omitido al condensar puede no estar disponible a menos que exista otra fuente recuperable. Mastra describe una implementación de framework y un experimento con un harness personalizado; no se verificó aquí un plugin listo para OpenCode.

### 3.8 Mem0, Zep, OpenViking y MemOS

**[Mem0](https://github.com/mem0ai/mem0)** combina extracción de hechos con búsquedas semánticas y léxicas. Ofrece SDK abierto y servicio administrado; el propio proyecto señala que los resultados recientes citados corresponden a la plataforma administrada e incluyen optimizaciones propietarias. No deben presentarse como resultados garantizados del SDK local.

**[Zep y Graphiti](https://arxiv.org/abs/2501.13956)** guardan episodios originales y construyen un grafo de entidades y relaciones. El esquema bitemporal distingue cuándo ocurrió o fue válido un hecho de cuándo fue registrado o invalidado en el sistema. Es útil para preguntas sobre cambios, aunque extracción y resolución de entidades pueden equivocarse. Graphiti es el motor; Zep es el servicio, por lo que no deben tratarse como el mismo producto.

**[OpenViking](https://github.com/volcengine/OpenViking)** estructura recursos, memorias y skills en un sistema virtual `viking://`, con resúmenes L0 y L1 y contenido detallado L2. Su documentación anuncia integración para OpenCode y Hermes y despliegue local o alojado, con un modelo de embeddings y un modelo de procesamiento. Una instalación local no implica necesariamente inferencia local. El proyecto declara AGPLv3 para su componente principal y licencias distintas para algunos componentes; revisar su archivo de licencia y condiciones de distribución.

**[MemOS](https://github.com/MemTensor/MemOS)** presenta un servicio con almacenamiento estructurado, opciones de nube y un plugin local separado para Hermes, OpenClaw y DeepSeek Harness. Su repositorio reporta pruebas tanto de recuperación como de tareas de agente; las cifras no identifican automáticamente el desempeño del plugin local en OpenCode. No se verificó una integración nativa de OpenCode en las fuentes revisadas.

**[MemGPT](https://arxiv.org/abs/2310.08560)** propuso administrar memoria como niveles semejantes a memoria principal y almacenamiento externo, con herramientas para mover información al contexto. El artículo original evalúa agentes con estado. Esta idea es relevante para diseñar harnesses, pero el estudio histórico no permite afirmar que la implementación actual de Letta supere a productos recientes en un uso concreto.

## 4. Qué mide cada benchmark

| Benchmark | Qué evalúa | Alcance y límites |
|---|---|---|
| **[LongMemEval](https://arxiv.org/abs/2410.10813)** | Extracción, varias sesiones, tiempo, cambios y abstención | 500 preguntas; versión S de aproximadamente 115,000 tokens y M de unas 500 sesiones. Conversaciones parcialmente simuladas. |
| **[LoCoMo](https://arxiv.org/abs/2402.17753)** | Preguntas sobre conversaciones, razonamiento temporal y relaciones | 50 conversaciones en el estudio, de unas 300 intervenciones de promedio; datos generados y editados por personas. La versión y el evaluador importan. |
| **[LongMemEval V2](https://github.com/xiaowu0162/LongMemEval-V2)** | Estado, pasos de trabajo, errores recurrentes y premisas incorrectas en trayectorias de agentes | 451 preguntas; hasta 500 trayectorias y 115 millones de tokens en los historiales más grandes. También mide latencia. Más cercano a agentes, pero no sustituye tareas propias de programación. |
| **[DMR](https://arxiv.org/abs/2310.08560)** | Recuperación de hechos de conversaciones previas | En el estudio de Zep, las conversaciones tienen unas 60 intervenciones; incluso la línea base de contexto completo obtiene resultados muy altos. |
| **[OmniMemEval](https://github.com/MemTensor/OmniMemEval)** | Dos rutas: memoria de usuario y agentes con plugins | Incluye LoCoMo, LongMemEval y dominios de tareas de agente. Desarrollado por MemTensor, creador de MemOS; revisar configuraciones y resultados por separado. |
| **[tau2-bench](https://blog.openviking.ai/post/openviking-benchmark-results/)** | Éxito de tareas de atención en dominios como comercio y aerolíneas | Más cercano a acciones de agente que un cuestionario de memoria; las cifras aquí provienen de OpenViking. |
| **[Terminal-Bench](https://github.com/laude-institute/terminal-bench)** | Tareas verificables en terminal | Puede servir como base de tareas para agentes, pero por sí solo no demuestra memoria entre sesiones: hay que diseñar la secuencia y conservar o aislar estado. |
| **[SWE-bench Verified](https://github.com/SWE-bench/SWE-bench)** | Resolver problemas reales de software con cambios verificables | 500 problemas revisados por ingenieros. Para medir memoria hace falta comparar el mismo agente con y sin memoria y con experiencias anteriores controladas. |
| **[LiveCodeBench](https://github.com/LiveCodeBench/LiveCodeBench)** | Implementación de soluciones de programación | En OmniMemEval se utiliza un subconjunto con experiencias previas y tareas de prueba; no mide por sí solo memoria entre sesiones. |

### Cómo interpretar las métricas

- **R@5 o R@10:** proporción de consultas para las que el material de evidencia aparece entre los primeros 5 o 10 resultados, según la definición del experimento. No es precisión de respuesta ni éxito de tarea. En preguntas con varias evidencias hay que revisar si se exige encontrar una, todas o un promedio.
- **Exactitud de respuesta:** porcentaje de respuestas juzgadas correctas. Depende del modelo que responde, del juez, del prompt, de categorías incluidas y del método de agregación.
- **Éxito de tarea:** proporción de tareas terminadas según verificadores. Depende además de herramientas, entorno y criterios de éxito.
- **Latencia y tokens:** deben medirse incluyendo ingesta, recuperación, generación y, cuando proceda, procesamiento en segundo plano. Un costo de consulta no incluye necesariamente el costo de indexar o sintetizar recuerdos.

Dos porcentajes no son comparables solo porque compartan el nombre del benchmark. Deben coincidir conjunto y versión, preguntas, modelo lector, juez, instrucciones, agregación, presupuesto de contexto, cantidad de resultados y protocolo de ingesta. Los modelos usados para extracción y reranking también forman parte de la configuración.

## 5. Resultados publicados, con contexto

| Sistema y fuente | Resultado y métrica declarada | Configuración y lectura correcta |
|---|---|---|
| [MemPalace](https://github.com/MemPalace/mempalace/blob/develop/benchmarks/BENCHMARKS.md) | **96.6 % R@5**, LongMemEval | Recuperación de sesiones originales, 500 preguntas según el proyecto, sin LLM en esta ruta. No mide respuestas correctas. |
| [MemPalace](https://github.com/MemPalace/mempalace/blob/develop/benchmarks/BENCHMARKS.md) | **88.9 % R@10**, LoCoMo | Recuperación híbrida en la configuración del proyecto, no exactitud de respuesta. |
| [Hindsight, artículo](https://arxiv.org/abs/2512.12818) | **91.4 %** LongMemEval y **hasta 89.61 %** LoCoMo | Exactitud de respuesta en configuraciones específicas de sus autores; requiere revisar modelo, juez y versión para comparar. |
| [Mastra OM](https://mastra.ai/research/observational-memory) | **94.87 %** LongMemEval S | GPT-5-mini como actor y Gemini 2.5 Flash para observación y reflexión; GPT-4o como juez; promedio no ponderado de seis categorías, según el autor. |
| [Mastra OM](https://mastra.ai/research/observational-memory) | **84.23 %** LongMemEval S | GPT-4o como actor; mismo observador declarado. La diferencia ilustra que el lector importa. |
| [Zep, artículo de 2025](https://arxiv.org/abs/2501.13956) | **71.2 %** LongMemEval S | GPT-4o como lector; contexto completo con el mismo lector: 60.2 %. Es una comparación histórica específica, no un dato del producto actual. |
| [Mem0](https://github.com/mem0ai/mem0) | **94.4** LongMemEval y **92.5** LoCoMo | Cifras del proveedor para la plataforma administrada, con optimizaciones no disponibles íntegramente en el SDK abierto; no se equiparan a otras configuraciones. |
| [OpenViking](https://blog.openviking.ai/post/openviking-benchmark-results/) | Hermes **33.38 % a 82.86 %** en LoCoMo | Comparación reportada por OpenViking entre su integración y memoria nativa, bajo su configuración; no prueba el mismo incremento en OpenCode. |
| [OpenViking](https://blog.openviking.ai/post/openviking-benchmark-results/) | Claude Code **57.21 % a 80.32 %** en LoCoMo | Comparación reportada por el proveedor; utiliza modelos de procesamiento e embeddings declarados en su repositorio. |
| [OpenViking](https://blog.openviking.ai/post/openviking-benchmark-results/) | tau2 comercio **70.94 % a 77.81 %**; aerolíneas **54.38 % a 66.25 %** | Éxito de tarea declarado por el proveedor para memoria de experiencia. Es más cercano al uso de agentes, pero no una prueba independiente ni de programación. |
| [MemOS](https://github.com/MemTensor/MemOS) | **36.63 % a 50.87 %** | Promedio de finalización de tareas de OpenClaw reportado por el proveedor en cinco tareas; consultar implementación y protocolo antes de extrapolar. |

### 5.1 Auditoría de afirmaciones de MemPalace

Su [documentación de benchmarks](https://github.com/MemPalace/mempalace/blob/develop/benchmarks/BENCHMARKS.md) es valiosa porque publica métodos y reconoce dos problemas: primero, la variante de **100 % R@5** incorporó ajustes basados en tres errores concretos del conjunto evaluado; segundo, el **100 % de LoCoMo a top 50** cubría todas las sesiones de cada conversación y, por tanto, no demuestra calidad de ordenación. Además, el documento presenta **98.4 % en 450 preguntas** como si fueran reservadas, pero describe ajustes desarrollados inspeccionando el conjunto completo antes de crear el corte de 50/450. Sin evidencia adicional sobre qué preguntas se consultaron durante cada etapa, no puede asumirse que ese conjunto fuera verdaderamente independiente de todo el desarrollo. La publicación contiene afirmaciones más fuertes que sus propias reservas permiten sostener.

### 5.2 La recuperación no es el resultado final

En el estudio original de [LongMemEval](https://arxiv.org/abs/2410.10813), fragmentar sesiones en turnos y enriquecer claves con hechos mejoró el desempeño en las configuraciones probadas; sustituir el original por resúmenes o hechos podía perder información. Incluso con evidencia correcta, el método de lectura afectó la respuesta hasta en 10 puntos absolutos en algunas comparaciones. En [LoCoMo](https://arxiv.org/abs/2402.17753), recuperar más fragmentos no siempre mejoró las respuestas: la relación entre cobertura y ruido depende del lector.

### 5.3 Un punto de control contra resultados inflados

El [artículo de Zep](https://arxiv.org/abs/2501.13956) reporta 94.8 % en DMR con GPT-4 Turbo frente a 94.4 % con toda la conversación; con GPT-4o-mini, 98.2 % frente a 98.0 %. El propio artículo observa que la conversación cabe en el contexto y que la tarea es limitada. Un número cercano a 100 % no prueba que una arquitectura compleja genere una ventaja práctica relevante.

### 5.4 Benchmarks específicos de código y memoria

La ruta de [memoria de agentes de OmniMemEval](https://github.com/MemTensor/OmniMemEval/blob/main/docs/agent_memory/README.md) es especialmente pertinente porque compara un harness con y sin plugins de memoria en tareas que incluyen SWE-bench y LiveCodeBench. En su protocolo de memoria, el agente recibe tareas previas y retroalimentación, se conserva una copia del estado de memoria y después se evalúa sobre tareas separadas. El conjunto usado contiene **101 tareas de preparación y 26 de prueba** para SWE-bench, y **97 de preparación y 39 de prueba** para LiveCodeBench. No debe confundirse esta muestra de 26 problemas con los 500 de SWE-bench Verified.

Los [resultados publicados por MemTensor](https://github.com/MemTensor/OmniMemEval/blob/main/docs/agent_memory/results.md), desarrollador de MemOS, presentan la siguiente comparación en el subconjunto SWE-bench:

| Harness | Sin plugin | Mem0 | Hindsight | MemOS |
|---|---:|---:|---:|---:|
| OpenClaw | 26.92 % | 26.92 % | 38.46 % | 38.46 % |
| Hermes | 37.18 % | 34.62 % | 28.20 % | 52.56 % |

Las cifras son el **promedio de la tasa de éxito de una ejecución en tres corridas independientes**, no pass@3. El estudio informa OpenClaw 2026.5.7, Hermes 0.18.0, MemOS Local Plugin 2.0.8, Qwen3.6 Flash sin razonamiento como modelo del agente y Qwen3.6 Flash con razonamiento como juez. La muestra es pequeña, no se documenta una prueba de significancia y la disponibilidad de servicios puede afectar los resultados. La configuración pública de feedback estructurado puede diferir entre plugins, por lo que debe revisarse antes de atribuir la diferencia exclusivamente a la arquitectura. El adaptador público actual cubre OpenClaw; la tabla de Hermes corresponde a una configuración histórica y no implica una ruta de reproducción pública actual para Hermes. Los resultados no miden OpenCode y no establecen un ganador universal.

La misma tabla reporta para **LiveCodeBench con OpenClaw** 51.28 % sin plugin, 60.68 % con Mem0, 71.79 % con Hindsight y 64.96 % con MemOS. Para **Hermes**, reporta 52.99 % sin plugin, 57.26 % con Mem0, 61.54 % con Hindsight y 64.10 % con MemOS. Son resultados del protocolo y la muestra de OmniMemEval, no resultados equivalentes al leaderboard completo de LiveCodeBench. El desempeño distinto de Hindsight en SWE-bench según el harness muestra por qué la integración y el entorno importan.

**Selección para una evaluación propia:** usar LongMemEval V2 para recordar procedimientos y errores de trayectorias previas, SWE-bench Verified para cambios verificables de código y Terminal-Bench para tareas de terminal. Comparar las memorias con idénticos modelo, herramientas y episodios previos, además de una línea base sin memoria. Añadir tareas propias entre sesiones para verificar recuperación de decisiones, correcciones posteriores y aislamiento de proyectos; registrar porcentaje resuelto, uso de información obsoleta, latencia y tokens. SWE-bench y Terminal-Bench, ejecutados de forma convencional, evalúan tareas de código o terminal y **no demuestran por sí solos memoria persistente**.

## 6. Comparación por necesidad

| Si la prioridad es... | Primeras opciones a evaluar | Razón y reserva |
|---|---|---|
| Leer y corregir información en Obsidian | Open Second Brain; Obsidian Second Brain; Markdown manual | Notas editables. Verificar escrituras automáticas, compatibilidad y control de cambios. |
| Encontrar conversaciones originales | MemPalace; historial buscable del harness | Preservan o consultan texto fuente. Probar identificación de la sesión y la evidencia exacta. |
| Componentes mínimos | Archivos + búsqueda; OptMem | Bajan complejidad operativa; requieren evaluar disciplina de captura y búsqueda. |
| Fechas, relaciones y cambios de estado | Hindsight; Zep/Graphiti; Open Second Brain | Modelan contexto y vigencia de manera más explícita; comparar errores de extracción y costo. |
| Contexto jerárquico de proyectos | OpenViking; Hindsight; Markdown por proyecto | Capacidad de seleccionar alcance; no hay ganador demostrado para un repositorio concreto. |
| Contexto compacto y estable | Hermes nativo; Mastra OM; OptMem | Diferentes políticas de compresión; hay que comprobar pérdida de detalles y cuándo se refresca el contexto. |
| Operación completamente local | Archivos, OptMem, MemPalace local, Open Second Brain | Verificar también embeddings y modelo del agente: almacenamiento local no basta para garantizar inferencia local. |

**Juicio provisional para un flujo OpenCode + Obsidian:** iniciar la comparación con archivos y búsqueda, Open Second Brain, MemPalace y OptMem. Agregar Hindsight y OpenViking si se necesita búsqueda estructurada de mayor complejidad y se acepta operar sus servicios. Incluir Hermes nativo en una prueba separada solo si también se evalúa Hermes como harness. Obsidian Second Brain debe incluirse si interesa una bóveda más orientada a investigación y síntesis, diferenciándolo de Open Second Brain.

## 7. Protocolo propuesto para una comparación justa

> [!important] Propuesta, no resultado
> Ninguna de estas pruebas se ha ejecutado. El propósito es comparar el valor incremental de la memoria en el flujo real, no optimizar para una tabla pública.

1. **Congelar el entorno:** misma versión de OpenCode, modelo, razonamiento, repositorios, herramientas, permisos y presupuesto por tarea. Registrar sistema, versión y configuración exactos de cada memoria. Usar un almacén limpio por ensayo.
2. **Construir una línea base:** memoria externa desactivada, con las instrucciones y archivos de proyecto normales. Comparar otra línea base de Markdown y búsqueda textual. No eliminar el contexto del proyecto que el agente normalmente necesita.
3. **Crear episodios de preparación equivalentes:** decisiones de arquitectura con justificación, errores corregidos, convenciones, preferencias en español y cambios posteriores. Cerrar las sesiones y crear una nueva antes de evaluar. Asegurar que todos los sistemas reciban los mismos eventos y anotar si requieren captura explícita o automática.
4. **Preparar preguntas y tareas reservadas:** repartir ejemplos por categoría sin ajustar el sistema a las respuestas de evaluación. Usar tareas adicionales no vistas después de cambiar prompts, índices o heurísticas. Conservar marcas temporales y fuentes de verdad.
5. **Medir recuperación:** proporción de evidencias correctas entre los resultados; si se requieren varias, medir cuántas se recuperaron. Registrar si el agente invocó la búsqueda y cuántos tokens recibió.
6. **Medir comportamiento:** cumplimiento de preferencias, elección de la decisión vigente, no repetición de un error conocido, abstención ante una premisa falsa y éxito de tareas verificables. Incluir correcciones contradictorias y aislamiento entre proyectos.
7. **Medir costos completos:** tiempo de configuración, ingesta inicial, procesamiento posterior, latencia de consulta, tokens del agente y de modelos auxiliares, costo monetario cuando corresponda y espacio en disco. Registrar fallas y procesos de fondo.
8. **Repetir y revisar:** usar varias corridas por tarea, reportar número de observaciones y variabilidad; revisar manualmente una muestra de respuestas y escrituras. Un juez automático puede equivocarse. Cuando sea posible, alternar el orden de evaluación.

Ejemplos concretos de casos: recordar por qué se descartó una biblioteca; recuperar el comando correcto después de cambiarlo; distinguir una preferencia personal de una restricción exclusiva de un repositorio; detectar que una instrucción antigua fue revocada; encontrar una explicación escrita en español a partir de una consulta en inglés; y rechazar que ocurrió una decisión que nunca existió. Para programación, pedir una modificación real sobre una copia reproducible y evaluarla con pruebas de aceptación, no solo con una respuesta textual.

## 8. Riesgos y criterios operativos

- **Información obsoleta:** un dato viejo puede ser recuperado con apariencia de certeza. Registrar fecha, alcance, procedencia y sustitución cuando existan.
- **Errores de extracción y resúmenes:** conservar acceso a la fuente original cuando sea posible; una nota automática es una interpretación, no necesariamente la conversación completa.
- **Separación entre proyectos:** etiquetar o aislar por usuario y repositorio, y probar explícitamente que una instrucción no se transfiera a otro contexto.
- **Datos sensibles y control:** almacenamiento local, inferencia local y sincronización son decisiones distintas. Revisar qué se indexa, qué se envía a proveedores y cómo borrar o exportar información.
- **Instrucciones maliciosas en recuerdos:** el contenido recuperado puede contener instrucciones de terceros. Una nota o resultado de búsqueda debe tratarse como evidencia, no como una regla que automáticamente prevalece sobre instrucciones del usuario.
- **Dependencia de proveedor y reversibilidad:** comprobar exportación, formato, migración, restauración de respaldos y mantenimiento del plugin. Documentar el costo de reconstruir índices.
- **Sobrecarga de contexto:** inyectar demasiadas notas aumenta tokens y ruido; medir calidad y costo en vez de asumir que más memoria siempre ayuda.

## 9. Límites de esta investigación

La revisión se basa mayormente en fuentes primarias de autores y proveedores, que conocen sus sistemas pero tienen incentivos para presentar buenos resultados. Los artículos académicos consultados no constituyen una prueba independiente de todos los productos aquí descritos. Algunas cifras provienen de versiones y fechas distintas; no se han armonizado ni reproducido. No se verificaron en ejecución la instalación, el consumo real, la privacidad efectiva ni la compatibilidad exacta de cada plugin. No se halló una evaluación homogénea publicada que incluya OptMem, los dos Second Brain, Hermes nativo, MemPalace, Hindsight y OpenViking en el mismo harness y con las mismas tareas. Ausencia de un resultado localizado no significa que no exista.

## 10. Fuentes principales

### Benchmarks y artículos

- Wu y colaboradores. [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813). Artículo y metodología original.
- Wu y colaboradores. [LongMemEval V2](https://github.com/xiaowu0162/LongMemEval-V2). Datos, evaluación y líneas base para trayectorias de agentes.
- Maharana y colaboradores. [Evaluating Very Long-Term Conversational Memory of LLM Agents](https://arxiv.org/abs/2402.17753). Diseño y resultados de LoCoMo.
- Latimer y colaboradores. [Hindsight is 20/20](https://arxiv.org/abs/2512.12818). Arquitectura y experimentos de Hindsight.
- Rasmussen y colaboradores. [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956). Arquitectura y evaluación histórica.
- Packer y colaboradores. [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560). Jerarquía de contexto y DMR.
- MemTensor. [OmniMemEval](https://github.com/MemTensor/OmniMemEval). Framework de evaluación publicado por el desarrollador de MemOS.
- MemTensor. [Resultados de Agent Memory](https://github.com/MemTensor/OmniMemEval/blob/main/docs/agent_memory/results.md) y [protocolo y tamaños de muestra](https://github.com/MemTensor/OmniMemEval/blob/main/docs/agent_memory/README.md).
- [SWE-bench](https://github.com/SWE-bench/SWE-bench), [LiveCodeBench](https://github.com/LiveCodeBench/LiveCodeBench) y [Terminal-Bench](https://github.com/laude-institute/terminal-bench). Benchmarks de programación y tareas de terminal.

### Documentación y resultados de productos

- [OptMem: repositorio](https://github.com/VictorTaelin/OptMem).
- [Hermes Agent: memoria persistente](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/).
- [MemPalace: repositorio](https://github.com/MemPalace/mempalace) y [metodología de benchmarks](https://github.com/MemPalace/mempalace/blob/develop/benchmarks/BENCHMARKS.md).
- [Open Second Brain](https://github.com/itechmeat/open-second-brain) y [Obsidian Second Brain](https://github.com/eugeniughelbur/obsidian-second-brain).
- [Hindsight: repositorio](https://github.com/vectorize-io/hindsight), [benchmarks](https://benchmarks.hindsight.vectorize.io/) e [integración anterior de OpenCode](https://hindsight.vectorize.io/sdks/integrations/opencode).
- [Mastra: Observational Memory](https://mastra.ai/research/observational-memory).
- [Mem0: repositorio](https://github.com/mem0ai/mem0).
- [OpenViking: repositorio](https://github.com/volcengine/OpenViking) y [reporte de benchmarks](https://blog.openviking.ai/post/openviking-benchmark-results/).
- [MemOS: repositorio](https://github.com/MemTensor/MemOS).

**Estado final de la evidencia:** comparación documental suficientemente amplia para seleccionar candidatos y diseñar una prueba, pero insuficiente para afirmar qué sistema es el mejor en el entorno del usuario sin ejecutar esa prueba.
