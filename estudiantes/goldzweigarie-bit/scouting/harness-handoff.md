# Harness from scratch — handoff (alternative final project)

Context for a new conversation in the NERV project. The main conversation continues with the **CDMX site-suitability dashboard**; this one is for the **agent harness** track.

## Working rules
- **goldzweigarie-bit is the only author/contributor.** No `Co-Authored-By`, "Generated with Claude" or any other attribution in commits, PRs or files.
- Repo lives at `~/NERV/nerv-harness` on the student's Mac; GitHub: https://github.com/goldzweigarie-bit/Harness-Proyecto-Final (the student pushes from his Terminal).
- Claude's shell on the Mac is a Linux VM: no Docker, no file deletes, so git commits there leave lock files. Claude writes/tests code in its cloud workspace, copies changed files into the folder, and the student commits/pushes. The `Makefile` is protected from remote writes; the student edits it by hand.

## Status (2026-11-15)
- **Milestone 1** committed and pushed (`2c4e1ab`, attribution removed). Stdlib-only Python.
  - `harness/agent.py` loop (regex, exactly one ```bash block, `submit` to finish, format errors fed back, step limit, 10k-char output cap)
  - `harness/models.py` Anthropic (default `claude-sonnet-5-5`) + OpenAI-compatible via urllib, retries on 429/5xx; `ScriptedModel` for tests
  - `harness/run.py` CLI: `python3 -m harness.run tasks/001-fizzbuzz` → runs check, writes `runs/<ts>_<task>/trajectory.json`
  - `tasks/001-fizzbuzz`, `tests/test_agent.py`
- **Milestone 2 code written, copied to the Mac, not yet committed by the student.** 17 tests pass (fake `docker` shim, no daemon).
  - `SandboxLimits`: `--network none`, `--cpus 1`, `--memory 512m` = `--memory-swap`, `--pids-limit 256`, `--user agent`, `--cap-drop ALL`, `no-new-privileges`, `--read-only` + tmpfs `/tmp`, `/home/agent` + anonymous volume `/workspace`. CLI flags `--cpus --memory --pids --network`; limits saved in trajectory.
  - `timeout -k 5 N` inside the container; 124 = timeout, 137 + cgroup `memory.events` oom_kill increase = OOM; agent gets a `[harness] …` reason.
  - `copy_in` chowns `/workspace` to 1000:1000.
  - `harness/selftest.py`: 10 checks against a real container (non-root, no network, writable workspace, read-only root, /tmp, memory, timeout, SIGTERM-ignoring process, pids, CPU quota).
- **Pending on the Mac:** `docker build`, `python3 -m harness.selftest`, first real `harness.run` with an API key; Makefile `selftest` target; commit + push M2.

## Done earlier
- Researched four reference harnesses: **Pi** (Mario Zechner / Earendil; 4 tools read/write/edit/bash, <1k-token system prompt, extensions), **mini-SWE-agent** (~100 lines Python, bash only, linear history, `subprocess.run` → swap for `docker exec`), **Hermes Agent** (Nous Research; SQLite+FTS5 sessions, compaction into child sessions, skills, gateways, `delegate_task`), **Prime Agent** (Prime Intellect; built on Pi; single tool = persistent IPython kernel, `rlm()` async subagents, Continual Harness CRUD).
- Built a course-style page: "11.13 Harnesses de agentes" — https://claude.ai/artifact/9btW21eU5SMcFSZ1snjLgG
- Estimate: full defensible project ≈ 54 h (≈ 68 h with buffer); trimmed version (loop + Docker + concurrency + evaluation) ≈ 29 h.

## Milestones (hours)
1. Minimal loop + API, regex action parsing, trajectory JSON — 6 — **done; real run pending**
2. Docker sandbox (`--network none`, CPU/mem limits, timeouts) — 5 — **code done; selftest on real Docker pending**
3. Native tool calling with typed read/write/edit/bash — 8
4. Sessions (JSONL/SQLite), resume, AGENTS.md — 5
5. Context: truncate outputs, token count, compaction — 6
6. Concurrency: `asyncio.gather` tool calls, subagents as processes + Semaphore, 429 retries — 10
7. Evaluation: 15–20 auto-checked tasks; success rate, cost, time, speedup — 8
8. GitHub: repo, docker compose, Actions CI running the benchmark, README, demo — 6
Optional: SSE streaming + TUI/web Gantt (8); urban-data tools, e.g., OSM/INEGI (8)

## Sources
- https://www.mariozechner.at/posts/2025-11-30-pi-coding-agent/
- https://github.com/SWE-agent/mini-swe-agent
- https://arize.com/blog/how-hermes-implements-open-source-agent-harness-architecture/
- https://primeintellect.ai/blog/prime-agent
- https://ampcode.com/how-to-build-an-agent
