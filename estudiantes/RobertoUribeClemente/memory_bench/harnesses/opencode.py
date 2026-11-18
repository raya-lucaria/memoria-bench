"""opencode, headless, with its free Zen models or an OAuth login (no API key)."""
import json

from harnesses.base import CliHarness


class OpenCode(CliHarness):
    def command(self):
        # With no message argument, `opencode run` takes the prompt from stdin.
        return ["opencode", "run", "--pure", "--format", "json", "-m", self.model]

    def parse(self, stdout: str) -> str:
        parts = []
        for line in stdout.splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            part = ev.get("part") or {}
            if ev.get("type") == "text" and part.get("text"):
                parts.append(part["text"])
        return "".join(parts).strip()


def make(model: str = "opencode/deepseek-v4.1-flash-free"):
    if model and "/" not in model:
        model = f"opencode/{model}"
    return OpenCode(name="opencode", model=model or "opencode/deepseek-v4.1-flash-free")
