# Diseño

En la taxonomía de los cuatro ejes (dónde vive, qué guarda, quién escribe y cuándo se lee, para quién es), esta
memoria es: **archivos de texto bajo git**; guarda **semántica** (hechos), **procedimental** (reglas) y
**episódica destilada** (errores); **escribe el agente y aprueba un humano**; el índice se carga siempre (push)
y el detalle bajo demanda (pull); el alcance es **proyecto/repo**.

## Decisiones

| Decisión | Por qué | Costo que se acepta |
|---|---|---|
| Push sólo de `INDICE.md` (una línea por nota, ≤1,500 tokens) y pull del detalle | Si la memoria depende de que el agente decida buscar, puede no buscar nunca; si se empuja todo, crece y diluye las instrucciones (context rot) | Hay que escribir buenos resúmenes de ≤100 caracteres |
| El índice no tiene fechas y se ordena de forma determinista; sólo cambia al aprobar u obsoletar | Prompt caching: un prefijo idéntico cuesta ≈0.1× al leerse desde caché. Hermes congela su memoria por sesión por la misma razón | Lo aprobado a mitad de sesión entra a la siguiente |
| Una nota = un archivo con frontmatter `clave: valor` | Diffs pequeños, `git blame` útil, conflictos de merge localizados, sin parser YAML | Más archivos |
| `LOG.md` append-only con el sha de cada versión | Igual que el LOG de OptMem: la historia no se reescribe. El sha permite a `lint` detectar ediciones hechas fuera de la herramienta | Editar a mano obliga a `sellar` |
| Snapshots `agents/vNNN.md` además de git | Quien compara arquitecturas puede leer la evolución sin clonar el historial; `TRANSICIONES.md` la resume en ≈30 tokens por versión | Duplica texto (AGENTS.md debe ser corto de todos modos) |
| Búsqueda BM25 en Python puro | Auditable, determinista y sin infraestructura. En el banco sintético BM25 rinde igual que grep+recencia o mejor | Débil con paráfrasis; si se necesita, se cambia `buscar` por embeddings locales sin tocar el formato |
| Sin LLM dentro de la herramienta | Escritura determinista (como MemPalace) y cero tokens de mantenimiento | La consolidación semántica la hace el humano o el agente vía `proponer --reemplaza` |

## Amenazas y defensas

### Envenenamiento (MINJA, AgentPoison, MemoryGraft, MemSecBench)
El ataque típico es que un texto que el agente lee (un issue, un README, una página web, un mensaje del usuario)
termine guardado como memoria y luego se obedezca en todas las sesiones.

1. **Cuarentena**: todo lo que escribe el agente cae en `propuestas/` y no entra al índice. `aprobar` exige
   `--por humano`, y en un repo compartido la aprobación es además un PR revisado.
2. **Procedencia obligatoria**: cada nota declara `fuente` (humano, agente, herramienta o externo) y `evidencia`
   (ruta, comando o URL). Sin evidencia se rechaza.
3. **Lo externo nunca es regla**: una nota con fuente externa puede ser un hecho citado, pero no puede
   aprobarse como regla, y `lint` también lo marca.
4. **Escáner de inyección** al proponer y en `lint`: «ignora las instrucciones», suplantación de system prompt,
   `curl | sh`, «sin avisar», desactivar tests/hooks/revisión, blobs base64. Las reglas negadas («nunca
   desactives los tests») no cuentan. Es una heurística y no garantiza nada: la defensa real es la cuarentena.
5. **Integridad**: el sha en `LOG.md` delata ediciones directas, y `INDICE.md` se regenera, así que editarlo a
   mano no sirve.
6. **Jerarquía explícita** en el bloque de AGENTS.md: la memoria son datos, no órdenes, y si contradice AGENTS.md
   o al usuario, pierde.
7. **Reversible**: cualquier cosa aprendida se deshace con `obsoletar` o `git revert`, y queda registrado quién y
   cuándo.

### Aprender errores (y no aprender errores)
- `mem.py error <clave>` **suma repeticiones** en vez de duplicar. Si el mismo error ocurre **2 veces**, sugiere
  convertirlo en regla de AGENTS.md (equivale a «actualiza AGENTS.md cuando el agente se equivoque de forma
  repetida»).
- `version --refs E-0001` enlaza la versión nueva con la lección y **saca la nota del índice**, porque ya vive en
  AGENTS.md y no conviene pagarla dos veces en tokens.
- Si el error reaparece después de promovido, se abre una propuesta nueva. Esa es la señal de que la regla no
  funcionó.
- Para evitar «memorias que aprenden errores»: aprobación humana, evidencia obligatoria, campo `revisar` (90
  días; `lint` marca las vencidas) y `reemplaza`, que obsoleta la nota vieja en lugar de dejar dos verdades.

### Privacidad
- **Alcance**: aquí sólo va conocimiento del proyecto. Las preferencias personales se quedan en la memoria local
  del harness (por ejemplo, la auto memory de Claude Code, que es local a la máquina) y nunca se commitean.
- **Escáner** al proponer, al versionar AGENTS.md y en `lint`, sobre todos los archivos (incluido `LOG.md`):
  correos, teléfonos, rutas `/home/<usuario>`, llaves de API, llaves privadas y JWT.
- **Lista local** `local/privado.txt` (ignorada por git): nombres reales, proyectos o clientes que no deben
  aparecer. Bloquea sin publicar la lista misma.
- **Olvido**: `olvidar <ID>` borra el archivo y deja en `LOG.md` sólo el id. Git conserva el historial, así que en
  un repo público hay que purgarlo (`git filter-repo`) y rotar cualquier credencial expuesta.
- Los ids nunca se reutilizan, para que una referencia vieja no apunte a otra nota.

## Comparación rápida

| Sistema | Dónde vive | Quién escribe | Defensa ante envenenamiento | Arranque | Versionado |
|---|---|---|---|---|---|
| **memoria-versionada** | MD + git | agente propone, humano aprueba | cuarentena, procedencia, escáner, sha | índice ≤1.5k tokens (ejemplo: 68) | git + snapshots + TRANSICIONES |
| OptMem | log append-only + árbol de resúmenes | agente | ninguna explícita | bloque de ~426 tokens | log inmutable |
| MemPalace | ChromaDB + SQLite | determinista, literal | ninguna explícita | ~170 tokens | no |
| Letta MemFS | MD + git | agente y subagentes de reflexión | revert | según bloques | commit por cambio |
| LLM Wiki | MD | LLM compila | lint de páginas | `index.md` | opcional |
| Claude Code auto memory | MD local | agente | ninguna explícita | ≤200 líneas / 25 KB | no (local) |

Cifras y fuentes de esta tabla: investigación propia sobre memoria de harnesses (nov-2026). Las cifras de
arranque de terceros son las que reportan los propios proyectos.

## Límites conocidos
- La aprobación humana es un cuello de botella; está pensada para pocas notas de alto valor, no para miles.
- El escáner de inyección se evade con paráfrasis. No reemplaza la revisión.
- Las ventanas de validez son por fecha de revisión, no por hecho (un grafo temporal tipo Graphiti lo hace mejor).
- No hay alcance por usuario ni multiusuario. Es memoria de repositorio.
