"""The only contract a benchmark sees. Adapters never import each other."""
from __future__ import annotations

import importlib
import os
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Protocol


class Harness(Protocol):
    name: str
    model: str

    def ask(self, prompt: str) -> str:
        """Send one self-contained prompt, return the final text answer."""


@dataclass
class CliHarness:
    """Shared helper: run a CLI once, in an empty temp dir, with the prompt on stdin."""

    name: str
    model: str
    timeout: int = 600

    def command(self) -> list[str]:  # overridden per adapter
        raise NotImplementedError

    def env(self) -> dict[str, str]:
        return dict(os.environ)

    def parse(self, stdout: str) -> str:
        return stdout.strip()

    def ask(self, prompt: str) -> str:
        with tempfile.TemporaryDirectory(prefix="membench-") as cwd:
            out = subprocess.run(
                self.command(), input=prompt, capture_output=True, text=True,
                cwd=cwd, env=self.env(), timeout=self.timeout,
            )
        if out.returncode != 0:
            raise RuntimeError(f"{self.name} exited {out.returncode}: {out.stderr[-500:]}")
        return self.parse(out.stdout)


def load(spec: str) -> Harness:
    """'claude_code:haiku' -> harnesses.claude_code.make('haiku')."""
    module, _, model = spec.partition(":")
    return importlib.import_module(f"harnesses.{module}").make(model)
