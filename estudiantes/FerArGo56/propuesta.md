---
# Copia este archivo a estudiantes/<tu-login>/propuesta.md.
#
# PARTE ESTÁNDAR (este bloque): igual para todos. Con ella juntamos las
# propuestas, acordamos qué hacemos y repartimos el trabajo. Llena todo lo que
# puedas; si no sabes algo, pon "no-se". Usa los ids de AGENTS.md cuando
# encajen; si no, escribe el nombre como tú lo llames.
#
# PARTE LIBRE (debajo del bloque): escribe como quieras.

login: "FerArGo56"
harnesses: [antigravity]
suscripciones: ["Anthropic (suscripción)"]
sistema_operativo: "macos"

# Una entrada por memoria que investigaste.
memorias:
  - id: "ninguna"
    tipo: [ninguna]
    fuente: ""
    sin_api_key: si
    facilidad: facil
    interes: 3

  - id: "claude-md-manual"
    tipo: [archivo-instrucciones]
    fuente: ""
    sin_api_key: si
    facilidad: facil
    interes: 2

  - id: "optmem"
    tipo: [notas, resumen-jerarquico]
    fuente: "https://github.com/VictorTaelin/OptMem"
    sin_api_key: si
    facilidad: facil
    interes: 3

  - id: "memo"
    tipo: [resumen-jerarquico]
    fuente: "https://github.com/arunv3rma/MeMo"
    sin_api_key: no-se   # MeMo (Memory as a Model) / condensación; configurable con modelo local Ollama
    facilidad: media
    interes: 3

  - id: "rag-local"
    tipo: [vectorial]
    fuente: "https://docs.trychroma.com/"   # ChromaDB / FAISS + embeddings locales (sentence-transformers)
    sin_api_key: si
    facilidad: facil
    interes: 3

  - id: "mempalace"
    tipo: [vectorial]
    fuente: "https://github.com/MemPalace/mempalace"
    sin_api_key: si   # Usa ChromaDB local por defecto
    facilidad: media
    interes: 2

  - id: "mem0"
    tipo: [vectorial, grafo]
    fuente: "https://github.com/mem0ai/mem0"
    sin_api_key: no-se   # Por defecto usa API key; sin verificar si funciona con Ollama
    facilidad: dificil
    interes: 2

  - id: "letta"
    tipo: [resumen-jerarquico, vectorial]
    fuente: "https://github.com/letta-ai/letta"
    sin_api_key: no-se   # Por defecto usa API key; sin verificar si funciona con Ollama
    facilidad: dificil
    interes: 2

  - id: "nativa-antigravity"
    tipo: [nativa]
    fuente: ""
    sin_api_key: si
    facilidad: facil
    interes: 2

# Una entrada por benchmark que investigaste o que propones.
benchmarks:
  - id: "longmemeval"
    mide: "recuerdo en conversaciones largas (extracción, razonamiento temporal, actualización, abstención)"
    fuente: "https://github.com/xiaowu0162/LongMemEval"
    calificacion: automatica
    casos: "500"
    cabe_en_suscripcion: no-se
    interes: 2

  - id: "locomo"
    mide: "memoria en conversaciones muy largas entre varias sesiones"
    fuente: "https://github.com/snap-research/locomo"
    calificacion: automatica
    casos: no-se
    cabe_en_suscripcion: no-se
    interes: 1

  - id: "propio-membench"
    mide: "recuperación de hechos técnicos sembrados en sesiones de programación, medida por distancia en turnos (Distance Decay)"
    fuente: "propio"
    calificacion: automatica   # Exact Match + F1 como base; LLM-juez local opcional
    casos: "~200 probes sobre 50 conversaciones sintéticas"
    cabe_en_suscripcion: si
    interes: 3

# Una entrada por experimento que propones.
experimentos:
  - pregunta: "¿Un sistema RAG local (rag-local con ChromaDB) recuerda mejor que el baseline sin memoria (ninguna) en sesiones de programación de 15–25 turnos, especialmente a distancias ≥ 7 turnos?"
    memorias: [ninguna, rag-local]
    harnesses: [antigravity]
    benchmark: "propio-membench"
    por_que_interesa: "Es la comparación mínima útil: saber si añadir recuperación vectorial local aporta algo real frente a no tener memoria. Es el primer paso antes de comparar sistemas más complejos."

  - pregunta: "¿Los sistemas basados en resumen/condensación (optmem / memo) tienen menor hallucination rate que el vectorial (rag-local) en la categoría de hechos contradictorios (F-CONT)?"
    memorias: [rag-local, memo, optmem]
    harnesses: [antigravity]
    benchmark: "propio-membench"
    por_que_interesa: "La hipótesis es que condensar y jerarquizar en lugar de recuperar fragmentos crudos por similitud reduce las alucinaciones cuando hay dos versiones contradictorias del mismo hecho."

  - pregunta: "¿El sistema rag-local mantiene el hecho actualizado (F-UPD) mejor que un archivo de instrucciones estático (claude-md-manual) cuando el usuario cambia una preferencia a mitad de sesión?"
    memorias: [claude-md-manual, rag-local]
    harnesses: [antigravity]
    benchmark: "propio-membench"
    por_que_interesa: "El archivo de instrucciones es estático y no se actualiza solo durante la conversación. Si el RAG local lo supera en F-UPD, justifica la complejidad de mantener un almacén dinámico."

