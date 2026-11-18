"""Codex CLI, headless, with a ChatGPT login (no API key).
UNTESTED: codex is not installed on this machine. `exec -` reads the prompt from stdin.
"""
from harnesses.base import CliHarness


class Codex(CliHarness):
    def command(self):
        cmd = ["codex", "exec", "--skip-git-repo-check", "-"]
        return cmd[:2] + (["-m", self.model] if self.model else []) + cmd[2:]


def make(model: str = ""):
    return Codex(name="codex", model=model)
