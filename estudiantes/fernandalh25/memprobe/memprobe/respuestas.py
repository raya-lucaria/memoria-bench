"""Lectura estricta de los archivos de respuestas que escribe el agente.

Nada se corrige en silencio: todo lo que no se pueda leer se cuenta y se reporta,
y esa pregunta puntúa 0.
"""
from __future__ import annotations

import json
import os
from typing import Dict, List, Tuple


def leer(paths: List[str], n_preguntas: int) -> Tuple[Dict[int, object], Dict]:
    """Devuelve ({id: respuesta}, info). Si un id aparece dos veces, gana el último."""
    respuestas: Dict[int, object] = {}
    info = {"lineas": 0, "invalidas": 0, "duplicadas": 0, "ids_fuera_de_rango": 0,
            "sin_respuesta": 0, "detalle": []}

    def malo(clave: str, donde: str, motivo: str) -> None:
        info[clave] += 1
        if len(info["detalle"]) < 20:
            info["detalle"].append("%s: %s" % (donde, motivo))

    for path in paths:
        base = os.path.basename(path)  # nunca la ruta completa: puede ser personal
        with open(path, encoding="utf-8") as f:
            for n, linea in enumerate(f, 1):
                linea = linea.strip()
                if not linea or linea.startswith("```"):  # tolera cercas de código de markdown
                    continue
                info["lineas"] += 1
                donde = "%s:%d" % (base, n)
                try:
                    obj = json.loads(linea)
                except ValueError:
                    malo("invalidas", donde, "no es JSON")
                    continue
                if (not isinstance(obj, dict) or "answer" not in obj
                        or not isinstance(obj.get("id"), int) or isinstance(obj.get("id"), bool)):
                    malo("invalidas", donde, 'falta {"id": entero, "answer": ...}')
                    continue
                i = obj["id"]
                if not 0 <= i < n_preguntas:
                    malo("ids_fuera_de_rango", donde, "id %d no existe" % i)
                    continue
                if i in respuestas:
                    malo("duplicadas", donde, "id %d repetido (gana el último)" % i)
                respuestas[i] = obj["answer"]
    info["sin_respuesta"] = n_preguntas - len(respuestas)
    return respuestas, info
