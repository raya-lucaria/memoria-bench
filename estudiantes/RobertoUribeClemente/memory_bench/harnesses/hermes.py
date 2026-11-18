"""Hermes Agent, one-shot. Needs a provider logged in without a key, e.g. the
ChatGPT/Codex OAuth login (`hermes model` -> OpenAI Codex). Claude subscriptions
are not accepted by Hermes. --ignore-rules skips AGENTS.md/SOUL context files.
"""
from harnesses.base import CliHarness


class Hermes(CliHarness):
    def command(self):
        cmd = ["hermes", "chat", "-Q", "--ignore-rules", "--query-file", "-"]
        return cmd + (["-m", self.model] if self.model else [])


def make(model: str = ""):
    return Hermes(name="hermes", model=model)
