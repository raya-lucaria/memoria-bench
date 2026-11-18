# Evidencia de Scouting: diseño de propio-membench

**Fecha:** 2026-11-17  
**Harness:** Antigravity (Google)  
**Modelo:** Claude Sonnet 4.6 Thinking / Gemini 3.8 Flash  

## Qué se hizo

Sesión de diseño estructurado mediante análisis y entrevista con el harness.
Se definieron los parámetros del benchmark propuesto `propio-membench`:
sistemas de memoria homologados a comparar, categorías de hechos sintéticos, protocolo de Distance Decay, métricas de evaluación deterministas e infraestructura local sin requerir API keys de pago.

## Decisiones de diseño

| Decisión | Valor seleccionado | Alternativas consideradas |
|---|---|---|
| **Horizonte temporal** | Medio plazo (sesión extendida, 15–25 turnos) | Corto plazo (< 5 turnos), inter-sesión largo |
| **Dominio de aplicación** | Sesión de desarrollo de software / programación | Conversación casual, roleplay |
| **Generador de datos** | Dataset sintético automático controlado | Registros reales sin anonimizar |
| **Distancias de evaluación** | {3, 7, 12, 20} turnos entre siembra y pregunta | Distancia aleatoria continua |
| **Métricas clave** | Exact Match (EM), Token F1, Hallucination Rate, Hit@k | Solo LLM-as-judge |
| **Escala piloto** | 50 conversaciones, ~200 probes | 500+ casos |
| **Infraestructura** | Embeddings locales (ChromaDB / sentence-transformers) + Ollama opcional | APIs comerciales pagadas |
| **Implementación** | Protocol Python agnóstico (MemoryAdapter) | Dependiente de LangChain / LlamaIndex |

## Sistemas de memoria homologados para comparación

| ID de Sistema | Tipo AGENTS.md | Descripción / Implementación |
|---|---|---|
| `ninguna` | `ninguna` | Baseline frío: sin retención entre turnos fuera del prompt actual |
| `claude-md-manual` | `archivo-instrucciones` | Reglas e instrucciones estáticas leídas al inicio |
| `optmem` | `notas`, `resumen-jerarquico` | Script local de log aditivo y árbol de resúmenes (Taelin) |
| `memo` | `resumen-jerarquico` | Condensación de memoria / Memory as a Model (MeMo) |
| `rag-local` | `vectorial` | Vector store local (ChromaDB) con embeddings locales |
| `mempalace` | `vectorial` | Metáfora de palacio de memoria sobre ChromaDB |
| `mem0` | `vectorial`, `grafo` | Sistema híbrido vector + grafo (requiere verificar modo local sin API key) |
| `letta` | `resumen-jerarquico`, `vectorial` | Memoria multi-nivel agente-administrada (requiere verificar servidor local) |
| `nativa-antigravity` | `nativa` | Almacén y memoria persistente interna del harness Antigravity |

## Categorías de hechos sembrados (Fact Injection)

| Código | Categoría | Propósito en el Benchmark |
|---|---|---|
| `F-ID` | Identidad / Perfil | Datos específicos del usuario y entorno (ej. versión de runtime) |
| `F-RULE` | Reglas de estilo / Convenciones | Instrucciones explícitas de programación a mantener |
| `F-CODE` | Código previo en sesión | Funciones y clases generadas previamente que se vuelven a solicitar |
| `F-NEG` | Instrucciones negativas | Restricciones de cosas que NO se deben hacer |
| `F-UPD` | Actualización de preferencia | Cambios de criterio a mitad de sesión (prueba obsolescencia) |
| `F-CONT` | Hechos contradictorios | Dos versiones sembradas para evaluar tasa de alucinación |

## Estado actual

- Scouting y diseño conceptual completados.
- Homologación de tipos, sistemas y experimentos adaptada a la plantilla de `memoria-bench`.
