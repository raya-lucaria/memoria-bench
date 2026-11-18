"""Carga y valida tareas (tasks/<id>/task.toml)."""
from __future__ import annotations

import fnmatch
import re
import tomllib
from dataclasses import dataclass, replace
from pathlib import Path

CATEGORIES = {"paralelo", "concurrencia", "race", "deadlock", "memoria", "docker", "analisis"}
REQUIRED = [
    "prompt.md",
    "workspace",
    "tests/prepare.py",
    "tests/solve.sh",
    "tests/check.py",
    "solution/solve.sh",
]
_SIZE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*([kmgKMG])?[bB]?\s*$")


def parse_mem_mb(value) -> int:
    """'512m' -> 512, '2g' -> 2048, 300 -> 300 (MB)."""
    if isinstance(value, (int, float)):
        return int(value)
    m = _SIZE.match(str(value))
    if not m:
        raise ValueError(f"tamaño de memoria inválido: {value!r}")
    n, unit = float(m.group(1)), (m.group(2) or "m").lower()
    return int({"k": n / 1024, "m": n, "g": n * 1024}[unit])


@dataclass(frozen=True)
class Limits:
    timeout_s: int
    cpus: float
    memory_mb: int
    network: str = "none"
    pids: int = 256
    tmpfs_mb: int = 16

    def merged(self, d: dict | None) -> "Limits":
        if not d:
            return self
        kw = {}
        for key, val in d.items():
            if key == "memory":
                kw["memory_mb"] = parse_mem_mb(val)
            elif key == "tmpfs":
                kw["tmpfs_mb"] = parse_mem_mb(val)
            elif key in {"timeout_s", "pids"}:
                kw[key] = int(val)
            elif key == "cpus":
                kw[key] = float(val)
            elif key == "network":
                kw[key] = str(val)
            else:
                raise ValueError(f"clave de límites desconocida: {key}")
        return replace(self, **kw)


# Fases: prepare (genera datos + esperado), agent, grading (solución medida), check.
DEFAULTS = {
    "prepare": Limits(timeout_s=300, cpus=1, memory_mb=1024, pids=64),
    "agent": Limits(timeout_s=900, cpus=2, memory_mb=2048, tmpfs_mb=256),
    "grading": Limits(timeout_s=120, cpus=1, memory_mb=512),
    "check": Limits(timeout_s=60, cpus=1, memory_mb=256, pids=64),
}


@dataclass(frozen=True)
class Expect:
    null: str = "fail"          # el agente que no hace nada debe fallar
    naive: str = "fail"         # fail | oom | timeout | skip
    oracle_max_mem_frac: float = 0.7  # pico del oráculo <= 70 % del límite


@dataclass(frozen=True)
class Task:
    id: str
    path: Path
    title: str
    category: str
    difficulty: int
    prepare: Limits
    agent: Limits
    grading: Limits
    check: Limits
    repeats: int
    expect: Expect

    @property
    def prompt_path(self) -> Path:
        return self.path / "prompt.md"

    @property
    def has_naive(self) -> bool:
        return (self.path / "naive" / "solve.sh").is_file()

    @property
    def dockerfile(self) -> Path | None:
        p = self.path / "Dockerfile"
        return p if p.is_file() else None


class TaskError(ValueError):
    pass


def load_task(path: Path) -> Task:
    path = path.resolve()
    cfg_file = path / "task.toml"
    if not cfg_file.is_file():
        raise TaskError(f"{path.name}: falta task.toml")
    cfg = tomllib.loads(cfg_file.read_text(encoding="utf-8"))
    missing = [r for r in REQUIRED if not (path / r).exists()]
    if missing:
        raise TaskError(f"{path.name}: faltan {', '.join(missing)}")
    tid = cfg.get("id", path.name)
    if tid != path.name:
        raise TaskError(f"{path.name}: id '{tid}' no coincide con el directorio")
    category = cfg.get("category", "")
    if category not in CATEGORIES:
        raise TaskError(f"{tid}: categoría '{category}' no está en {sorted(CATEGORIES)}")
    lim = {k: DEFAULTS[k].merged(cfg.get(k)) for k in DEFAULTS}
    for phase in ("prepare", "grading", "check"):
        if lim[phase].network != "none":
            raise TaskError(f"{tid}: [{phase}] debe usar network = 'none'")
    exp = cfg.get("expect", {})
    expect = Expect(
        null=exp.get("null", "fail"),
        naive=exp.get("naive", "fail" if (path / "naive").exists() else "skip"),
        oracle_max_mem_frac=float(exp.get("oracle_max_mem_frac", 0.7)),
    )
    if expect.naive not in {"fail", "oom", "timeout", "skip"}:
        raise TaskError(f"{tid}: expect.naive inválido: {expect.naive}")
    return Task(
        id=tid,
        path=path,
        title=cfg.get("title", tid),
        category=category,
        difficulty=int(cfg.get("difficulty", 1)),
        prepare=lim["prepare"],
        agent=lim["agent"],
        grading=lim["grading"],
        check=lim["check"],
        repeats=int(cfg.get("repeats", 1)),
        expect=expect,
    )


def discover(root: Path, patterns: list[str] | None = None) -> list[Task]:
    tasks = []
    for d in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))):
        if patterns and not any(fnmatch.fnmatch(d.name, pat) for pat in patterns):
            continue
        tasks.append(load_task(d))
    return tasks
