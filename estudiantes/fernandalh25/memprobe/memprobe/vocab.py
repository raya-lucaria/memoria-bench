"""Invented words.

Every entity name and value is a made-up word (e.g. "Brakelor"). A system under
test therefore cannot answer from pretraining/world knowledge or by guessing:
the only source of truth is what it was told in the stream.

Some words get one-letter "twins" (Brakelor / Brakilor) to punish fuzzy
matching, which is a common silent failure of memory layers.
"""
from __future__ import annotations

from .rng import Rng

ONSETS = ["b", "br", "c", "d", "dr", "f", "g", "gl", "h", "j", "k", "kl", "l", "m",
          "n", "p", "pr", "r", "s", "sk", "st", "t", "tr", "v", "w", "z", "th", "sh"]
VOWELS = ["a", "e", "i", "o", "u"]
CODAS = ["", "", "", "n", "r", "l", "s", "m", "k"]
_VOW = set("aeiou")
_CONS = "bcdfghjklmnprstvwz"


class Words:
    def __init__(self, rng: Rng):
        self.rng = rng
        self.used: set = set()

    def new(self, syllables: int = 3) -> str:
        while True:
            w = "".join(
                self.rng.choice(ONSETS) + self.rng.choice(VOWELS) + self.rng.choice(CODAS)
                for _ in range(syllables)
            )
            if len(w) >= 6 and w not in self.used:
                self.used.add(w)
                return w

    def twin(self, w: str):
        """A word at edit distance 1 from `w` (same letter class), or None."""
        positions = self.rng.sample(range(1, len(w) - 1), len(w) - 2)
        for i in positions:
            c = w[i]
            alphabet = "aeiou" if c in _VOW else _CONS
            options = [x for x in alphabet if x != c]
            self.rng.shuffle(options)
            for x in options:
                t = w[:i] + x + w[i + 1:]
                if t not in self.used:
                    self.used.add(t)
                    return t
        return None
