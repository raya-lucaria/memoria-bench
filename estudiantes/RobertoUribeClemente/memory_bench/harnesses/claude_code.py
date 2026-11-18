"""Claude Code, headless, on the user's subscription (no API key).

Tools, settings, MCP, session files and auto memory are all off, so the harness
answers only from the prompt the benchmark gives it.
"""
from harnesses.base import CliHarness


class ClaudeCode(CliHarness):
    def command(self):
        return ["claude", "-p", "--model", self.model, "--tools", "",
                "--setting-sources", "", "--strict-mcp-config",
                "--no-session-persistence"]

    def env(self):
        e = super().env()
        e["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
        e.pop("ANTHROPIC_API_KEY", None)  # force the subscription login
        return e


def make(model: str = "haiku"):
    return ClaudeCode(name="claude_code", model=model or "haiku")
