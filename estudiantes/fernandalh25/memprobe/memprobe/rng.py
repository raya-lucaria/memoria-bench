"""Tiny deterministic PRNG (SplitMix64).

We deliberately do not use Python's `random` module: its algorithms are not
guaranteed identical across Python versions. This one is 20 lines, so the same
seed produces byte-identical datasets on any platform or Python version.
"""
from __future__ import annotations

MASK = (1 << 64) - 1


def fnv1a(s: str) -> int:
    h = 0xCBF29CE484222325
    for b in s.encode("utf-8"):
        h ^= b
        h = (h * 0x100000001B3) & MASK
    return h


class Rng:
    def __init__(self, seed: int):
        self.s = seed & MASK

    @classmethod
    def derive(cls, seed: int, label: str) -> "Rng":
        """Independent stream per (seed, label), so changing e.g. the number
        of questions never changes the event stream."""
        return cls(((seed & MASK) * 0x9E3779B97F4A7C15 ^ fnv1a(label)) & MASK)

    def u64(self) -> int:
        self.s = (self.s + 0x9E3779B97F4A7C15) & MASK
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return z ^ (z >> 31)

    def below(self, n: int) -> int:
        return self.u64() % n

    def rand(self) -> float:
        return (self.u64() >> 11) / float(1 << 53)

    def chance(self, p: float) -> bool:
        return self.rand() < p

    def choice(self, seq):
        return seq[self.below(len(seq))]

    def sample(self, seq, k: int) -> list:
        pool = list(seq)
        k = min(k, len(pool))
        for i in range(k):
            j = i + self.below(len(pool) - i)
            pool[i], pool[j] = pool[j], pool[i]
        return pool[:k]

    def shuffle(self, lst: list) -> None:
        for i in range(len(lst) - 1, 0, -1):
            j = self.below(i + 1)
            lst[i], lst[j] = lst[j], lst[i]
