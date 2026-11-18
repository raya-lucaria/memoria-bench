"""Pruebas. Se corren con:  python3 -m unittest discover -s tests -p pruebas.py"""
import ast
import contextlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

from memprobe import corrida, respuestas
from memprobe.cli import main
from memprobe.generate import ABILITIES, FINAL_ONLY, UNKNOWN, generate_episode
from memprobe.kit import TIERS, build_kit
from memprobe.runner import Sut, run_episode
from memprobe.score import norm, piso, score_one, summarize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = [sys.executable, os.path.join(ROOT, "examples", "reference-sut.py")]
NULL = [sys.executable, os.path.join(ROOT, "examples", "null-sut.py")]
FMT = {"valor": "value", "lista": "list", "conteo": "count"}


def correr(argv, ep):
    r = run_episode(argv, ep, timeout=30)
    items = [(q, score_one(q.fmt, q.gold, a), a) for q, a in zip(ep.questions, r.answers)]
    return r, summarize(items, boot=0)


def cli(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(args))
    return code, out.getvalue(), err.getvalue()


def leer_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def agente_simulado(kit_dir, destino, argv=REF):
    """Hace de 'agente': lee SOLO los archivos del kit, ingiere sesiones y responde preguntas."""
    sut = Sut(argv, 30)
    try:
        sesiones = sorted(os.listdir(os.path.join(kit_dir, "fase-1-sesiones")))
        pregs = {}
        for fn in sorted(os.listdir(os.path.join(kit_dir, "fase-2-preguntas"))):
            pregs.setdefault(int(re.match(r"preguntas-tras-sesion-(\d+)", fn).group(1)), []).append(fn)
        lineas = []
        for fn in sesiones:
            k = int(re.match(r"sesion-(\d+)\.md", fn).group(1))
            with open(os.path.join(kit_dir, "fase-1-sesiones", fn), encoding="utf-8") as f:
                cuerpo = f.read()
            bloque = cuerpo.split("```text\n", 1)[1].split("\n```", 1)[0]
            for linea in bloque.split("\n"):
                sut.call({"op": "ingest", "text": linea})
            for pf in pregs.get(k, []):
                with open(os.path.join(kit_dir, "fase-2-preguntas", pf), encoding="utf-8") as f:
                    for ln in f:
                        m = re.match(r"- \*\*id (\d+)\*\* \((valor|lista|conteo)\): (.*)$", ln.rstrip("\n"))
                        if m:
                            r = sut.call({"op": "query", "q": m.group(3), "format": FMT[m.group(2)]})
                            lineas.append(json.dumps({"id": int(m.group(1)), "answer": r["answer"]}))
        with open(destino, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas) + "\n")
    finally:
        sut.close()


def tarjeta_valida(manifest, **cambios):
    c = corrida.plantilla(manifest)
    c.update({"harness": "claude-code", "harness_version": "no-se", "modelo": "no-se", "suscripcion": "no-se",
              "memoria_id": "ninguna", "memoria_version": "no-se", "condicion": "ninguna", "memoria_nativa": "desactivada",
              "aislamiento": "si", "repeticion": 1, "fecha": "2026-11-17", "sistema_operativo": "macos"})
    c.update(cambios)
    return c


