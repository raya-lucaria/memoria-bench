"""Procedural dataset generator.

A hidden "world" (entities with attributes that change over time) is simulated
into a stream of events. The same facts can be rendered as prose or as
code-like statements ("tracks"). Questions are built from the simulated state,
so gold answers come from the simulation itself: no model, no annotators.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

from .rng import Rng
from .vocab import Words

BENCH_VERSION = "0.2"
UNKNOWN = "UNKNOWN"
ATTRS = ("city", "role", "team", "tool", "level", "lead")
ABILITIES = ("recall", "update", "temporal", "multi_hop", "aggregate", "abstain", "forget")
TRACKS = ("prose", "code", "mixed")
CHECKPOINTS = (0.4, 0.6, 0.8, 1.0)  # default for the scripted runner: fractions of the stream at which questions are asked
FINAL_ONLY = (1.0,)  # default for harness kits: one question session after the last session


@dataclass(frozen=True)
class Event:
    day: int
    kind: str  # "set" | "retract" | "noise"
    e: str
    a: str
    v: Optional[str]


@dataclass
class Question:
    after_seq: int  # number of events that must be ingested before this question
    q: str
    fmt: str  # "value" | "list" | "count"
    gold: Union[str, List[str]]
    ability: str
    kind: str
    age_frac: Optional[float]  # how far back the needed fact is, as a fraction of the stream so far


@dataclass
class Episode:
    track: str
    seed: int
    events: List[str]
    questions: List[Question]
    dataset_id: str
    n_entities: int


# ----------------------------------------------------------------------------- world

class World:
    def __init__(self, seed: int, n_events: int):
        rng = Rng.derive(seed, "vocab")
        words = Words(rng)
        n_ent = min(5000, max(12, n_events // 10))
        pool = min(80, max(6, n_ent // 5))

        self.entities: List[str] = []
        self.ghosts: List[str] = []  # near-twins of real entities that NEVER appear in the stream
        base = 0
        while base < n_ent:
            w = words.new(3)
            self.entities.append(w.capitalize())
            base += 1
            r = rng.rand()
            if r < 0.20:  # a real twin that does appear
                t = words.twin(w)
                if t:
                    self.entities.append(t.capitalize())
            elif r < 0.35:  # a ghost twin that never appears
                t = words.twin(w)
                if t:
                    self.ghosts.append(t.capitalize())

        def make_pool(cap: bool) -> List[str]:
            out: List[str] = []
            while len(out) < pool:
                x = words.new(2 + rng.below(2))
                out.append(x.capitalize() if cap else x)
                if len(out) < pool and rng.chance(0.30):
                    t = words.twin(x)
                    if t:
                        out.append(t.capitalize() if cap else t)
            return out

        self.pools: Dict[str, List[str]] = {
            "city": make_pool(True),
            "role": make_pool(False),
            "team": make_pool(True),
            "tool": make_pool(False),
            "level": [str(i) for i in range(1, 10)],
        }

    def value(self, attr: str, rng: Rng, exclude: Optional[str] = None, avoid: Optional[str] = None) -> str:
        pool = self.entities if attr == "lead" else self.pools[attr]
        v = pool[0]
        for _ in range(20):
            v = rng.choice(pool)
            if v != exclude and v != avoid:
                return v
        return v


def gen_events(world: World, n: int, rng: Rng) -> List[Event]:
    evs: List[Event] = []
    day = 1
    cur: Dict[Tuple[str, str], str] = {}
    last_day: Dict[Tuple[str, str], int] = {}
    setpairs: List[Tuple[str, str]] = []
    seen = set()
    for _ in range(n):
        if rng.chance(0.4):
            day += 1
        r = rng.rand()
        if r < 0.15:  # distractor: mentions an entity and a value without asserting anything
            a = rng.choice(ATTRS)
            e = rng.choice(world.entities)
            evs.append(Event(day, "noise", e, a, world.value(a, rng, exclude=e)))
            continue
        if r < 0.26 and setpairs:  # retraction (11% of events)
            pair = None
            for _ in range(10):
                p = rng.choice(setpairs)
                if p in cur:
                    pair = p
                    break
            if pair is not None:
                if last_day.get(pair) == day:
                    day += 1
                evs.append(Event(day, "retract", pair[0], pair[1], None))
                del cur[pair]
                last_day[pair] = day
                continue
        if setpairs and rng.chance(0.5):
            pair = rng.choice(setpairs)
        else:
            pair = (rng.choice(world.entities), rng.choice(ATTRS))
        if last_day.get(pair) == day:  # at most one event per (entity, attribute) per day
            day += 1
        v = world.value(pair[1], rng, exclude=pair[0], avoid=cur.get(pair))
        evs.append(Event(day, "set", pair[0], pair[1], v))
        if pair not in seen:
            seen.add(pair)
            setpairs.append(pair)
        cur[pair] = v
        last_day[pair] = day
    return evs


# --------------------------------------------------------------------------- rendering

PROSE_SET = {
    "city": ["{e} relocated to {v}.", "{e} now lives in {v}.", "{e} has settled in {v}."],
    "role": ["{e} took on the role of {v}.", "{e} is now working as {v}.", "{e} was appointed {v}."],
    "team": ["{e} joined the {v} team.", "{e} was assigned to team {v}.", "{e} transferred into the {v} team."],
    "tool": ["{e} switched to using {v}.", "{e}'s main tool is now {v}.", "{e} adopted {v} as the default tool."],
    "level": ["{e} reached level {v}.", "{e} was graded at level {v}.", "{e} now holds level {v}."],
    "lead": ["{e} now reports to {v}.", "{v} became the lead of {e}.", "{e}'s lead is now {v}."],
}
PROSE_RETRACT = [
    "The record of {e}'s {a} was struck from the log.",
    "{e}'s {a} was cleared and is no longer known.",
    "Forget what was said about {e}'s {a}.",
]
PROSE_NOISE = [
    "{e} was mentioned in a briefing about {v}.",
    "Rumours that {e} would be linked to {v} were denied.",
    "{e} did not change anything about {v} today.",
    "A note about {v} was filed next to {e}'s name.",
]


def _lit(v: str) -> str:
    return v if v.isdigit() else '"%s"' % v


def render(ev: Event, track: str, rr: Rng) -> str:
    if track == "mixed":
        track = "prose" if rr.chance(0.5) else "code"
    if track == "prose":
        if ev.kind == "set":
            t = rr.choice(PROSE_SET[ev.a]).format(e=ev.e, v=ev.v)
        elif ev.kind == "retract":
            t = rr.choice(PROSE_RETRACT).format(e=ev.e, a=ev.a)
        else:
            t = rr.choice(PROSE_NOISE).format(e=ev.e, v=ev.v)
        return "Day %d: %s" % (ev.day, t)
    # code track
    if ev.kind == "set":
        lit = _lit(ev.v)
        stmt = rr.choice([
            'set_attr("%s", "%s", %s)' % (ev.e, ev.a, lit),
            "%s.%s = %s" % (ev.e, ev.a, lit),
            'config["%s"]["%s"] = %s' % (ev.e, ev.a, lit),
        ])
    elif ev.kind == "retract":
        stmt = rr.choice([
            'del_attr("%s", "%s")' % (ev.e, ev.a),
            "del %s.%s" % (ev.e, ev.a),
            'del config["%s"]["%s"]' % (ev.e, ev.a),
        ])
    else:
        lit = _lit(ev.v)
        stmt = rr.choice([
            "# TODO maybe %s.%s = %s" % (ev.e, ev.a, lit),
            "assert %s.%s != %s" % (ev.e, ev.a, lit),
            "# %s.%s = %s  # reverted" % (ev.e, ev.a, lit),
        ])
    return "%s  # day %d" % (stmt, ev.day)


# -------------------------------------------------------------------------- questions

class View:
    """The simulated truth after the first `cp` events."""

    def __init__(self, events: List[Event], cp: int):
        self.cp = cp
        self.hist: Dict[Tuple[str, str], List[Tuple[int, int, Optional[str]]]] = {}
        self.cur: Dict[Tuple[str, str], str] = {}
        for pos, ev in enumerate(events[:cp]):
            if ev.kind == "noise":
                continue
            pair = (ev.e, ev.a)
            val = ev.v if ev.kind == "set" else None
            self.hist.setdefault(pair, []).append((pos, ev.day, val))
            if val is None:
                self.cur.pop(pair, None)
            else:
                self.cur[pair] = val

    def age(self, pos: int) -> float:
        return (self.cp - pos) / float(self.cp)


def _q_current(cp, e, a, gold, ability, kind, age):
    return Question(cp, "What is the current %s of %s?" % (a, e), "value", gold, ability, kind, age)


def _cands_recall(v: View, world: World, rng: Rng):
    out = []
    for (e, a), h in v.hist.items():
        if len(h) == 1 and h[0][2] is not None:
            out.append(_q_current(v.cp, e, a, h[0][2], "recall", "single", v.age(h[0][0])))
    return [out]


def _cands_update(v: View, world: World, rng: Rng):
    out = []
    for (e, a), h in v.hist.items():
        vals = [x[2] for x in h if x[2] is not None]
        if len(h) >= 2 and h[-1][2] is not None and len(vals) >= 2 and vals[-1] != vals[0]:
            out.append(_q_current(v.cp, e, a, h[-1][2], "update", "latest", v.age(h[-1][0])))
    return [out]


def _cands_temporal(v: View, world: World, rng: Rng):
    out = []
    for (e, a), h in v.hist.items():
        for k in range(len(h) - 1):
            pos, day, val = h[k]
            if val is not None and val != v.cur.get((e, a)):
                out.append(Question(v.cp, "What was the %s of %s at the end of day %d?" % (a, e, day),
                                    "value", val, "temporal", "as_of", v.age(pos)))
    return [out]


def _cands_multi_hop(v: View, world: World, rng: Rng):
    out = []
    for (e, a), x in v.cur.items():
        if a != "lead":
            continue
        for a2 in ATTRS:
            if a2 == "lead":
                continue
            val = v.cur.get((x, a2))
            if val is None:
                continue
            oldest = min(v.hist[(e, "lead")][-1][0], v.hist[(x, a2)][-1][0])
            out.append(Question(v.cp, "What is the %s of the lead of %s?" % (a2, e),
                                "value", val, "multi_hop", "two_hop", v.age(oldest)))
    return [out]


def _cands_aggregate(v: View, world: World, rng: Rng):
    groups: Dict[Tuple[str, str], List[str]] = {}
    for (e, a), val in v.cur.items():
        groups.setdefault((a, val), []).append(e)
    sizes = [len(x) for x in groups.values()]
    lo, hi = (2, 12) if any(2 <= s <= 12 for s in sizes) else (1, 12)
    sets, counts = [], []
    for (a, val), ents in sorted(groups.items()):
        if lo <= len(ents) <= hi:
            sets.append(Question(v.cp, "Which entities currently have %s %s?" % (a, val),
                                 "list", sorted(ents), "aggregate", "set", None))
            counts.append(Question(v.cp, "How many entities currently have %s %s?" % (a, val),
                                   "count", str(len(ents)), "aggregate", "count", None))
    return [sets, counts]


def _cands_abstain(v: View, world: World, rng: Rng):
    seen_ents = sorted({e for (e, _a) in v.hist})
    never = []
    if seen_ents:
        tried = set()
        for _ in range(400):
            e, a = rng.choice(seen_ents), rng.choice(ATTRS)
            if (e, a) in v.hist or (e, a) in tried:
                continue
            tried.add((e, a))
            never.append(_q_current(v.cp, e, a, UNKNOWN, "abstain", "never_stated", None))
    ghost = [_q_current(v.cp, g, a, UNKNOWN, "abstain", "ghost_entity", None)
             for g in world.ghosts for a in ATTRS]
    pre = []
    for (e, a), h in v.hist.items():
        if h[0][2] is not None and h[0][1] >= 2:
            pre.append(Question(v.cp, "What was the %s of %s at the end of day %d?" % (a, e, h[0][1] - 1),
                                "value", UNKNOWN, "abstain", "before_first", None))
    return [never, ghost, pre]


def _cands_forget(v: View, world: World, rng: Rng):
    out = []
    for (e, a), h in v.hist.items():
        if h[-1][2] is None:
            out.append(_q_current(v.cp, e, a, UNKNOWN, "forget", "retracted", v.age(h[-1][0])))
    return [out]


_BUILDERS = {
    "recall": _cands_recall, "update": _cands_update, "temporal": _cands_temporal,
    "multi_hop": _cands_multi_hop, "aggregate": _cands_aggregate,
    "abstain": _cands_abstain, "forget": _cands_forget,
}


def _pick(groups: List[List[Question]], k: int, rng: Rng, seen: set) -> List[Question]:
    shuf = [rng.sample(g, min(len(g), k * 4 + 10)) for g in groups]
    idx = [0] * len(groups)
    active = [i for i in range(len(groups))]
    res: List[Question] = []
    while len(res) < k and active:
        for gi in list(active):
            if len(res) >= k:
                break
            while idx[gi] < len(shuf[gi]) and (shuf[gi][idx[gi]].after_seq, shuf[gi][idx[gi]].q) in seen:
                idx[gi] += 1
            if idx[gi] >= len(shuf[gi]):
                active.remove(gi)
                continue
            c = shuf[gi][idx[gi]]
            idx[gi] += 1
            seen.add((c.after_seq, c.q))
            res.append(c)
    return res


def build_questions(events: List[Event], world: World, rng: Rng, n_queries: int,
                    checkpoints: Tuple[float, ...] = CHECKPOINTS) -> List[Question]:
    n = len(events)
    n_ab = len(ABILITIES)
    quota = {ab: n_queries // n_ab + (1 if i < n_queries % n_ab else 0) for i, ab in enumerate(ABILITIES)}
    cps: List[int] = []
    for f in checkpoints:
        c = max(1, int(round(n * f)))
        if c not in cps:
            cps.append(c)
    out: List[Question] = []
    seen: set = set()
    for ci, cp in enumerate(cps):
        view = View(events, cp)
        batch: List[Question] = []
        for ab in ABILITIES:
            k = quota[ab] // len(cps) + (1 if ci < quota[ab] % len(cps) else 0)
            if k:
                batch.extend(_pick(_BUILDERS[ab](view, world, rng), k, rng, seen))
        rng.shuffle(batch)
        out.extend(batch)
    return out


# ------------------------------------------------------------------------------ API

def dataset_id(texts: List[str], questions: List[Question]) -> str:
    blob = json.dumps(
        {"v": BENCH_VERSION, "events": texts,
         "questions": [[q.after_seq, q.q, q.fmt, q.gold, q.ability] for q in questions]},
        separators=(",", ":"), sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(blob.encode("ascii")).hexdigest()[:16]


def generate_episode(track: str, seed: int, n_events: int, n_queries: int,
                     checkpoints: Tuple[float, ...] = CHECKPOINTS) -> Episode:
    if track not in TRACKS:
        raise ValueError("track must be one of %s" % (TRACKS,))
    world = World(seed, n_events)
    evs = gen_events(world, n_events, Rng.derive(seed, "events"))
    rr = Rng.derive(seed, "render:" + track)
    texts = [render(ev, track, rr) for ev in evs]
    qs = build_questions(evs, world, Rng.derive(seed, "queries"), n_queries, checkpoints)
    return Episode(track, seed, texts, qs, dataset_id(texts, qs), len(world.entities))
