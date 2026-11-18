"""Genera el kit para correr memprobe con un harness (agente con suscripción).

Layout de salida (DIR):
    kit/                    <- lo único que ve el agente/operador
        LEEME.md
        fase-1-sesiones/sesion-NN.md
        fase-2-preguntas/preguntas-tras-sesion-NN[-lote-K].md
        referencia/contexto-completo-tras-sesion-NN.md
    gold.jsonl              <- respuestas correctas: NO copiar dentro de la carpeta de trabajo
    manifest.json
    corrida-plantilla.json
"""
from __future__ import annotations

import hashlib
import json
import os
from typing import Dict, List, Optional, Tuple

from . import __version__
from .generate import BENCH_VERSION, FINAL_ONLY, Episode, Question, generate_episode
from .score import piso as calcular_piso

# nombre: (sesiones, eventos por sesión, preguntas)
TIERS: Dict[str, Tuple[int, int, int]] = {
    "chico": (8, 35, 42),
    "medio": (12, 50, 70),
    "grande": (24, 100, 140),
}

FMT_ES = {"value": "valor", "list": "lista", "count": "conteo"}

PROMPT_FASE1 = "Lee `entrada/{archivo}` y sigue sus instrucciones."
PROMPT_FASE2 = "Lee `entrada/{archivo}` y sigue sus instrucciones. Escribe `respuestas.jsonl` en la carpeta de trabajo."

REGLAS = """\
## Reglas

- Los nombres y valores son palabras inventadas. No adivines: si lo ocurrido en las sesiones no basta para contestar, la respuesta es exactamente `UNKNOWN`.
- «Actual» significa lo último que se afirmó. Si algo se pidió olvidar o borrar y después no se volvió a afirmar, la respuesta es `UNKNOWN`.
- «Al final del día D» significa el estado después de todo lo ocurrido hasta el día D inclusive.
- Responde solo con el valor, sin explicaciones.

## Cómo responder

Escribe un archivo `respuestas.jsonl` en tu carpeta de trabajo, con **una línea JSON por pregunta** y el `id` exactamente como aparece abajo:

- tipo `valor`: `{"id": 12, "answer": "Zarste"}`
- tipo `lista`: `{"id": 13, "answer": ["Brakelor", "Veltrin"]}`
- tipo `conteo`: `{"id": 14, "answer": 3}`
- si no se puede saber: `{"id": 15, "answer": "UNKNOWN"}`
"""


def _nn(k: int) -> str:
    return "%02d" % k


def _sesion_md(k: int, n: int, eventos: List[str]) -> str:
    return (
        "# Sesión %d de %d\n\n"
        "Esta es la sesión %d de %d de una serie. Más adelante, en una conversación nueva, se te harán "
        "preguntas sobre lo que ocurrió en estas sesiones. En ese momento **no tendrás este archivo**: "
        "solo contarás con lo que hayas guardado en tu memoria.\n\n"
        "Qué hacer ahora:\n\n"
        "1. Lee los %d eventos de abajo, en orden. Cada uno trae su día.\n"
        "2. Haz lo que tu sistema de memoria requiera para recordar esto después. "
        "Si no tienes ningún sistema de memoria, no hagas nada especial.\n"
        "3. No respondas preguntas todavía y no modifiques este archivo.\n"
        "4. Cuando termines, responde únicamente: `Listo.`\n\n"
        "## Eventos\n\n```text\n%s\n```\n" % (k, n, k, n, len(eventos), "\n".join(eventos))
    )


def _lista_preguntas(qs: List[Tuple[int, Question]]) -> str:
    return "\n".join("- **id %d** (%s): %s" % (i, FMT_ES[q.fmt], q.q) for i, q in qs) + "\n"


def _preguntas_md(k: int, n: int, qs: List[Tuple[int, Question]], lote: Optional[Tuple[int, int]]) -> str:
    titulo = "# Preguntas (tras la sesión %d de %d)" % (k, n)
    if lote:
        titulo += ", lote %d de %d" % lote
    return (
        titulo + "\n\n"
        "Estás en una conversación nueva. **No tienes acceso a los archivos de las sesiones.** "
        "Responde usando solo tu memoria.\n\n" + REGLAS + "\n## Preguntas\n\n" + _lista_preguntas(qs)
    )


def _referencia_md(k: int, n: int, eventos: List[str], qs: List[Tuple[int, Question]]) -> str:
    return (
        "# Condición de referencia: contexto completo (tras la sesión %d de %d)\n\n"
        "Todo el historial está a continuación. Úsalo para responder las preguntas. "
        "No hay sistema de memoria que probar en esta condición.\n\n"
        "## Historial (%d eventos, en orden)\n\n```text\n%s\n```\n\n" % (k, n, len(eventos), "\n".join(eventos))
        + REGLAS + "\n## Preguntas\n\n" + _lista_preguntas(qs)
    )


