#!/usr/bin/env python3
"""mem.py — memoria versionada en Markdown para agentes (sólo biblioteca estándar).

Una nota = un archivo con frontmatter. El agente PROPONE, un humano APRUEBA.
Cada cambio queda en LOG.md (append-only) con el hash del archivo, así `lint`
detecta ediciones fuera de la herramienta. Ver README.md y DISENO.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import math
import os
import re
import shutil
import sys
from pathlib import Path

PRESUPUESTO_INDICE = 1500   # tokens (≈ caracteres/4) que se empujan al contexto
MAX_RESUMEN = 100           # caracteres por línea del índice
MAX_CUERPO = 40             # líneas por nota
UMBRAL_PROMOVER = 2         # repeticiones de un error para sugerir regla en AGENTS.md
DIAS_REVISION = 90

TIPOS = {"hecho": "H", "regla": "R", "error": "E"}
FUENTES = {"humano", "agente", "herramienta", "externo"}
ESTADOS = {"propuesta", "vigente", "obsoleta"}
CAMPOS = ["id", "tipo", "resumen", "fuente", "evidencia", "estado", "creado", "revisar"]
OPCIONALES = ["clave", "veces", "reemplaza", "aprobado"]

PRIVACIDAD = {
    "email": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "telefono": r"(?<![\w=-])(?:\+?\d{1,3}[ -])?\(?\d{2,3}\)?[ -]?\d{3,4}[ -]?\d{4}(?![\w-])",
    "ruta_personal": r"/(?:home|Users)/[^/\s]+",
    "llave_api": r"\b(?:sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bp]-[\w-]{10,})",
    "llave_privada": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "jwt": r"\beyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}",
}
INYECCION = {
    "ignorar_instrucciones": r"(?i)\b(ignora|olvida|ignore|disregard)\b.{0,30}\b(instruc|reglas|previous|above)",
    "suplantar_sistema": r"(?i)(system prompt|<\s*/?\s*system\s*>|eres ahora|you are now)",
    "ejecutar_remoto": r"(?i)(curl|wget)[^\n|]*\|\s*(ba)?sh",
    "ocultar": r"(?i)\b(no le digas|sin avisar|don'?t tell|without telling)\b",
    "desactivar_controles": r"(?i)\b(salt[ae]s?|omit[ea]s?|desactiv[ae]s?|skip|disable)\b.{0,20}\b(tests?|lint|revisi[oó]n|hooks?|aprobaci[oó]n)",
    "blob": r"[A-Za-z0-9+/=]{120,}",
}


# ---------------------------------------------------------------- utilidades
def hoy() -> str:
    return os.environ.get("MEMV_HOY") or dt.date.today().isoformat()


def tokens(texto: str) -> int:
    return math.ceil(len(texto) / 4)


def sha(texto: str) -> str:
    return hashlib.sha256(texto.encode()).hexdigest()[:12]


def raiz_por_defecto() -> Path:
    return Path(os.environ.get("MEMV_RAIZ") or Path(__file__).parent / "memoria")


def leer_nota(ruta: Path) -> tuple[dict, str]:
    texto = ruta.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?(.*)", texto, re.DOTALL)
    if not m:
        raise ValueError(f"{ruta.name}: falta frontmatter")
    meta = dict(linea.split(": ", 1) for linea in m.group(1).splitlines() if ": " in linea)
    return meta, m.group(2).strip()


def escribir_nota(ruta: Path, meta: dict, cuerpo: str) -> str:
    lineas = [f"{k}: {meta[k]}" for k in CAMPOS + OPCIONALES if meta.get(k) not in (None, "")]
    texto = "---\n" + "\n".join(lineas) + "\n---\n" + (cuerpo.strip() + "\n" if cuerpo.strip() else "")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")
    return texto


NEGACION = re.compile(r"(?i)\b(no|nunca|jam[aá]s|never|not|don'?t)\b[^.\n]{0,15}$")


def escanear(texto: str, patrones: dict, extra: list[str] = ()) -> list[str]:
    """Nombres de los patrones que aparecen. "Nunca desactives los tests" no cuenta como ataque."""
    negable = patrones is INYECCION
    hallazgos = [n for n, p in patrones.items()
                 if any(not (negable and NEGACION.search(texto[max(0, m.start() - 25):m.start()]))
                        for m in re.finditer(p, texto))]
    hallazgos += [f"lista_local:{i}" for i, w in enumerate(extra, 1) if w.lower() in texto.lower()]
    return hallazgos


class Memoria:
    def __init__(self, raiz: Path) -> None:
        self.raiz = raiz
        self.log = raiz / "LOG.md"
        self.indice = raiz / "INDICE.md"

    # -- rutas y lectura
    def carpeta(self, estado: str) -> Path:
        return self.raiz / ("propuestas" if estado == "propuesta" else "notas")

    def notas(self, incluir_propuestas: bool = False) -> list[tuple[Path, dict, str]]:
        dirs = ["notas"] + (["propuestas"] if incluir_propuestas else [])
        out = []
        for d in dirs:
            for p in sorted((self.raiz / d).glob("*.md")):
                meta, cuerpo = leer_nota(p)
                out.append((p, meta, cuerpo))
        return out

    def buscar_id(self, nota_id: str) -> Path:
        for d in ("notas", "propuestas"):
            for p in (self.raiz / d).glob(f"{nota_id}-*.md"):
                return p
        raise SystemExit(f"no existe {nota_id}")

    def siguiente_id(self, prefijo: str) -> str:
        usados = [int(m.group(1)) for d in ("notas", "propuestas") for p in (self.raiz / d).glob(f"{prefijo}-*.md")
                  if (m := re.match(rf"{prefijo}-(\d+)", p.name))]
        if self.log.exists():  # nunca reutilizar ids, ni de notas olvidadas
            usados += [int(n) for n in re.findall(rf"\| {prefijo}-(\d+) \|", self.log.read_text())]
        return f"{prefijo}-{max(usados, default=0) + 1:04d}"

    def lista_local(self) -> list[str]:
        p = self.raiz.parent / "local" / "privado.txt"   # ignorado por git
        if not p.exists():
            return []
        return [w.strip() for w in p.read_text().splitlines() if w.strip() and not w.startswith("#")]

    # -- bitácora
    def registrar(self, accion: str, nota_id: str, texto: str | None, por: str, motivo: str) -> None:
        motivo = motivo.replace("|", "/").replace("\n", " ")[:120]
        linea = f"{hoy()} | {accion} | {nota_id} | sha={sha(texto) if texto else '-'} | por={por} | {motivo}\n"
        if not self.log.exists():
            self.log.write_text("# LOG (append-only; lo escribe mem.py)\n", encoding="utf-8")
        with self.log.open("a", encoding="utf-8") as f:
            f.write(linea)

    def ultimo_sha(self) -> dict[str, str]:
        res: dict[str, str] = {}
        if self.log.exists():
            for linea in self.log.read_text().splitlines():
                partes = [x.strip() for x in linea.split("|")]
                if len(partes) >= 4 and partes[3].startswith("sha="):
                    res[partes[2]] = partes[3][4:]
        return res

    # -- operaciones
    def validar_texto(self, texto: str) -> None:
        priv = escanear(texto, PRIVACIDAD, self.lista_local())
        if priv:
            raise SystemExit(f"rechazado por privacidad: {', '.join(priv)}")
        iny = escanear(texto, INYECCION)
        if iny:
            raise SystemExit(f"rechazado por posible inyección: {', '.join(iny)}")

    def proponer(self, tipo: str, resumen: str, fuente: str, evidencia: str, cuerpo: str = "",
                 clave: str = "", reemplaza: str = "") -> str:
        if tipo not in TIPOS or fuente not in FUENTES:
            raise SystemExit(f"tipo ∈ {sorted(TIPOS)}, fuente ∈ {sorted(FUENTES)}")
        if len(resumen) > MAX_RESUMEN:
            raise SystemExit(f"resumen > {MAX_RESUMEN} caracteres")
        if not evidencia.strip():
            raise SystemExit("sin evidencia no hay memoria: indica ruta, comando o URL")
        self.validar_texto(f"{resumen}\n{evidencia}\n{cuerpo}\n{clave}")
        pid = self.siguiente_id("P")
        meta = {"id": pid, "tipo": tipo, "resumen": resumen, "fuente": fuente, "evidencia": evidencia,
                "estado": "propuesta", "creado": hoy(), "revisar": "-", "clave": clave,
                "veces": "1" if tipo == "error" else "", "reemplaza": reemplaza}
        texto = escribir_nota(self.raiz / "propuestas" / f"{pid}-{slug(resumen)}.md", meta, cuerpo)
        self.registrar("proponer", pid, texto, fuente, resumen)
        return pid

    def aprobar(self, pid: str, por: str, motivo: str = "") -> str:
        if por != "humano":
            raise SystemExit("sólo un humano aprueba (--por humano): el agente no se auto-promueve")
        ruta = self.buscar_id(pid)
        meta, cuerpo = leer_nota(ruta)
        if meta["estado"] != "propuesta":
            raise SystemExit(f"{pid} no es propuesta")
        if meta["tipo"] == "regla" and meta["fuente"] == "externo":
            raise SystemExit("contenido externo puede ser hecho citado, nunca regla")
        self.validar_texto(ruta.read_text())
        nid = self.siguiente_id(TIPOS[meta["tipo"]])
        revisar = (dt.date.fromisoformat(hoy()) + dt.timedelta(days=DIAS_REVISION)).isoformat()
        meta.update(id=nid, estado="vigente", revisar=revisar, aprobado=f"{hoy()} {pid}")
        ruta.unlink()
        texto = escribir_nota(self.raiz / "notas" / f"{nid}-{slug(meta['resumen'])}.md", meta, cuerpo)
        self.registrar("aprobar", nid, texto, por, motivo or f"desde {pid}")
        if meta.get("reemplaza"):
            self.obsoletar(meta["reemplaza"], por, f"reemplazada por {nid}")
        self.generar_indice()
        return nid

    def rechazar(self, pid: str, por: str, motivo: str) -> None:
        self.buscar_id(pid).unlink()
        self.registrar("rechazar", pid, None, por, motivo)

    def error(self, clave: str, resumen: str, evidencia: str, fuente: str = "agente") -> str:
        """Aprendizaje de errores: misma clave → suma una repetición en vez de duplicar."""
        for ruta, meta, cuerpo in self.notas(incluir_propuestas=True):
            if meta.get("tipo") == "error" and meta.get("clave") == clave and meta["estado"] != "obsoleta":
                self.validar_texto(evidencia)
                meta["veces"] = str(int(meta.get("veces", "1")) + 1)
                cuerpo = (cuerpo + f"\n- {hoy()}: {evidencia}").strip()
                texto = escribir_nota(ruta, meta, cuerpo)
                self.registrar("repetir", meta["id"], texto, fuente, f"veces={meta['veces']}")
                if int(meta["veces"]) >= UMBRAL_PROMOVER and meta["estado"] == "vigente":
                    print(f"SUGERENCIA: {meta['id']} se repitió {meta['veces']}×; conviértelo en regla "
                          f"de AGENTS.md y registra la versión con `mem.py version`.", file=sys.stderr)
                if meta["estado"] == "vigente":
                    self.generar_indice()
                return meta["id"]
        return self.proponer("error", resumen, fuente, evidencia, f"- {hoy()}: {evidencia}", clave=clave)

    def obsoletar(self, nid: str, por: str, motivo: str) -> None:
        ruta = self.buscar_id(nid)
        meta, cuerpo = leer_nota(ruta)
        meta["estado"] = "obsoleta"
        texto = escribir_nota(ruta, meta, cuerpo + f"\n\nObsoleta {hoy()}: {motivo}")
        self.registrar("obsoletar", nid, texto, por, motivo)
        self.generar_indice()

    def olvidar(self, nid: str, por: str) -> None:
        """Borrado por privacidad: el LOG guarda sólo el id, nunca el contenido."""
        self.buscar_id(nid).unlink()
        self.registrar("olvidar", nid, None, por, "borrado por privacidad (purga también el historial de git)")
        self.generar_indice()

    def sellar(self, nid: str, por: str, motivo: str) -> None:
        """Re-registra una nota editada a mano (tras revisarla)."""
        ruta = self.buscar_id(nid)
        self.validar_texto(ruta.read_text())
        leer_nota(ruta)
        self.registrar("sellar", nid, ruta.read_text(), por, motivo)
        self.generar_indice()

    def generar_indice(self) -> str:
        grupos: dict[str, list[str]] = {"regla": [], "error": [], "hecho": []}
        for _, meta, _ in self.notas():
            if meta["estado"] == "vigente":
                veces = f" ×{meta['veces']}" if meta["tipo"] == "error" else ""
                grupos[meta["tipo"]].append(f"- {meta['id']}{veces} {meta['resumen']}")
        titulos = {"regla": "Reglas", "error": "Errores aprendidos", "hecho": "Hechos"}
        partes = ["# Memoria del proyecto (generado por mem.py; no editar)",
                  "Detalle: `python3 mem.py ver <ID>` · búsqueda: `python3 mem.py buscar \"...\"`"]
        for t, lineas in grupos.items():
            if lineas:
                partes += ["", f"## {titulos[t]}", *lineas]
        texto = "\n".join(partes) + "\n"   # sin fechas: prefijo estable para el prompt cache
        self.indice.write_text(texto, encoding="utf-8")
        return texto

    # -- versiones de AGENTS.md
    def version(self, agents: Path, por: str, motivo: str, refs: str = "") -> str:
        for ref in filter(None, (r.strip() for r in refs.split(","))):
            self.buscar_id(ref)                       # falla antes de escribir nada
        texto = agents.read_text(encoding="utf-8")
        priv = escanear(texto, PRIVACIDAD, self.lista_local())
        if priv:
            raise SystemExit(f"rechazado por privacidad: {', '.join(priv)}")
        for h in escanear(texto, INYECCION):
            print(f"AVISO: patrón sospechoso en AGENTS.md ({h}); revísalo en el diff", file=sys.stderr)
        d = self.raiz / "agents"
        d.mkdir(parents=True, exist_ok=True)
        previas = sorted(d.glob("v*.md"))
        nueva = f"v{len(previas) + 1:03d}"
        if previas and previas[-1].read_text() == texto:
            raise SystemExit(f"sin cambios respecto a {previas[-1].stem}")
        shutil.copyfile(agents, d / f"{nueva}.md")
        resumen = resumen_transicion(previas[-1].read_text() if previas else "", texto)
        tabla = d / "TRANSICIONES.md"
        if not tabla.exists():
            tabla.write_text("# Transiciones de AGENTS.md\n\n| versión | fecha | líneas | secciones | por qué | refs |\n"
                             "|---|---|---|---|---|---|\n", encoding="utf-8")
        with tabla.open("a", encoding="utf-8") as f:
            f.write(f"| {nueva} | {hoy()} | {resumen['lineas']} | {resumen['secciones']} | "
                    f"{motivo.replace('|', '/')} | {refs or '-'} |\n")
        self.registrar("version", f"AGENTS-{nueva}", texto, por, motivo)
        for ref in filter(None, (r.strip() for r in refs.split(","))):
            meta, _ = leer_nota(self.buscar_id(ref))
            if meta["estado"] == "vigente":   # ya vive en AGENTS.md: no pagarla dos veces en tokens
                self.obsoletar(ref, por, f"promovida a AGENTS {nueva}")
        return nueva

    def lint(self) -> list[str]:
        problemas: list[str] = []
        shas = self.ultimo_sha()
        locales = self.lista_local()
        vistos: set[str] = set()
        for ruta, meta, cuerpo in self.notas(incluir_propuestas=True):
            nid = meta.get("id", ruta.name)
            faltan = [c for c in CAMPOS if c not in meta]
            if faltan:
                problemas.append(f"{nid}: faltan campos {faltan}")
                continue
            if nid in vistos:
                problemas.append(f"{nid}: id duplicado")
            vistos.add(nid)
            if meta["tipo"] not in TIPOS or meta["fuente"] not in FUENTES or meta["estado"] not in ESTADOS:
                problemas.append(f"{nid}: tipo/fuente/estado inválido")
            if len(meta["resumen"]) > MAX_RESUMEN:
                problemas.append(f"{nid}: resumen largo")
            if len(cuerpo.splitlines()) > MAX_CUERPO:
                problemas.append(f"{nid}: cuerpo > {MAX_CUERPO} líneas; divide o resume")
            if meta["tipo"] == "regla" and meta["fuente"] == "externo":
                problemas.append(f"{nid}: regla con fuente externa")
            if meta["estado"] != "propuesta" and not meta.get("aprobado"):
                problemas.append(f"{nid}: vigente sin aprobación humana")
            if shas.get(nid) != sha(ruta.read_text()):
                problemas.append(f"{nid}: editada fuera de mem.py (revisa y usa `sellar`)")
            if meta["estado"] == "vigente" and meta["revisar"] != "-" and meta["revisar"] < hoy():
                problemas.append(f"{nid}: revisión vencida ({meta['revisar']}); confirma u obsoleta")
        archivos = [p for p in self.raiz.rglob("*.md")]
        for p in archivos:
            t = p.read_text(encoding="utf-8")
            for h in escanear(t, PRIVACIDAD, locales):
                problemas.append(f"{p.relative_to(self.raiz)}: posible dato privado ({h})")
            if p.parent.name in ("notas", "propuestas"):
                for h in escanear(t, INYECCION):
                    problemas.append(f"{p.relative_to(self.raiz)}: posible inyección ({h})")
        if self.indice.exists():
            actual = self.indice.read_text()
            if actual != self.generar_indice():
                problemas.append("INDICE.md editado a mano (regenerado)")
            if tokens(actual) > PRESUPUESTO_INDICE:
                problemas.append(f"INDICE.md usa {tokens(actual)} > {PRESUPUESTO_INDICE} tokens; consolida")
        return problemas


# ---------------------------------------------------------------- transiciones
def secciones(texto: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {"(inicio)": []}
    actual = "(inicio)"
    for linea in texto.splitlines():
        if linea.startswith("#"):
            actual = linea.lstrip("# ").strip()
            out[actual] = []
        else:
            out[actual].append(linea)
    return {k: v for k, v in out.items() if k != "(inicio)" or any(x.strip() for x in v)}


def resumen_transicion(a: str, b: str) -> dict[str, str]:
    sa, sb = secciones(a), secciones(b)
    diff = list(difflib.ndiff(a.splitlines(), b.splitlines()))
    mas = sum(1 for x in diff if x.startswith("+ "))
    menos = sum(1 for x in diff if x.startswith("- "))
    cambios = [f"+{k}" for k in sb if k not in sa] + [f"−{k}" for k in sa if k not in sb]
    cambios += [f"~{k}" for k in sb if k in sa and sa[k] != sb[k]]
    return {"lineas": f"+{mas} −{menos}", "secciones": ", ".join(cambios) or "-"}


def transicion(a: str, b: str, contexto: int = 0) -> str:
    """Diff por secciones: sólo lo que cambió, para leerlo con pocos tokens."""
    sa, sb = secciones(a), secciones(b)
    out = []
    for k in list(dict.fromkeys([*sa, *sb])):
        if sa.get(k) == sb.get(k):
            continue
        marca = "+" if k not in sa else "−" if k not in sb else "~"
        out.append(f"{marca} ## {k}")
        for linea in difflib.unified_diff(sa.get(k, []), sb.get(k, []), n=contexto, lineterm=""):
            if not linea.startswith(("---", "+++", "@@")) and linea.strip("+- "):
                out.append("  " + linea)
    return "\n".join(out) or "(sin cambios)"


# ---------------------------------------------------------------- búsqueda (pull)
def slug(texto: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", texto.lower().translate(str.maketrans("áéíóúñü", "aeiounu"))).strip("-")
    return s[:40] or "nota"


def terminos(texto: str) -> list[str]:
    t = texto.lower().translate(str.maketrans("áéíóúñü", "aeiounu"))
    return [w for w in re.findall(r"[a-z0-9_]+", t) if len(w) > 1]


def bm25(docs: list[tuple[str, str]], consulta: str, k: int, k1: float = 1.5, b: float = 0.75):
    toks = {i: terminos(t) for i, t in docs}
    if not toks:
        return []
    prom = sum(map(len, toks.values())) / len(toks)
    df: dict[str, int] = {}
    for ts in toks.values():
        for w in set(ts):
            df[w] = df.get(w, 0) + 1
    res = []
    for i, ts in toks.items():
        s = 0.0
        for w in set(terminos(consulta)):
            if w in df:
                f = ts.count(w)
                idf = math.log(1 + (len(toks) - df[w] + 0.5) / (df[w] + 0.5))
                s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(ts) / max(prom, 1)))
        if s > 0:
            res.append((i, s))
    return sorted(res, key=lambda x: (-x[1], x[0]))[:k]


# ---------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="mem.py", description=__doc__.splitlines()[0])
    ap.add_argument("--raiz", type=Path, default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("proponer", help="el agente sugiere una nota (queda en cuarentena)")
    p.add_argument("--tipo", required=True, choices=sorted(TIPOS))
    p.add_argument("--resumen", required=True)
    p.add_argument("--fuente", required=True, choices=sorted(FUENTES))
    p.add_argument("--evidencia", required=True)
    p.add_argument("--cuerpo", default="")
    p.add_argument("--reemplaza", default="")
    for nombre in ("aprobar", "rechazar", "obsoletar", "olvidar", "sellar"):
        q = sub.add_parser(nombre)
        q.add_argument("id")
        q.add_argument("--por", default="humano")
        q.add_argument("--motivo", default="")
    e = sub.add_parser("error", help="registra un error; si la clave existe suma una repetición")
    e.add_argument("clave")
    e.add_argument("--resumen", required=True)
    e.add_argument("--evidencia", required=True)
    e.add_argument("--fuente", default="agente", choices=sorted(FUENTES))
    v = sub.add_parser("version", help="guarda una versión de AGENTS.md y su transición")
    v.add_argument("agents", type=Path)
    v.add_argument("--motivo", required=True)
    v.add_argument("--refs", default="")
    v.add_argument("--por", default="humano")
    t = sub.add_parser("transicion", help="qué cambió entre dos versiones de AGENTS.md")
    t.add_argument("desde")
    t.add_argument("hasta")
    s = sub.add_parser("buscar", help="BM25 sobre notas vigentes (y notas de benchmark)")
    s.add_argument("consulta")
    s.add_argument("k", nargs="?", type=int, default=5)
    w = sub.add_parser("ver")
    w.add_argument("id")
    n = sub.add_parser("nota", help="adaptador memeval: guarda texto crudo con id numérico")
    n.add_argument("id")
    n.add_argument("texto")
    sub.add_parser("indice")
    sub.add_parser("contexto", help="imprime lo que se empuja al prompt y su costo")
    sub.add_parser("lint")
    a = ap.parse_args(argv)
    m = Memoria(a.raiz or raiz_por_defecto())

    if a.cmd == "proponer":
        print(m.proponer(a.tipo, a.resumen, a.fuente, a.evidencia, a.cuerpo, reemplaza=a.reemplaza))
    elif a.cmd == "aprobar":
        print(m.aprobar(a.id, a.por, a.motivo))
    elif a.cmd == "rechazar":
        m.rechazar(a.id, a.por, a.motivo or "rechazada")
    elif a.cmd == "obsoletar":
        m.obsoletar(a.id, a.por, a.motivo or "ya no aplica")
    elif a.cmd == "olvidar":
        m.olvidar(a.id, a.por)
    elif a.cmd == "sellar":
        m.sellar(a.id, a.por, a.motivo or "edición manual revisada")
    elif a.cmd == "error":
        print(m.error(a.clave, a.resumen, a.evidencia, a.fuente))
    elif a.cmd == "version":
        print(m.version(a.agents, a.por, a.motivo, a.refs))
    elif a.cmd == "transicion":
        d = m.raiz / "agents"
        print(transicion((d / f"{a.desde}.md").read_text(), (d / f"{a.hasta}.md").read_text()))
    elif a.cmd == "buscar":
        docs = [(meta["id"], f"{meta['resumen']} {meta.get('clave', '')} {c}") for _, meta, c in m.notas()
                if meta["estado"] == "vigente"]
        banco = m.raiz / "notas.jsonl"
        if banco.exists():
            docs += [(str(r["id"]), r["texto"]) for r in map(json.loads, banco.read_text().splitlines())]
        resumen = {meta["id"]: meta["resumen"] for _, meta, _ in m.notas()}
        for i, s in bm25(docs, a.consulta, a.k):
            print(f"{i}\t{s:.3f}\t{resumen.get(i, '')}".rstrip())
    elif a.cmd == "ver":
        print(m.buscar_id(a.id).read_text(), end="")
    elif a.cmd == "nota":
        m.raiz.mkdir(parents=True, exist_ok=True)
        with (m.raiz / "notas.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps({"id": a.id, "texto": a.texto}, ensure_ascii=False) + "\n")
    elif a.cmd == "indice":
        print(m.generar_indice(), end="")
    elif a.cmd == "contexto":
        texto = m.generar_indice()
        print(texto, end="")
        print(f"\n[≈{tokens(texto)} tokens de {PRESUPUESTO_INDICE}]", file=sys.stderr)
    elif a.cmd == "lint":
        problemas = m.lint()
        for x in problemas:
            print("✗", x)
        print("ok" if not problemas else f"{len(problemas)} problema(s)")
        return 1 if problemas else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