class Determinismo(unittest.TestCase):
    # Si cambias el generador a propósito: sube BENCH_VERSION y actualiza estos ids.
    # Entonces los resultados nuevos y viejos dejan de ser comparables.
    GOLDEN = {"prose": "31085fd6ec10a2ca", "code": "4e4912ac5a74c864"}

    def test_ids_dorados(self):
        for pista, esperado in self.GOLDEN.items():
            self.assertEqual(generate_episode(pista, 1, 300, 70).dataset_id, esperado)

    def test_repetible(self):
        a, b = generate_episode("prose", 7, 400, 70), generate_episode("prose", 7, 400, 70)
        self.assertEqual(a.events, b.events)
        self.assertEqual(a.questions, b.questions)

    def test_eventos_no_dependen_del_numero_de_preguntas(self):
        a, b = generate_episode("code", 3, 400, 70), generate_episode("code", 3, 400, 140)
        self.assertEqual(a.events, b.events)

    def test_pistas_comparten_hechos(self):
        p, c = generate_episode("prose", 2, 500, 70), generate_episode("code", 2, 500, 70)
        self.assertNotEqual(p.events, c.events)
        self.assertEqual(p.questions, c.questions)

    def test_cada_tier_cubre_las_siete_habilidades_en_muchas_semillas(self):
        for tier, (ns, per, nq) in TIERS.items():
            for seed in range(1, 31):
                ep = generate_episode("prose", seed, ns * per, nq, FINAL_ONLY)
                for ab in ABILITIES:
                    n = sum(q.ability == ab for q in ep.questions)
                    self.assertGreaterEqual(n, nq // 7, "%s semilla %d habilidad %s" % (tier, seed, ab))

    def test_gold_valido(self):
        for q in generate_episode("prose", 1, 2000, 140).questions:
            self.assertTrue(q.gold)
            if q.ability in ("abstain", "forget"):
                self.assertEqual(q.gold, UNKNOWN)


class Puntuacion(unittest.TestCase):
    def test_norm(self):
        self.assertEqual(norm('  "Foo  Bar". '), "foo bar")

    def test_lista_f1(self):
        self.assertEqual(score_one("list", ["a", "b"], ["B", "a"]), 1.0)
        self.assertAlmostEqual(score_one("list", ["a", "b"], ["a"]), 2 / 3)
        self.assertEqual(score_one("list", ["a"], ["z"]), 0.0)
        self.assertEqual(score_one("list", ["a", "b"], "a, b"), 1.0)

    def test_conteo_y_valor(self):
        self.assertEqual(score_one("count", "3", 3), 1.0)
        self.assertEqual(score_one("count", "3", "tres"), 0.0)
        self.assertEqual(score_one("value", "7", 7), 1.0)
        self.assertEqual(score_one("value", "x", None), 0.0)

    def test_piso_es_macro_de_siempre_unknown(self):
        ep = generate_episode("prose", 1, 600, 70)
        self.assertAlmostEqual(piso(ep.questions), 2 / 7, places=6)


class RunnerStdio(unittest.TestCase):
    def test_referencia_perfecta(self):
        for pista in ("prose", "code", "mixed"):
            _, s = correr(REF, generate_episode(pista, 1, 600, 70))
            self.assertEqual(s["macro"], 1.0, pista)

    def test_null_solo_pasa_abstencion(self):
        _, s = correr(NULL, generate_episode("prose", 1, 600, 70))
        for ab in ABILITIES:
            self.assertEqual(s["abilities"][ab]["score"], 1.0 if ab in ("abstain", "forget") else 0.0, ab)

    def test_ablaciones_dañan_la_habilidad_correcta(self):
        ep = generate_episode("prose", 1, 1500, 140)
        for flag, hab in {"--no-forget": "forget", "--first-write-wins": "update", "--no-history": "temporal"}.items():
            _, s = correr(REF + [flag], ep)
            self.assertLess(s["abilities"][hab]["score"], 0.5, flag)
        _, s = correr(REF + ["--window", "300"], ep)
        self.assertLess(s["abilities"]["recall"]["score"], 0.9)
        self.assertGreater(s["age"]["<10%"]["score"], s["age"][">50%"]["score"])

    def test_caida_se_puntua_no_lanza(self):
        r, s = correr([sys.executable, "-c", "import sys; sys.exit(0)"], generate_episode("prose", 1, 300, 70))
        self.assertIsNotNone(r.crashed)
        self.assertTrue(all(a is None for a in r.answers))
        self.assertEqual(s["macro"], 0.0)

    def test_ejecutable_inexistente(self):
        r = run_episode(["/no/existe/este/programa"], generate_episode("prose", 1, 300, 70))
        self.assertIsNotNone(r.crashed)


class Kit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def hacer(self, **kw):
        salida = os.path.join(self.tmp, kw.pop("nombre", "k"))
        args = dict(tier="chico", track="prose", seed=1, out=salida)
        args.update(kw)
        return build_kit(**args), salida

    def test_estructura_y_sin_gold_en_el_kit(self):
        m, salida = self.hacer()
        kit = os.path.join(salida, "kit")
        self.assertTrue(os.path.exists(os.path.join(salida, "gold.jsonl")))
        archivos = [os.path.join(r, f) for r, _d, fs in os.walk(kit) for f in fs]
        self.assertFalse([a for a in archivos if "gold" in os.path.basename(a)])
        for a in archivos:
            with open(a, encoding="utf-8") as f:
                self.assertNotIn('"gold"', f.read())
        self.assertEqual(len(os.listdir(os.path.join(kit, "fase-1-sesiones"))), TIERS["chico"][0])

    def test_sesiones_son_el_flujo_completo_sin_perdida(self):
        m, salida = self.hacer()
        ep = generate_episode("prose", 1, m["eventos"], m["preguntas"], FINAL_ONLY)
        texto = []
        for fn in sorted(os.listdir(os.path.join(salida, "kit", "fase-1-sesiones"))):
            with open(os.path.join(salida, "kit", "fase-1-sesiones", fn), encoding="utf-8") as f:
                texto += f.read().split("```text\n", 1)[1].split("\n```", 1)[0].split("\n")
        self.assertEqual(texto, ep.events)
        self.assertEqual(m["dataset_id"], ep.dataset_id)

    def test_kit_es_reproducible_y_kit_id_estable(self):
        a, _ = self.hacer(nombre="a")
        b, _ = self.hacer(nombre="b")
        self.assertEqual(a["kit_id"], b["kit_id"])
        c, _ = self.hacer(nombre="c", seed=2)
        self.assertNotEqual(a["kit_id"], c["kit_id"])

    def test_no_sobrescribe(self):
        _, salida = self.hacer()
        with self.assertRaises(FileExistsError):
            build_kit("chico", "prose", 1, salida)

    def test_agente_simulado_perfecto_y_piso(self):
        for pista in ("prose", "code"):
            m, salida = self.hacer(nombre=pista, track=pista)
            resp = os.path.join(self.tmp, pista + ".jsonl")
            agente_simulado(os.path.join(salida, "kit"), resp)
            code, out, _ = cli("puntuar", "--dir", salida, "--respuestas", resp, "--sin-corrida")
            self.assertEqual(code, 0)
            self.assertRegex(out, r"MACRO\s+100\.0%")
            self.assertIn("no oficial", out)
        # un agente que no recuerda nada (siempre UNKNOWN) cae exactamente en el piso
        m, salida = self.hacer(nombre="nulo")
        resp = os.path.join(self.tmp, "nulo.jsonl")
        with open(resp, "w") as f:
            for i in range(m["preguntas"]):
                f.write(json.dumps({"id": i, "answer": "UNKNOWN"}) + "\n")
        _, out, _ = cli("puntuar", "--dir", salida, "--respuestas", resp, "--sin-corrida")
        self.assertRegex(out, r"MACRO\s+%.1f%%" % (100 * m["piso_macro"]))

    def test_varios_checkpoints_y_lotes(self):
        m, salida = self.hacer(checkpoints=(0.5, 1.0), lote=10)
        per = m["eventos_por_sesion"]
        self.assertEqual(len(m["checkpoints_eventos"]), 2)
        for c in m["checkpoints_eventos"]:
            self.assertEqual(c % per, 0)
        self.assertTrue(all("lote" in a for a in m["archivos_preguntas"]))
        resp = os.path.join(self.tmp, "r.jsonl")
        agente_simulado(os.path.join(salida, "kit"), resp)
        code, out, _ = cli("puntuar", "--dir", salida, "--respuestas", resp, "--sin-corrida")
        self.assertRegex(out, r"MACRO\s+100\.0%")


class TarjetaYRespuestas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.m = build_kit("chico", "prose", 1, os.path.join(self.tmp, "k"))
        self.salida = os.path.join(self.tmp, "k")

    def escribir(self, nombre, obj):
        p = os.path.join(self.tmp, nombre)
        with open(p, "w", encoding="utf-8") as f:
            f.write(obj if isinstance(obj, str) else json.dumps(obj))
        return p

    def test_tarjeta_valida(self):
        err, _ = corrida.validar(tarjeta_valida(self.m), self.m)
        self.assertEqual(err, [])

    def test_plantilla_sin_llenar_se_rechaza(self):
        err, _ = corrida.validar(corrida.plantilla(self.m), self.m)
        self.assertTrue(any("falta" in e for e in err))

    def test_privacidad_y_valores(self):
        ruta = "/Us" + "ers/alguien/proyecto"
        correo = "alguien" + "@" + "ejemplo.com"
        llave = "sk-" + "abcdefghijklmnop"
        for campo, valor in (("modelo", ruta), ("suscripcion", correo), ("memoria_version", llave)):
            err, _ = corrida.validar(tarjeta_valida(self.m, **{campo: valor}), self.m)
            self.assertTrue(any("dato personal" in e for e in err), campo)
        err, _ = corrida.validar(tarjeta_valida(self.m, condicion="otra"), self.m)
        self.assertTrue(any("condicion" in e for e in err))
        err, _ = corrida.validar(tarjeta_valida(self.m, harness="no-se"), self.m)
        self.assertTrue(err)
        err, _ = corrida.validar(tarjeta_valida(self.m, kit_id="0000"), self.m)
        self.assertTrue(any("kit_id" in e for e in err))

    def test_puntuar_exige_corrida_y_la_valida(self):
        resp = self.escribir("r.jsonl", "")
        code, _, err = cli("puntuar", "--dir", self.salida, "--respuestas", resp)
        self.assertEqual(code, 2)
        mala = self.escribir("mala.json", tarjeta_valida(self.m, modelo="/Us" + "ers/x/y"))
        code, _, err = cli("puntuar", "--dir", self.salida, "--respuestas", resp, "--corrida", mala)
        self.assertEqual(code, 2)
        self.assertIn("dato personal", err)
        buena = self.escribir("buena.json", tarjeta_valida(self.m))
        code, out, _ = cli("puntuar", "--dir", self.salida, "--respuestas", resp, "--corrida", buena)
        self.assertEqual(code, 0)

    def test_lectura_estricta_de_respuestas(self):
        p = self.escribir("r.jsonl", "\n".join([
            "```json", '{"id": 0, "answer": "x"}', "no es json", '{"id": 0, "answer": "y"}',
            '{"id": 999, "answer": "z"}', '{"answer": "sin id"}', '{"id": true, "answer": 1}', "```"]))
        ans, info = respuestas.leer([p], 42)
        self.assertEqual(ans, {0: "y"})
        self.assertEqual((info["invalidas"], info["duplicadas"], info["ids_fuera_de_rango"]), (3, 1, 1))
        self.assertEqual(info["sin_respuesta"], 41)
        self.assertTrue(all(os.sep not in d.split(":")[0] for d in info["detalle"]))  # solo nombre, no ruta
        code, out, _ = cli("revisar-respuestas", "--dir", self.salida, "--respuestas", p)
        self.assertEqual(code, 1)

    def test_comparar_empareja_por_dataset_y_rechaza_distintos(self):
        resp_ref = os.path.join(self.tmp, "ref.jsonl")
        agente_simulado(os.path.join(self.salida, "kit"), resp_ref)
        resp_nulo = self.escribir("nulo.jsonl", "".join(
            json.dumps({"id": i, "answer": "UNKNOWN"}) + "\n" for i in range(self.m["preguntas"])))
        a = os.path.join(self.tmp, "a.json")
        b = os.path.join(self.tmp, "b.json")
        ca = self.escribir("ca.json", tarjeta_valida(self.m, condicion="ninguna"))
        cb = self.escribir("cb.json", tarjeta_valida(self.m, condicion="memoria", memoria_id="notas"))
        cli("puntuar", "--dir", self.salida, "--respuestas", resp_nulo, "--corrida", ca, "--salida", a)
        cli("puntuar", "--dir", self.salida, "--respuestas", resp_ref, "--corrida", cb, "--salida", b)
        code, out, _ = cli("comparar", "--a", a, "--b", b)
        self.assertEqual(code, 0)
        self.assertIn("B gana en 1 de 1 semillas", out)
        self.assertIn("menos de 3 semillas", out)
        # otro seed => otro dataset_id => no hay nada en común
        m2 = build_kit("chico", "prose", 2, os.path.join(self.tmp, "k2"))
        c2 = self.escribir("c2.json", tarjeta_valida(m2))
        r2 = self.escribir("r2.jsonl", "")
        b2 = os.path.join(self.tmp, "b2.json")
        cli("puntuar", "--dir", os.path.join(self.tmp, "k2"), "--respuestas", r2, "--corrida", c2, "--salida", b2)
        code, _, err = cli("comparar", "--a", a, "--b", b2)
        self.assertEqual(code, 2)
        self.assertIn("ningún dataset_id", err)


class Higiene(unittest.TestCase):
    """Reglas del repo memoria-bench: nada personal, nombres en kebab-case, sin red ni modelos."""

    def archivos(self):
        for r, dirs, fs in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
            for f in fs:
                yield os.path.join(r, f)

    def test_solo_stdlib_sin_red_ni_ml(self):
        prohibidos = {"socket", "urllib", "http", "requests", "ssl", "openai", "anthropic",
                      "numpy", "torch", "sklearn", "transformers", "yaml"}
        for p in self.archivos():
            if not p.endswith(".py"):
                continue
            with open(p, encoding="utf-8") as f:
                arbol = ast.parse(f.read())
            for nodo in ast.walk(arbol):
                nombres = []
                if isinstance(nodo, ast.Import):
                    nombres = [a.name for a in nodo.names]
                elif isinstance(nodo, ast.ImportFrom) and nodo.module and nodo.level == 0:
                    nombres = [nodo.module]
                for n in nombres:
                    self.assertNotIn(n.split(".")[0], prohibidos, "%s importa %s" % (p, n))

    def test_sin_datos_personales_en_ningun_archivo(self):
        patrones = [re.compile("/Us" + r"ers/[^\s\"']+"), re.compile("/ho" + r"me/[^\s\"']+"),
                    re.compile(r"[\w.+-]+" + "@" + r"[\w-]+\.[a-z]{2,}"), re.compile(r"\b(sk-|ghp_)[A-Za-z0-9_-]{8,}")]
        for p in self.archivos():
            if p.endswith((".pyc",)):
                continue
            with open(p, encoding="utf-8") as f:
                texto = f.read()
            for rx in patrones:
                self.assertIsNone(rx.search(texto), "%s contiene %s" % (p, rx.pattern))

    def test_nombres_en_kebab_case_y_sin_basura(self):
        kebab = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z]+)?$")
        permitidos = {"__init__.py", "__main__.py", "README.md", ".gitignore"}
        for p in self.archivos():
            f = os.path.basename(p)
            self.assertNotIn(f, {".DS_Store", ".env"})
            self.assertTrue(f in permitidos or kebab.match(f), "nombre no kebab-case: %s" % p)

    def test_tamano_razonable(self):
        total = sum(os.path.getsize(p) for p in self.archivos())
        self.assertLess(total, 1_000_000)


if __name__ == "__main__":
    unittest.main()