def _leeme(m: Dict, archivos_preguntas: List[str]) -> str:
    n = m["sesiones"]
    f1 = PROMPT_FASE1.format(archivo="sesion-NN.md")
    f2 = PROMPT_FASE2.format(archivo="<archivo-de-preguntas>.md")
    return """\
# Cómo correr este kit

Kit de memprobe %(version)s. Pista `%(track)s`, tamaño `%(tier)s`, semilla %(seed)d.
`dataset_id`: `%(dataset_id)s`. `kit_id`: `%(kit_id)s`. Anótalos en tu `corrida.json`: dos resultados solo se comparan si coinciden.

Mide si un sistema de memoria, dentro de un harness, conserva, actualiza, olvida y agrega información **entre conversaciones**.
Se califica sola, sin LLM juez y sin API keys.

## Condiciones

| condición | qué es | qué haces |
|---|---|---|
| `ninguna` | piso: conversación nueva, sin memoria | solo la fase 2, en una carpeta limpia y con la memoria nativa del harness desactivada |
| `contexto-completo` | baseline tonto: todo el historial pegado en una sola conversación | solo `referencia/contexto-completo-tras-sesion-NN.md`, sin memoria |
| `memoria` | el sistema de memoria que pruebas | fase 1 y fase 2 |

Cada resultado se compara contra `ninguna` y `contexto-completo` **con la misma semilla**. Un número sin esos dos al lado no cuenta.
El piso de siempre-UNKNOWN (%(piso).1f %% macro) se calcula sin agente y sale en el reporte.

## Preparación (condición `memoria`)

1. Crea una carpeta de trabajo vacía, `trabajo/`, e instala ahí el sistema de memoria como lo pida su documentación.
2. Todas las conversaciones se abren **en esa misma carpeta**, para que la memoria persista entre ellas.
3. Si el harness tiene memoria nativa y no es la que pruebas, desactívala y anótalo (`memoria_nativa`). Cómo se desactiva depende del harness y **no está verificado aquí**.

## Fase 1: las %(sesiones)d sesiones

Para cada sesión `NN` de 01 a %(sesiones)02d, en orden:

1. `mkdir -p trabajo/entrada && cp kit/fase-1-sesiones/sesion-NN.md trabajo/entrada/`
2. Abre una conversación **nueva** en `trabajo/`.
3. Pega exactamente este texto (cambiando `NN`). El agente debe contestar `Listo.`

```text
%(f1)s
```

4. Cierra la conversación y borra el archivo: `rm trabajo/entrada/sesion-NN.md`

## Fase 2: las preguntas

Archivos de preguntas: %(archivos)s

1. Copia el archivo a `trabajo/entrada/`.
2. Abre una conversación **nueva** en `trabajo/`.
3. Pega exactamente este texto:

```text
%(f2)s
```

4. Mueve `trabajo/respuestas.jsonl` fuera de `trabajo/` (por ejemplo a `resultados/respuestas-<archivo>.jsonl`) y borra el archivo de preguntas de `entrada/`.

### Condiciones `ninguna` y `contexto-completo`

- `ninguna`: carpeta `trabajo/` vacía y sin memoria instalada; haz solo la fase 2 con el mismo texto de arriba.
- `contexto-completo`: copia `kit/referencia/contexto-completo-tras-sesion-NN.md` a `entrada/` y usa el mismo texto de la fase 2 con ese nombre de archivo. No hay fase 1.

## Puntuar

```bash
python -m memprobe revisar-respuestas --dir <salida> --respuestas resultados/respuestas-*.jsonl
python -m memprobe puntuar --dir <salida> --respuestas resultados/respuestas-*.jsonl \\
    --corrida corrida.json --salida resultado.json
```

`corrida-plantilla.json` trae lo que ya se sabe; llena el resto a mano. No pongas rutas personales, correos ni llaves: `puntuar` lo rechaza.

## Qué no se puede comprobar

El aislamiento entre fases depende de que sigas estos pasos. Nada impide que el agente vea archivos que dejaste en `trabajo/`.
Por eso la corrida declara `aislamiento` (`si | no | no-se`). Repite cada condición con al menos 3 semillas y compara con `memprobe comparar`.
Tamaño del kit (estimado, caracteres/4): fase 1 ≈ %(t1)d tokens en total, fase 2 ≈ %(t2)d tokens.
El costo real en tu suscripción **no está medido**.
""" % {
        "version": m["version_benchmark"], "track": m["track"], "tier": m["tier"], "seed": m["seed"],
        "dataset_id": m["dataset_id"], "kit_id": m["kit_id"], "piso": 100 * m["piso_macro"],
        "sesiones": n, "f1": f1, "f2": f2,
        "archivos": ", ".join("`%s`" % a for a in archivos_preguntas),
        "t1": m["tokens_est_fase1"], "t2": m["tokens_est_fase2"],
    }