roles: [armar-benchmark, motor-comun, analisis-y-graficas]
quiero_encargarme_de:
  - "diseño del dataset sintético de propio-membench (plantillas YAML + generador)"
  - "interfaz MemoryAdapter agnóstica (Python Protocol) para enchufar cualquier sistema"
  - "script de evaluación standalone sin framework"
disponibilidad: media
---

# Propuesta de FerArGo56

## Mi scouting

Mi punto de partida fue investigar **qué hace que un sistema de memoria sea efectivo en sesiones de programación**: un entorno interactivo donde el desarrollador define reglas de estilo, pide código que luego reutiliza, actualiza preferencias o introduce restricciones. Los benchmarks existentes (LongMemEval y LoCoMo) evalúan principalmente historias conversacionales cotidianas o de dominio general, dejando fuera la especificidad de flujos de código.

El detalle técnico del scouting está en `scouting/diseno-membench.md`. El trabajo se desarrolló mediante una sesión de diseño estructurado en Antigravity, definiendo las dimensiones de evaluación, distancias de degradación y métricas deterministas sin requerir API keys de pago.

El análisis de `LECTURAS.md` (especialmente el caso de MemPalace y el 96.6 % atribuible al baseline de ChromaDB) nos enseñó que cualquier métrica debe compararse contra un baseline honesto (`ninguna` y `claude-md-manual`) con pasos 100 % reproducibles.

## Lo que encontré

**Homologación de sistemas de memoria investigados:**

- **`optmem`** (Taelin): Tipo `[notas, resumen-jerarquico]`. Funciona como script local sin dependencias ni API key. Maneja un log de solo adición y árbol jerárquico. Fácil de desplegar, aunque las búsquedas por regex pueden ser frágiles ante variaciones semánticas.
- **`memo`** (Memory as a Model / Condensación): Tipo `[resumen-jerarquico]`. Modela el contexto mediante condensación o un modelo ligero dedicado. Prometedor para reducir ruido en sesiones largas.
- **`rag-local` / `mempalace`**: Tipo `[vectorial]`. Embeddings locales (p. ej. `nomic-embed-text` o `sentence-transformers` vía Ollama/ChromaDB). Totalmente reproducible y sin costos de API, ideal como benchmark de referencia vectorial.
- **`mem0` y `letta`**: Tipo `[vectorial, grafo]` y `[resumen-jerarquico, vectorial]`. Ofrecen características avanzadas de grafos y gestión autónoma, pero en su configuración estándar requieren API keys externas. Quedan categorizados con `sin_api_key: no-se` hasta verificar su viabilidad puramente local con Ollama.
- **`claude-md-manual`**: Tipo `[archivo-instrucciones]`. Baseline estático de instrucciones de inicio.
- **`ninguna`**: Tipo `[ninguna]`. Baseline frío (sin retención entre turnos fuera del prompt base).
- **`nativa-antigravity`**: Tipo `[nativa]`. Memoria interna del harness.

**Sobre benchmarks analizados:**
- `longmemeval`: 500 instancias de prueba enfocadas en razonamiento temporal y abstención. Relevante pero ajeno a programación.
- `locomo`: Conversaciones extensas multi-sesión; complejidad alta para pruebas bajo cuotas de suscripción.

## Experimentos que propongo

Se estructuran tres experimentos medibles con el benchmark propuesto (`propio-membench`):

1. **`ninguna` vs `rag-local`:** Evaluar si la memoria vectorial local aporta mejoras estadísticas medibles en la recuperación de hechos a distancias de 3, 7, 12 y 20 turnos frente a un agente sin memoria externa.
2. **`rag-local` vs `memo` / `optmem`:** Comparar el enfoque de búsqueda vectorial de fragmentos crudos contra la compresión y resumen jerárquico ante hechos contradictorios (`F-CONT`), evaluando la tasa de alucinación (Hallucination Rate).
3. **`claude-md-manual` vs `rag-local`:** Contrastar la memoria estática en archivo de instrucciones con una memoria vectorial dinámica ante cambios de requerimientos a mitad de sesión (`F-UPD`).

Para materializar esto, mis roles de interés son:
- Crear la especificación y generador del dataset sintético (50 escenarios, ~200 probes).
- Diseñar la interfaz `MemoryAdapter` en Python para desacoplar el benchmark de los sistemas evaluados.
- Construir el script evaluador con métricas estándar (EM, F1 y opcionalmente LLM-as-judge local).

## Preguntas y dudas

- **Estandarización de LLM-as-Judge:** Si el grupo decide utilizar LLM-as-Judge además de métricas exactas, ¿convendría fijar un modelo local específico (ej. Llama-3.1-8B vía Ollama) para que todos evaluemos bajo las mismas condiciones?
- **Soporte de mem0 / Letta sin API keys:** ¿Alguien en el equipo ha validado el rendimiento de mem0 o Letta usando únicamente backends locales como Ollama?
- **Criterio de verdad en hechos contradictorios (`F-CONT`):** Al actualizarse un hecho, ¿el benchmark debe considerar válida únicamente la versión más reciente, o evaluar explícitamente si el sistema detecta la discrepancia?
