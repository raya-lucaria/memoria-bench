"""Pruebas sin Docker: esquema de tareas y corrección funcional a escala chica.

A escala chica todas las variantes (workspace original, oracle, naive) deben dar
el resultado CORRECTO: lo que las separa es solo la memoria, y eso lo verifica
`python3 -m bench validate` con Docker a escala real.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from bench.task import discover, parse_mem_mb

REPO = Path(__file__).resolve().parent.parent
TASKS = discover(REPO / "tasks")

try:
    import numpy  # noqa: F401
    HAVE_NUMPY = True
except ImportError:
    HAVE_NUMPY = False


class SchemaTest(unittest.TestCase):
    def test_parse_mem(self):
        self.assertEqual(parse_mem_mb("96m"), 96)
        self.assertEqual(parse_mem_mb("2g"), 2048)
        self.assertEqual(parse_mem_mb(300), 300)

    def test_tasks_load(self):
        self.assertGreaterEqual(len(TASKS), 3)
        for t in TASKS:
            self.assertEqual(t.grading.network, "none")
            self.assertLess(t.grading.memory_mb, t.agent.memory_mb)


def _run(cmd, cwd, env):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=300)


@unittest.skipUnless(HAVE_NUMPY, "numpy no instalado")
class SmallScaleTest(unittest.TestCase):
    def _variant(self, task, variant):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            ws = tmp / "workspace"
            shutil.copytree(task.path / "workspace", ws)
            for d in ("data", "expected", "results"):
                (tmp / d).mkdir()
            env = dict(os.environ, BENCH_SEED="12345", BENCH_SCALE="0.01", BENCH_DATA=str(tmp / "data"),
                       BENCH_EXPECTED=str(tmp / "expected"), BENCH_RESULTS=str(tmp / "results"))
            if variant != "null":
                r = _run(["bash", str(task.path / variant / "solve.sh")], ws, env)
                self.assertEqual(r.returncode, 0, r.stderr)
            r = _run([sys.executable, str(task.path / "tests" / "prepare.py")], tmp, env)
            self.assertEqual(r.returncode, 0, r.stderr)
            # solve.sh usa /workspace; aquí lo reemplazamos por la copia temporal
            script = (task.path / "tests" / "solve.sh").read_text().replace("/workspace", str(ws))
            r = _run(["bash", "-c", script], ws, env)
            self.assertEqual(r.returncode, 0, r.stderr)
            r = _run([sys.executable, str(task.path / "tests" / "check.py")], tmp, env)
            self.assertEqual(r.returncode, 0, f"{task.id}/{variant}: {r.stdout}{r.stderr}")

    def test_all_variants_correct_at_small_scale(self):
        for t in TASKS:
            for v in ("null", "solution", "naive"):
                if v == "naive" and not t.has_naive:
                    continue
                with self.subTest(task=t.id, variant=v):
                    self._variant(t, v)


if __name__ == "__main__":
    unittest.main()