def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _kit_id(kit_dir: str) -> str:
    h = hashlib.sha256()
    for root, _dirs, files in sorted(os.walk(kit_dir)):
        for fn in sorted(files):
            rel = os.path.relpath(os.path.join(root, fn), kit_dir).replace(os.sep, "/")
            if rel == "LEEME.md":  # el LEEME contiene el propio kit_id
                continue
            with open(os.path.join(root, fn), "rb") as f:
                h.update(rel.encode() + b"\0" + f.read() + b"\0")
    return h.hexdigest()[:16]


def build_kit(tier: str, track: str, seed: int, out: str, lote: int = 0,
              checkpoints: Optional[Tuple[float, ...]] = None) -> Dict:
    ns, per, nq = TIERS[tier]
    cps = checkpoints or FINAL_ONLY
    cps = tuple(round(f * ns) / ns for f in cps)  # alinear a fronteras de sesión
    ep: Episode = generate_episode(track, seed, ns * per, nq, cps)
    kit = os.path.join(out, "kit")
    if os.path.exists(kit):
        raise FileExistsError("ya existe %s: usa otra carpeta de salida" % kit)

    for k in range(1, ns + 1):
        _write(os.path.join(kit, "fase-1-sesiones", "sesion-%s.md" % _nn(k)),
               _sesion_md(k, ns, ep.events[(k - 1) * per:k * per]))

    por_cp: Dict[int, List[Tuple[int, Question]]] = {}
    for i, q in enumerate(ep.questions):
        por_cp.setdefault(q.after_seq, []).append((i, q))
    archivos: List[str] = []
    for after, qs in sorted(por_cp.items()):
        k = after // per
        _write(os.path.join(kit, "referencia", "contexto-completo-tras-sesion-%s.md" % _nn(k)),
               _referencia_md(k, ns, ep.events[:after], qs))
        chunks = [qs] if not lote else [qs[j:j + lote] for j in range(0, len(qs), lote)]
        for j, chunk in enumerate(chunks, 1):
            suf = "-lote-%d" % j if lote else ""
            name = "preguntas-tras-sesion-%s%s.md" % (_nn(k), suf)
            _write(os.path.join(kit, "fase-2-preguntas", name),
                   _preguntas_md(k, ns, chunk, (j, len(chunks)) if lote else None))
            archivos.append(name)

    piso = calcular_piso(ep.questions)
    chars1 = sum(len(t) for t in ep.events)
    chars2 = sum(len(q.q) + 40 for q in ep.questions)
    manifest = {
        "benchmark": "memprobe", "version_paquete": __version__, "version_benchmark": BENCH_VERSION,
        "tier": tier, "track": track, "seed": seed, "dataset_id": ep.dataset_id,
        "sesiones": ns, "eventos_por_sesion": per, "eventos": ns * per, "preguntas": len(ep.questions),
        "checkpoints_eventos": sorted(por_cp), "archivos_preguntas": archivos, "lote": lote,
        "piso_macro": piso, "tokens_est_fase1": chars1 // 4, "tokens_est_fase2": chars2 // 4,
    }
    _write(os.path.join(kit, "LEEME.md"), _leeme(dict(manifest, kit_id="(pendiente)"), archivos))
    manifest["kit_id"] = _kit_id(kit)
    _write(os.path.join(kit, "LEEME.md"), _leeme(manifest, archivos))
    _write(os.path.join(out, "manifest.json"), json.dumps(manifest, indent=2) + "\n")
    _write(os.path.join(out, "gold.jsonl"), "".join(
        json.dumps({"id": i, "gold": q.gold, "ability": q.ability, "kind": q.kind, "format": q.fmt,
                    "age_frac": q.age_frac, "after_seq": q.after_seq, "q": q.q}, ensure_ascii=True) + "\n"
        for i, q in enumerate(ep.questions)))
    from .corrida import plantilla
    _write(os.path.join(out, "corrida-plantilla.json"), json.dumps(plantilla(manifest), indent=2, ensure_ascii=False) + "\n")
    return manifest
