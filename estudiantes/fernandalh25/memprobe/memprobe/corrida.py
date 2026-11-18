"""Tarjeta de corrida (`corrida.json`): quién corrió qué, para poder repetirlo.

Reglas del repo memoria-bench que se aplican aquí: nada de rutas personales,
correos, llaves ni tokens; lo que no se sabe se escribe `no-se`, nunca se deja
en blanco ni se inventa.
"""
from __future__ import annotations

import os
import re
from typing import Dict, List, Tuple

CAMPOS = ["harness", "harness_version", "modelo", "suscripcion", "memoria_id", "memoria_version",
          "condicion", "memoria_nativa", "aislamiento", "repeticion", "fecha", "sistema_operativo"]
PERMITIDOS = {
    "condicion": {"ninguna", "contexto-completo", "memoria"},
    "memoria_nativa": {"activada", "desactivada", "no-se"},
    "aislamiento": {"si", "no", "no-se"},
    "sistema_operativo": {"linux", "macos", "windows", "wsl", "no-se"},
}
# Estos no pueden ser "no-se": sin ellos el resultado no se puede situar.
OBLIGATORIOS_REALES = {"harness", "memoria_id", "condicion", "repeticion", "fecha"}

PRIVACIDAD = [
    # Los prefijos se parten a propósito para que este archivo no contenga ninguna ruta personal literal.
    ("ruta personal", re.compile(r"(/Us" r"ers/|/ho" r"me/|[A-Za-z]:\\Us" r"ers\\)[^\s\"\']+")),
    ("correo", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("llave o token", re.compile(r"\b(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9]{8,}|github_pat_[A-Za-z0-9_]{8,}|"
                                 r"xox[bp]-[A-Za-z0-9-]{8,}|AKIA[A-Z0-9]{8,}|AIza[A-Za-z0-9_-]{10,})")),
]
FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def plantilla(manifest: Dict) -> Dict:
    card: Dict = {
        "_ayuda": "Llena los campos vacíos. Usa no-se si no lo sabes. Sin rutas personales, correos ni llaves.",
        "_valores_permitidos": {k: sorted(v) for k, v in PERMITIDOS.items()},
        "dataset_id": manifest["dataset_id"], "kit_id": manifest["kit_id"],
        "tier": manifest["tier"], "track": manifest["track"], "seed": manifest["seed"],
    }
    for c in CAMPOS:
        card[c] = 1 if c == "repeticion" else ""
    return card


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _strings(k)
            yield from _strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _strings(v)


def privacidad(obj) -> List[str]:
    hallazgos = []
    for s in _strings(obj):
        for nombre, rx in PRIVACIDAD:
            if rx.search(s):
                hallazgos.append("%s en un campo de texto" % nombre)
    return hallazgos


def validar(card: Dict, manifest: Dict) -> Tuple[List[str], List[str]]:
    """Devuelve (errores, avisos). Con errores no se puntúa como corrida oficial."""
    err: List[str] = []
    avisos: List[str] = []
    for c in CAMPOS:
        v = card.get(c)
        if v is None or (isinstance(v, str) and not v.strip()):
            err.append("falta `%s` (si no lo sabes, escribe no-se)" % c)
        elif v == "no-se" and c in OBLIGATORIOS_REALES:
            err.append("`%s` no puede ser no-se" % c)
    for c, ok in PERMITIDOS.items():
        v = card.get(c)
        if isinstance(v, str) and v.strip() and v not in ok:
            err.append("`%s` = %r no es válido; usa uno de %s" % (c, v, sorted(ok)))
    r = card.get("repeticion")
    if r is not None and (not isinstance(r, int) or isinstance(r, bool) or r < 1):
        err.append("`repeticion` debe ser un entero >= 1")
    f = card.get("fecha")
    if isinstance(f, str) and f.strip() and not FECHA.match(f):
        err.append("`fecha` debe ser AAAA-MM-DD")
    for k in ("dataset_id", "kit_id"):
        if card.get(k) != manifest.get(k):
            err.append("`%s` no coincide con el kit (%s vs %s): no se pueden comparar" % (k, card.get(k), manifest.get(k)))
    for h in privacidad(card):
        err.append("posible dato personal: %s (quítalo antes de subirlo)" % h)
    if card.get("condicion") in ("ninguna", "contexto-completo") and card.get("memoria_id") not in ("ninguna", "no-se"):
        avisos.append("la condición %s se anota con memoria_id `ninguna`" % card.get("condicion"))
    return err, avisos


def limpiar_home(s: str) -> str:
    """Reemplaza el directorio personal por `~` en textos que irán a un reporte."""
    home = os.path.expanduser("~")
    return s.replace(home, "~") if home and home != "~" else s
