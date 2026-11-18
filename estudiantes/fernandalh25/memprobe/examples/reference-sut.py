#!/usr/bin/env python3
"""Reference system under test: a rule-based memory (regex parser + dict).

It exists to validate the benchmark, not to compete:
  * with no flags it should score 100% (proves every question is answerable
    from the stream alone, i.e. the benchmark itself is sound);
  * each flag ablates ONE memory behaviour, and should hurt ONE ability
    (proves the benchmark can tell those failure modes apart).

Deliberately independent of the generator's code: it only sees the text.
"""
import argparse
import collections
import difflib
import json
import re
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--window", type=int, help="remember only the last K stored events")
ap.add_argument("--no-forget", action="store_true", help="ignore retractions")
ap.add_argument("--first-write-wins", action="store_true", help="ignore later updates")
ap.add_argument("--no-history", action="store_true", help="keep only the latest value per key")
ap.add_argument("--fuzzy", action="store_true", help="resolve unknown names to the closest known name")
ap.add_argument("--guess", action="store_true", help="never say UNKNOWN: guess the most common value")
args = ap.parse_args()

W, V = r"([A-Za-z]+)", r"([A-Za-z0-9]+)"
PROSE_SET = [
    ("city", rf"{W} relocated to {V}\.", 0), ("city", rf"{W} now lives in {V}\.", 0),
    ("city", rf"{W} has settled in {V}\.", 0),
    ("role", rf"{W} took on the role of {V}\.", 0), ("role", rf"{W} is now working as {V}\.", 0),
    ("role", rf"{W} was appointed {V}\.", 0),
    ("team", rf"{W} joined the {V} team\.", 0), ("team", rf"{W} was assigned to team {V}\.", 0),
    ("team", rf"{W} transferred into the {V} team\.", 0),
    ("tool", rf"{W} switched to using {V}\.", 0), ("tool", rf"{W}'s main tool is now {V}\.", 0),
    ("tool", rf"{W} adopted {V} as the default tool\.", 0),
    ("level", rf"{W} reached level {V}\.", 0), ("level", rf"{W} was graded at level {V}\.", 0),
    ("level", rf"{W} now holds level {V}\.", 0),
    ("lead", rf"{W} now reports to {V}\.", 0), ("lead", rf"{V} became the lead of {W}\.", 1),
    ("lead", rf"{W}'s lead is now {V}\.", 0),
]
PROSE_SET = [(a, re.compile(p), sw) for a, p, sw in PROSE_SET]
PROSE_DEL = [re.compile(p) for p in (
    rf"The record of {W}'s ([a-z]+) was struck from the log\.",
    rf"{W}'s ([a-z]+) was cleared and is no longer known\.",
    rf"Forget what was said about {W}'s ([a-z]+)\.")]
CODE_SET = [re.compile(p) for p in (
    r'set_attr\("(\w+)", "(\w+)", (.+)\)', r"(\w+)\.(\w+) = (.+)", r'config\["(\w+)"\]\["(\w+)"\] = (.+)')]
CODE_DEL = [re.compile(p) for p in (
    r'del_attr\("(\w+)", "(\w+)"\)', r"del (\w+)\.(\w+)", r'del config\["(\w+)"\]\["(\w+)"\]')]
TRAIL = re.compile(r"(.*?)\s+# day (\d+)")
LEAD_PROSE = re.compile(r"Day (\d+): (.*)")

hist = {}  # (entity, attr) -> list[(day, value|None)]
known = set()
window = collections.deque()


def store(pair, day, val):
    if args.no_forget and val is None:
        return
    h = hist.setdefault(pair, [])
    if args.first_write_wins and any(x[1] is not None for x in h) and val is not None:
        return
    if args.no_history:
        h.clear()
    h.append((day, val))
    known.add(pair[0])
    if args.window:
        window.append(pair)
        if len(window) > args.window:
            old = window.popleft()
            hh = hist.get(old)
            if hh:
                hh.pop(0)
                if not hh:
                    del hist[old]


def lit(s):
    s = s.strip()
    return s[1:-1] if len(s) >= 2 and s[0] == s[-1] == '"' else s


def ingest(text):
    m = LEAD_PROSE.fullmatch(text)
    if m:
        day, body = int(m.group(1)), m.group(2)
        for attr, rx, swap in PROSE_SET:
            mm = rx.fullmatch(body)
            if mm:
                e, v = (mm.group(2), mm.group(1)) if swap else (mm.group(1), mm.group(2))
                return store((e, attr), day, v)
        for rx in PROSE_DEL:
            mm = rx.fullmatch(body)
            if mm:
                return store((mm.group(1), mm.group(2)), day, None)
        return
    m = TRAIL.fullmatch(text)
    if not m:
        return
    stmt, day = m.group(1), int(m.group(2))
    if stmt.startswith("#"):
        return
    for rx in CODE_SET:
        mm = rx.fullmatch(stmt)
        if mm:
            return store((mm.group(1), mm.group(2)), day, lit(mm.group(3)))
    for rx in CODE_DEL:
        mm = rx.fullmatch(stmt)
        if mm:
            return store((mm.group(1), mm.group(2)), day, None)


def resolve(e):
    if args.fuzzy and e not in known:
        c = difflib.get_close_matches(e, list(known), n=1, cutoff=0.85)
        if c:
            return c[0]
    return e


def current(e, a):
    h = hist.get((resolve(e), a))
    return h[-1][1] if h else None


def as_of(e, a, day):
    h = hist.get((resolve(e), a))
    res = None
    for d, v in h or []:
        if d <= day:
            res = v
    return res


def unknown_or_guess(a, val):
    if val is not None:
        return val
    if args.guess:
        c = collections.Counter(h[-1][1] for (e, aa), h in hist.items() if aa == a and h[-1][1] is not None)
        if c:
            return c.most_common(1)[0][0]
    return "UNKNOWN"


def answer(q):
    m = re.fullmatch(r"What is the current (\w+) of (\w+)\?", q)
    if m:
        return unknown_or_guess(m.group(1), current(m.group(2), m.group(1)))
    m = re.fullmatch(r"What was the (\w+) of (\w+) at the end of day (\d+)\?", q)
    if m:
        return unknown_or_guess(m.group(1), as_of(m.group(2), m.group(1), int(m.group(3))))
    m = re.fullmatch(r"What is the (\w+) of the lead of (\w+)\?", q)
    if m:
        lead = current(m.group(2), "lead")
        return "UNKNOWN" if lead is None else unknown_or_guess(m.group(1), current(lead, m.group(1)))
    m = re.fullmatch(r"Which entities currently have (\w+) (\w+)\?", q)
    if m:
        return sorted(e for (e, a), h in hist.items() if a == m.group(1) and h[-1][1] == m.group(2))
    m = re.fullmatch(r"How many entities currently have (\w+) (\w+)\?", q)
    if m:
        return str(sum(1 for (e, a), h in hist.items() if a == m.group(1) and h[-1][1] == m.group(2)))
    return "UNKNOWN"


for line in sys.stdin:
    msg = json.loads(line)
    if msg["op"] == "ingest":
        ingest(msg["text"])
        out = {"ok": True}
    else:
        out = {"answer": answer(msg["q"])}
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()
