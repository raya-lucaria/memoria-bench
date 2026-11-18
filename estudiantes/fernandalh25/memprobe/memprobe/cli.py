from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from typing import Dict, List

from . import __version__, corrida, respuestas
from .generate import ABILITIES, BENCH_VERSION, TRACKS, Question, generate_episode
from .kit import TIERS, build_kit
from .runner import run_episode
from .score import piso, score_one, summarize

SUITES = {  # nombre: (eventos, preguntas, semillas); solo para `correr` (runner por stdin/stdout)
    "humo": (300, 70, [1]),
    "estandar": (2000, 140, [1, 2, 3]),
    "estres": (20000, 140, [1]),
}


def _pct(x) -> str:
    return "n/d" if x is None else "%.1f%%" % (100 * x)


def _cargar(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def imprimir_reporte(rep: Dict) -> None:
    print("\nmemprobe %s (benchmark %s)   sistema: %s" % (rep["version"], BENCH_VERSION, rep["sut"]))
    for track, t in rep["pistas"].items():
        ci = t["ci95"]
        print("\n== pista: %s   (%d preguntas, datasets %s)" % (track, t["n_questions"], ",".join(t["dataset_ids"])))
        for ab in ABILITIES:
            a = t["abilities"].get(ab)
            if a:
                print("   %-10s %7s   n=%d" % (ab, _pct(a["score"]), a["n"]))
        print("   %-10s %7s   IC95%% aprox. [%s, %s] (trata las preguntas como independientes)"
              % ("MACRO", _pct(t["macro"]), _pct(ci[0]) if ci else "n/d", _pct(ci[1]) if ci else "n/d"))
        if t.get("piso_macro") is not None:
            print("   piso (siempre UNKNOWN, sin agente): %s   techo: 100.0%%" % _pct(t["piso_macro"]))
        print("   alucinación (respondió algo cuando debía ser UNKNOWN): %s" % _pct(t["hallucination_rate"]))
        print("   falso UNKNOWN (dijo UNKNOWN habiendo respuesta):      %s" % _pct(t["false_abstain_rate"]))
        if t["age"]:
            print("   por distancia al hecho necesario: " + "  ".join(
                "%s %s" % (k, _pct(v["score"])) for k, v in t["age"].items()))
        r = t.get("respuestas")
        if r:
            print("   respuestas: %d líneas, %d inválidas, %d duplicadas, %d ids fuera de rango, %d preguntas sin respuesta"
                  % (r["lineas"], r["invalidas"], r["duplicadas"], r["ids_fuera_de_rango"], r["sin_respuesta"]))
            for d in r["detalle"][:5]:
                print("      - " + d)
        if t.get("crashed"):
            print("   !! caídas o timeouts: " + "; ".join(t["crashed"]))
        if t.get("seconds"):
            print("   tiempo (informativo, depende del hardware): ingesta %.1fs, consultas %.1fs"
                  % (t["seconds"]["ingest"], t["seconds"]["query"]))
    print("\nMACRO GENERAL (promedio de pistas): %s" % _pct(rep["overall_macro"]))
    gap = rep.get("brecha_prose_menos_code")
    if gap is not None:
        print("brecha prose - code: %+.1f puntos" % (100 * gap))


# ------------------------------------------------------------------ kit / puntuar / comparar

def cmd_kit(a) -> int:
    cps = tuple(float(x) for x in a.checkpoints.split(",")) if a.checkpoints else None
    try:
        m = build_kit(a.tier, a.pista, a.seed, a.salida, a.lote, cps)
    except FileExistsError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    print("kit listo en %s/kit  (dataset_id %s, kit_id %s)" % (a.salida, m["dataset_id"], m["kit_id"]))
    print("  %d sesiones x %d eventos, %d preguntas; piso siempre-UNKNOWN %s"
          % (m["sesiones"], m["eventos_por_sesion"], m["preguntas"], _pct(m["piso_macro"])))
    print("  tamaño estimado (caracteres/4): fase 1 ≈ %d tokens, fase 2 ≈ %d tokens" % (m["tokens_est_fase1"], m["tokens_est_fase2"]))
    print("  Sigue %s/kit/LEEME.md. NO copies gold.jsonl dentro de la carpeta de trabajo del agente." % a.salida)
    return 0


def _cargar_preguntas(dir_: str):
    manifest = _cargar(os.path.join(dir_, "manifest.json"))
    with open(os.path.join(dir_, "gold.jsonl"), encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    qs = [Question(g["after_seq"], g["q"], g["format"], g["gold"], g["ability"], g["kind"], g["age_frac"]) for g in rows]
    return manifest, qs


def cmd_revisar(a) -> int:
    manifest, qs = _cargar_preguntas(a.dir)
    _ans, info = respuestas.leer(a.respuestas, len(qs))
    print("%d líneas leídas: %d inválidas, %d duplicadas, %d ids fuera de rango, %d preguntas sin respuesta"
          % (info["lineas"], info["invalidas"], info["duplicadas"], info["ids_fuera_de_rango"], info["sin_respuesta"]))
    for d in info["detalle"]:
        print("  - " + d)
    return 0 if not (info["invalidas"] or info["duplicadas"] or info["ids_fuera_de_rango"]) else 1


def cmd_puntuar(a) -> int:
    manifest, qs = _cargar_preguntas(a.dir)
    card = None
    if a.corrida:
        card = _cargar(a.corrida)
        errores, avisos = corrida.validar(card, manifest)
        for w in avisos:
            print("aviso: " + w, file=sys.stderr)
        if errores:
            print("la corrida no es válida:", file=sys.stderr)
            for e in errores:
                print("  - " + e, file=sys.stderr)
            return 2
    elif not a.sin_corrida:
        print("error: falta --corrida corrida.json (o --sin-corrida para un cálculo no oficial)", file=sys.stderr)
        return 2
    ans, info = respuestas.leer(a.respuestas, len(qs))
    items = [(q, score_one(q.fmt, q.gold, ans.get(i)), ans.get(i)) for i, q in enumerate(qs)]
    block = summarize(items)
    block.update({"dataset_ids": [manifest["dataset_id"]], "piso_macro": piso(qs), "respuestas": info})
    nombre = "no oficial (sin corrida)" if card is None else "%s / %s / %s" % (
        card["harness"], card["memoria_id"], card["condicion"])
    rep = {"version": __version__, "sut": nombre, "pistas": {manifest["track"]: block}, "overall_macro": block["macro"]}
    imprimir_reporte(rep)
    if a.salida:
        out = {"benchmark": "memprobe", "version": __version__, "version_benchmark": BENCH_VERSION,
               "manifest": {k: manifest[k] for k in ("dataset_id", "kit_id", "tier", "track", "seed", "preguntas")},
               "corrida": card, "resultado": block}
        with open(a.salida, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, indent=2)
            f.write("\n")
        print("\nescrito %s" % a.salida)
    return 0


def _media(xs):
    return sum(xs) / len(xs) if xs else None


def cmd_comparar(a) -> int:
    def agrupar(paths):
        g: Dict[str, List[Dict]] = {}
        for p in paths:
            r = _cargar(p)
            g.setdefault(r["manifest"]["dataset_id"], []).append(r)
        return g
    A, B = agrupar(a.a), agrupar(a.b)
    comunes = sorted(set(A) & set(B))
    if not comunes:
        print("error: A y B no comparten ningún dataset_id; solo se comparan corridas del mismo kit y semilla.", file=sys.stderr)
        return 2
    for d in comunes:
        kits = {r["manifest"]["kit_id"] for r in A[d] + B[d]}
        if len(kits) > 1:
            print("error: el dataset %s aparece con kits distintos (%s)" % (d, ", ".join(sorted(kits))), file=sys.stderr)
            return 2
    for d in sorted(set(A) ^ set(B)):
        print("aviso: dataset %s solo está en un lado; se ignora" % d, file=sys.stderr)

    def etiqueta(g):
        c = next(iter(g.values()))[0].get("corrida") or {}
        return "%s/%s/%s" % (c.get("harness", "?"), c.get("memoria_id", "?"), c.get("condicion", "?"))
    print("A = %s     B = %s" % (etiqueta(A), etiqueta(B)))
    print("%-18s %4s %4s %8s %8s %9s" % ("dataset_id", "nA", "nB", "A", "B", "B - A"))
    deltas, wins = [], 0
    por_hab: Dict[str, List[float]] = {ab: [] for ab in ABILITIES}
    for d in comunes:
        ma = _media([r["resultado"]["macro"] for r in A[d]])
        mb = _media([r["resultado"]["macro"] for r in B[d]])
        deltas.append(mb - ma)
        wins += mb > ma
        print("%-18s %4d %4d %8s %8s %+8.1f" % (d, len(A[d]), len(B[d]), _pct(ma), _pct(mb), 100 * (mb - ma)))
        for ab in ABILITIES:
            xa = [r["resultado"]["abilities"][ab]["score"] for r in A[d] if ab in r["resultado"]["abilities"]]
            xb = [r["resultado"]["abilities"][ab]["score"] for r in B[d] if ab in r["resultado"]["abilities"]]
            if xa and xb:
                por_hab[ab].append(_media(xb) - _media(xa))
    print("\ndiferencia media B - A: %+.1f puntos (macro); B gana en %d de %d semillas" % (100 * _media(deltas), wins, len(comunes)))
    for ab in ABILITIES:
        if por_hab[ab]:
            print("   %-10s %+6.1f" % (ab, 100 * _media(por_hab[ab])))
    if len(comunes) < 3:
        print("\naviso: menos de 3 semillas en común; con agentes no deterministas esto no basta para concluir nada.")
    return 0


# ------------------------------------------------------------------ correr (runner por stdin/stdout)

def cmd_correr(a) -> int:
    ev, nq, seeds = SUITES[a.suite]
    ev = a.events or ev
    nq = a.queries or nq
    if a.seeds:
        seeds = [int(x) for x in a.seeds.split(",")]
    pistas = a.pistas.split(",")
    argv = shlex.split(a.sut)
    rep = {"benchmark": "memprobe", "version": __version__, "sut": corrida.limpiar_home(a.sut),
           "config": {"eventos": ev, "preguntas": nq, "semillas": seeds, "pistas": pistas}, "pistas": {}}
    for pista in pistas:
        items, ids, caidas, qs_all = [], [], [], []
        t_in = t_q = 0.0
        for seed in seeds:
            ep = generate_episode(pista, seed, ev, nq)
            ids.append(ep.dataset_id)
            print("corriendo pista=%s semilla=%d eventos=%d ..." % (pista, seed, ev), file=sys.stderr)
            r = run_episode(argv, ep, a.timeout, a.cwd)
            if r.crashed:
                caidas.append("semilla %d: %s" % (seed, corrida.limpiar_home(r.crashed)))
            t_in += r.t_ingest
            t_q += r.t_query
            qs_all += ep.questions
            for q, ans in zip(ep.questions, r.answers):
                items.append((q, score_one(q.fmt, q.gold, ans), ans))
        block = summarize(items)
        block.update({"dataset_ids": ids, "crashed": caidas, "seconds": {"ingest": t_in, "query": t_q},
                      "piso_macro": piso(qs_all)})
        rep["pistas"][pista] = block
    macros = [t["macro"] for t in rep["pistas"].values() if t["macro"] is not None]
    rep["overall_macro"] = sum(macros) / len(macros) if macros else None
    tr = rep["pistas"]
    rep["brecha_prose_menos_code"] = (tr["prose"]["macro"] - tr["code"]["macro"]) if "prose" in tr and "code" in tr else None
    imprimir_reporte(rep)
    if a.salida:
        with open(a.salida, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rep, f, indent=2)
            f.write("\n")
        print("\nescrito %s" % a.salida)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="memprobe", description="Benchmark de memoria determinista: sin modelo, sin API keys, sin red.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    k = sub.add_parser("kit", help="genera el kit para correr con un harness (camino principal)")
    k.add_argument("--tier", choices=sorted(TIERS), default="chico")
    k.add_argument("--pista", choices=TRACKS, default="prose")
    k.add_argument("--seed", type=int, default=1)
    k.add_argument("--lote", type=int, default=0, help="preguntas por archivo (0 = todas juntas)")
    k.add_argument("--checkpoints", help="fracciones separadas por coma, p. ej. 0.5,1.0 (por defecto solo al final)")
    k.add_argument("--salida", required=True, help="carpeta nueva donde se escribe el kit")
    k.set_defaults(fn=cmd_kit)

    r = sub.add_parser("revisar-respuestas", help="valida los archivos de respuestas que escribió el agente")
    r.add_argument("--dir", required=True)
    r.add_argument("--respuestas", nargs="+", required=True)
    r.set_defaults(fn=cmd_revisar)

    s = sub.add_parser("puntuar", help="puntúa respuestas contra el gold de un kit")
    s.add_argument("--dir", required=True)
    s.add_argument("--respuestas", nargs="+", required=True)
    s.add_argument("--corrida", help="corrida.json (obligatorio salvo --sin-corrida)")
    s.add_argument("--sin-corrida", action="store_true", help="cálculo no oficial, sin tarjeta de corrida")
    s.add_argument("--salida", help="escribe resultado.json aquí")
    s.set_defaults(fn=cmd_puntuar)

    c = sub.add_parser("comparar", help="compara dos conjuntos de resultados, emparejados por semilla")
    c.add_argument("--a", nargs="+", required=True, help="resultado.json de la condición A (p. ej. ninguna)")
    c.add_argument("--b", nargs="+", required=True, help="resultado.json de la condición B")
    c.set_defaults(fn=cmd_comparar)

    x = sub.add_parser("correr", help="corre un programa por stdin/stdout (camino secundario: CI y baselines)")
    x.add_argument("--sut", required=True, help='comando, p. ej. "python3 examples/reference-sut.py"')
    x.add_argument("--suite", choices=sorted(SUITES), default="estandar")
    x.add_argument("--pistas", default="prose,code", help="lista de: " + ",".join(TRACKS))
    x.add_argument("--seeds", help="lista separada por comas; reemplaza la de la suite")
    x.add_argument("--events", type=int)
    x.add_argument("--queries", type=int)
    x.add_argument("--timeout", type=float, default=60.0)
    x.add_argument("--cwd")
    x.add_argument("--salida")
    x.set_defaults(fn=cmd_correr)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
