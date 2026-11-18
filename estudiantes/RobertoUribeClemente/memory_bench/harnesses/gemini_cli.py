"""Gemini CLI, headless, with a Google account login (no API key).
UNTESTED: gemini is not installed on this machine. `-p ""` makes it read stdin.
"""
from harnesses.base import CliHarness


class GeminiCli(CliHarness):
    def command(self):
        return ["gemini", "-m", self.model, "-p", ""]


def make(model: str = "gemini-2.5-flash"):
    return GeminiCli(name="gemini_cli", model=model or "gemini-2.5-flash")
