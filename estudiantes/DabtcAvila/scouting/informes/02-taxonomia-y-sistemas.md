<!-- Salida original de un subagente de investigación web (Claude Code, 17-nov-2026). Sin editar, salvo quitar rutas locales. [P]/[V] = leído en la página; [S] = solo fragmento de búsqueda. Las páginas se leyeron a través de un resumidor: verificar cada cifra en su fuente antes de citarla. -->

# Memory types and architectures for LLM agent harnesses (as of 2026-11-17)

**Verification legend.** [V] = I read the page itself. [S] = search snippet or secondary source only, not confirmed against the primary. [M] = GitHub API metadata (license, stars, dates) pulled today.

---

## Part A — Taxonomy

### A1. Cognitive-science types (CoALA)

Source: Sumers, Yao, Narasimhan, Griffiths, "Cognitive Architectures for Language Agents", arXiv 2309.02427 (Sep 2023; TMLR version Mar 2024). https://arxiv.org/abs/2309.02427 [V]

| Type | CoALA definition [V] | Harness equivalent (my mapping) |
|---|---|---|
| Working | "maintains active and readily available information as symbolic variables for the current decision cycle" | Context window: system prompt, loaded CLAUDE.md, todo list, tool results |
| Episodic | "experience from earlier decision cycles" | Session transcripts, journals/progress logs, claude-mem observations, Hermes session DB |
| Semantic | Knowledge about the world and the agent itself | MEMORY.md facts, wikis, knowledge graphs, user profiles |
| Procedural | LLM weights (implicit) plus agent code (explicit) | CLAUDE.md/AGENTS.md rules, skills, hooks, self-written skills (Hermes) |

CoALA's internal actions are retrieval (long-term to working), reasoning (within working memory) and learning (writing to long-term) [V]. LangMem reuses the semantic/episodic/procedural split and notes that some procedural memory is "always present in the prompt" while other memory is recalled by similarity (https://blog.langchain.com/langmem-sdk-launch) [S].

### A2. Engineering axes

| Axis | Options | Examples |
|---|---|---|
| **Storage substrate** | Plain markdown files | Claude Code, OpenClaw, Hermes, Letta MemFS, LLM Wiki, Basic Memory |
| | Append-only log plus summary tree | OptMem |
| | Vector DB | MemPalace (ChromaDB), Mem0, Supermemory |
| | Temporal knowledge graph | Zep/Graphiti, Cognee, Hindsight |
| | SQL / versioned SQL | beads (Dolt), claude-mem (SQLite FTS5 + optional Chroma), Hermes sessions (SQLite FTS5) |
| | File-like KV you implement | Anthropic memory tool (`/memories` prefix mapped to any store) |
| **Write path** | Human-curated | CLAUDE.md, AGENTS.md, Cursor rules |
| | Agent-curated, in the hot path | Claude Code auto memory, memory tool, OptMem `note`, Hermes `memory` tool |
| | Automatic extraction by hooks or an observer | claude-mem, Mem0, Mastra Observer, MemPalace hooks, Codex memories |
| | Background consolidation ("sleep-time", "dreaming") | Managed Agents Dreams, OpenClaw dreaming, Letta reflection, Hermes background review, Mastra Reflector, Codex consolidation |
| **Read path** | Always-loaded index | MEMORY.md (first 200 lines / 25KB), Hermes frozen snapshot, Letta `system/` |
| | Retrieval on demand ("just-in-time") | grep/glob, `memory_search`, MCP search tools, `memo recall` |
| | Hook injection at session start | claude-mem, `bd prime`, `mempalace wake-up`, `memo wake` |
| | Progressive disclosure | index, then detail (claude-mem's three layers, Letta file tree with frontmatter) |
| **Scope** | Org / user / project / local / session / subagent / team | Claude Code's CLAUDE.md hierarchy covers the first four; team memory is mostly "commit it to git" |
| **Forgetting and conflict** | Never delete, compress with age | OptMem |
| | Invalidate with timestamps | Graphiti bi-temporal edges |
| | Size caps that force curation | Hermes (2,200 / 1,375 chars), Claude Code index limits |
| | Offline dedup and contradiction resolution | Dreams, OpenClaw promotion gates |
| | ADD-only | Mem0's 2026 algorithm |
| **Verbatim vs summarised** | Verbatim | MemPalace drawers, OptMem LOG.txt, Hermes session search |
| | Extracted or summarised | Mem0, Mastra OM, claude-mem observations |
| **Compaction vs memory** | Compaction summarises the same conversation to stay inside the window; memory persists outside it and survives resets | Anthropic recommends pairing them: "memory preserves the information that must survive summarization" (https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) [V]. OpenClaw runs a silent "memory flush" turn before compaction [V]. |

---

## Part B — System profiles

### B1. MemPalace
- **URL:** https://github.com/MemPalace/mempalace. MIT, about 60.6k stars, created 2026-04-05, v3.12.0 [V][M].
- **Architecture:** Wings (people/projects), rooms (topics) and drawers (verbatim original content) [V]. Early coverage also lists halls and closets; the current README does not mention halls, closets, tunnels or AAAK [V].
- **Storage:** ChromaDB by default, with swappable backends (sqlite_exact, milvus, qdrant, pgvector) and a temporal knowledge graph in local SQLite [V].
- **Write:** `mempalace mine`, `sweep` (one drawer per message), and auto-save hooks for Claude Code, Codex CLI and Cursor that fire periodically and before compaction [V].
- **Read:** `mempalace search`, `wake-up`, and an MCP server with 47 tools [V].
- **Current claims [V]:**
  - LongMemEval R@5 96.6% raw, no LLM.
  - 98.4% on 450 held-out questions for hybrid v4, which the README calls "the honest generalisable figure".
  - LoCoMo R@10 60.3% raw and 88.9% hybrid.
  - It now declines to compare against Mem0 or Zep because the metrics differ.
- **Controversy:** The critical analysis is arXiv 2604.21284 (Dey and Viradecha, not peer-reviewed), https://arxiv.org/html/2604.21284v1 [V]. Its findings:
  - The 96.6% is reproducible with bare ChromaDB plus verbatim chunks; the hierarchy is metadata filtering over one flat collection.
  - The metric is recall_any@5, "the most generous variant", and is retrieval recall rather than QA accuracy.
  - AAAK is lossy summarisation: 84.2% vs 96.6% verbatim, and the "30x compression, zero information loss" claim was inaccurate.
  - The original 100% LongMemEval involved iterative fixes on failing questions; the 100% LoCoMo used top_k=50.
  - "Contradiction detection" was exact-match dedup, and the knowledge graph is a single-hop triple store.
  - Maintainers acknowledged the audit (GitHub issue #29) and corrected the numbers. The paper's verdict: "significant architectural insight wrapped in overstated claims".
- **Other notes:** The README warns that impostor domains distribute malware [V]. The celebrity co-author (Milla Jovovich) is from press coverage only (https://hackernoon.com/resident-evil-star-milla-jovovich-shipped-an-ai-memory-system-devs-shredded-its-benchmarks) [S].

### B2. "Second brain" approaches
- **Karpathy's LLM Wiki** (gist, 2026-04-04): https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f [V]
  - Three layers: immutable raw sources, an LLM-written markdown wiki, and a schema file (CLAUDE.md/AGENTS.md).
  - Three operations: ingest (one source may touch 10–15 pages), query (answers can be filed back), and lint (contradictions, stale claims, orphans).
  - `index.md` is the catalog read first; `log.md` is an append-only chronological record.
  - It contrasts itself with RAG, where "the LLM is rediscovering knowledge from scratch on every question". It says this works at about 100 sources without embeddings, and recommends Obsidian, qmd and git.
- **Projects literally named second-brain** [S, not opened]:
  - `hess0ul/second-brain`: a single Claude skill treating an Obsidian vault as external memory.
  - `coleam00/second-brain-starter`: SOUL.md / USER.md / HEARTBEAT.md templates.
  - `kilip/second-brain`: a skills collection.
- **Related vault kits** [S]: `heyitsnoah/claudesidian` (PARA vault, MIT, 2.6k stars [M]), `agricidaniel/claude-obsidian` (LYT/PARA/Zettelkasten modes), `kengio/onebrain`.
- **Basic Memory:** https://github.com/basicmachines-co/basic-memory. AGPL-3.0, 4.6k stars [M]. Markdown notes with categorised observations and WikiLink relations, indexed in local SQLite, exposed through MCP, and editable in Obsidian [S].
- **Criticism:** No benchmark exists for these; one secondary estimate puts the wiki pattern's ceiling at roughly 400k words [S].

### B3. "OptMem" — found
- **What it is:** Victor Taelin's OptMem, https://github.com/VictorTaelin/OptMem. About 2.4k stars, created 2026-07-25, last push 2026-07-31, **no license file detected** [V][M].
- **Tagline:** "Permanent memory for AI agents. A 426-token prompt, a script, plug and play." [V]
- **Architecture [V]:** One dependency-free Python script, `memo`.
  - `LOG.txt` is an append-only log of fixed-width records, up to 280 bytes per memory.
  - `TREE/` is a rebuildable binary merge tree of summaries (#0-1, #2-3, then 0-3, and so on).
- **Write [V]:** `memo note`. When merges fall due, the agent itself writes the summary (`memo nap`); "Nothing ever runs in the background."
- **Read [V]:** `memo wake` at session start (default 96 lines, about 8k tokens; recent items verbatim, older ones progressively compressed), `memo recall <regex>`, `memo zoom`, and `memo forget` to drop a bad summary.
- **Integration [V]:** The installer prints a `## Memory` block to paste into CLAUDE.md or AGENTS.md. Subagents are told not to run it.
- **Claims [V]:** `wake` takes 0.03s at a million memories.
- **Criticism:** No benchmarks or independent evaluation found (AlphaSignal preview, https://alphasignal.ai/news/victor-taelin-s-optmem-gives-ai-agents-permanent-memory-without-a-database.md) [V].
- **Similar names, not the same thing [S]:** `Moeblack/OptMemo` (fork), `optmem-hermes-plugin` (Hermes provider with BM25), and "O-Mem" (a separate research framework). No "OptiMem" project was found.

### B4. Claude Code native memory
Source: https://code.claude.com/docs/en/memory [V]

- **CLAUDE.md hierarchy:**
  - Scopes: managed policy (OS-level path), user (`~/.claude/CLAUDE.md`), project (`./CLAUDE.md` or `./.claude/CLAUDE.md`), local (`./CLAUDE.local.md`).
  - Files above the working directory are concatenated root-down at launch; subdirectory files load on demand when Claude touches files there.
  - `@path` imports go up to four hops deep and do not reduce context cost.
  - `.claude/rules/` supports path-scoped rules that load only for matching files.
  - Target is under 200 lines per file. It is "context, not enforced configuration"; enforcement belongs in a PreToolUse hook.
  - AGENTS.md is read natively when no CLAUDE.md exists (v2.1.277+).
- **Auto memory:**
  - Lives at `~/.claude/projects/<project>/memory/`, with a `MEMORY.md` index (one line per memory) and one topic file per memory.
  - Frontmatter `type` is one of `user`, `feedback`, `project`, `reference`.
  - The first 200 lines or 25KB of MEMORY.md load every session; topic files are read on demand.
  - It skips anything derivable from the code or already in CLAUDE.md.
  - Machine-local, shared across worktrees of a repo, on by default locally. Controlled by `autoMemoryEnabled`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` and `autoMemoryDirectory`.
  - Subagents can keep their own memory.
- **Skills as procedural memory:** The memory page says multi-step procedures should move out of CLAUDE.md into a skill or path-scoped rule [V].
- **Dreaming in Claude Code:** Not in the official docs. The docs index (https://code.claude.com/docs/llms.txt) has no dream page and the memory page never mentions it [V]. Third parties describe "Auto Dream" / `/dream` as a flag-gated background consolidation, with reported triggers of roughly 24h plus 5 sessions (https://claudefa.st/blog/guide/mechanics/auto-dream, https://tessl.io/blog/anthropic-tests-auto-dream-to-clean-up-claudes-memory/) [S]. Treat as unconfirmed.
- **Dreams in Managed Agents (official, research preview):** https://platform.claude.com/docs/en/managed-agents/dreams [V]
  - An async job takes a memory store plus 1–100 session transcripts and produces a new store with duplicates merged and contradicted entries replaced.
  - The input store is never modified, so you can review and discard.
  - Requires the `dreaming-2026-04-21` beta header.
- **API memory tool:** `memory_20250818`, stable, client-side, https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool [V]
  - Commands: view, create, str_replace, insert, delete, rename under `/memories`.
  - The API auto-injects a protocol: "ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE … ASSUME INTERRUPTION".
  - The docs include a "multisession software development pattern": an initializer session creates a progress log and feature checklist, each session opens by reading them, and each ends by updating the log.

### B5. Anthropic context-engineering guidance
- **"Effective context engineering for AI agents"** (2025-09-29): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents [V]
  - Context is a finite "attention budget"; recall degrades as the window grows ("context rot").
  - Just-in-time retrieval: keep "lightweight identifiers (file paths, stored queries, web links)" and load at runtime.
  - Claude Code is described as a hybrid: "CLAUDE.md files are naively dropped into context up front" while glob and grep retrieve the rest.
  - Three long-horizon techniques: compaction, structured note-taking (the Pokémon notes example), and sub-agents returning 1–2k-token summaries.
  - Closing advice: "do the simplest thing that works".
- **"Effective harnesses for long-running agents"** (2025-11-26): https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents [V]
  - Initializer agent plus coding agent.
  - Artifacts: a JSON feature list (only the `passes` field is editable), `claude-progress.txt`, `init.sh`, and descriptive git commits.
  - Session-start routine: `pwd`, read the progress file and git log, pick the next feature, run `init.sh` and a smoke test.
  - This is the canonical journal/handoff-file pattern with a start ritual.

### B6. Letta / MemGPT
- **URL:** https://github.com/letta-ai/letta. Apache-2.0, 25.5k stars [M].
- **Legacy design:** Memory blocks pinned in context and edited with tools such as `core_memory_replace`, plus server-side sleep-time agents [S].
- **Current design, Context Repositories / MemFS** (2026-02-12): https://www.letta.com/blog/context-repositories [V]
  - Memory is a git-backed tree of markdown files with frontmatter; the tree is visible in the system prompt.
  - A `system/` directory is always fully loaded; everything else is progressive disclosure.
  - Subagents write concurrently in git worktrees and merge.
  - Built-in skills: initialization, reflection (sleep-time) and defragmentation into 15–25 focused files.
- **Filesystem finding** (2025-08-12): https://www.letta.com/blog/benchmarking-ai-agent-memory [V]
  - A GPT-4o-mini agent with only grep, search_files, open and close over a file of LoCoMo history scored 74.0%, against 68.5% for Mem0's best graph variant.
  - Caveat: `search_files` was semantic search, so this was not pure grep.
  - Conclusion: an agent's skill with retrieval tools matters more than the mechanism.
- **Criticism:** Mem0 has since published much higher scores and Letta has not rerun the experiment [S].

### B7. Dedicated memory layers

| System | URL / license [M] | Architecture and write path | Claims | Criticism |
|---|---|---|---|---|
| **Mem0** | https://github.com/mem0ai/mem0, Apache-2.0, 69k stars | Extracted facts in a vector store with optional graph. The April 2026 algorithm is a single ADD-only LLM call, replacing the two-pass ADD/UPDATE/DELETE [S] | LoCoMo 92.5 and LongMemEval 94.4 on its blog; 91.6 and 93.4 on PyPI [S] | Self-reported; Zep disputes its SOTA claim (https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/) [S]; Letta said its MemGPT numbers were unexplained [V] |
| **Zep / Graphiti** | https://github.com/getzep/graphiti, Apache-2.0, 32.9k stars | Bi-temporal knowledge graph; facts are invalidated with timestamps rather than deleted (arXiv 2501.13956) [S] | 71.2% LongMemEval with GPT-4o in its paper [S] | Graph operations add complexity [S] |
| **LangMem** | https://github.com/langchain-ai/langmem, MIT, 1.8k stars | LLM "Memory Manager" extraction; procedural memory as prompt rewriting [S] | None found | Pre-1.0, slow release cadence [S] |
| **Cognee** | https://github.com/topoteretes/cognee, Apache-2.0, 33.4k stars | Extract–Cognify–Load pipeline into a knowledge graph plus embeddings [S] | Evaluates on BEAM | No comparable LongMemEval score published [S] |
| **Supermemory** | https://github.com/supermemoryai/supermemory, MIT, 31.7k stars | Memory API / context engine; internals not verified | 81.6% LongMemEval (GPT-4o) per Mastra's table [V] | Not independently verified |
| **A-MEM** | https://github.com/agiresearch/A-mem, MIT, 1.2k stars | Zettelkasten-style notes with keywords, tags and autonomous linking; new memories can update old ones (arXiv 2502.12110, NeurIPS 2025) [S] | Research | Last push Dec 2025 [M] |
| **MemOS** | https://github.com/MemTensor/MemOS, Apache-2.0, 12.4k stars | "Memory OS" built on a MemCube abstraction [S] | Not checked | Primary paper not found in my searches |
| **Hindsight** | https://github.com/vectorize-io/hindsight, MIT, 61.6k stars | Four networks (world facts, experiences, entity summaries, beliefs); retain / recall / reflect (arXiv 2512.12818) [S] | 91.4% LongMemEval with Gemini-3 Pro; 83.6% with the open 20B model [S] | Headline number depends on the large backbone |
| **Mastra observational memory** | https://mastra.ai/research/observational-memory; repo license not identified by the GitHub API | Observer turns messages into dated, priority-tagged observations at a token threshold; Reflector condenses them. Text only, prompt-cache friendly [V] | 94.87% LongMemEval with gpt-5-mini; 84.23% with gpt-4o [V] | Multi-session category tops out at 87.2% [V]; initially ran synchronously [S] |

### B8. Coding-agent add-ons
- **claude-mem:** https://github.com/thedotmack/claude-mem. Apache-2.0, 118k stars [V][M]. Older write-ups say AGPL-3.0; the repo now reports Apache-2.0.
  - Hooks (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SessionEnd) send activity to a local worker.
  - An observer agent built on the Claude Agent SDK compresses it into observations and session summaries.
  - Storage is SQLite FTS5 with optional Chroma.
  - Sessions start with a compact index; three MCP tools (search, timeline, get_observations) fetch detail.
  - Supports Claude Code, Codex, Cursor, OpenCode and others.
  - The README mentions a third-party "CMEM" crypto token.
- **beads (Steve Yegge, now `gastownhall/beads`):** https://github.com/gastownhall/beads. MIT, 28.8k stars [V][M].
  - A graph issue tracker on Dolt (versioned SQL) that replaces markdown plans.
  - `bd ready` lists unblocked work, `bd update --claim` claims it, `bd prime` injects workflow context, `bd remember` stores project facts.
  - "Memory decay" summarises old closed tasks; hash IDs avoid merge collisions across agents and branches.
  - `bd init` writes AGENTS.md and installs harness integrations.

### B9. Other harnesses
- **OpenAI Codex:** https://developers.openai.com/codex/memories (redirects to learn.chatgpt.com) [V]
  - Off by default locally (`[features] memories = true`).
  - Generated in the background after a chat goes idle, with secrets redacted, into `~/.codex/memories_v2/`.
  - The files are generated and not meant for hand editing; required team guidance belongs in AGENTS.md.
  - Config keys include `memories.extract_model` and `memories.consolidation_model`.
  - The two-phase pipeline and the 6-hour idle threshold come from third parties only [S].
- **ChatGPT memory:** Saved memories plus a "continually updated synthesis" of past chats (https://help.openai.com/en/articles/11146739-how-does-reference-saved-memories-work) [S]. Internal retrieval architecture not found.
- **Cursor:** The docs page at `/docs/context/memories` now shows the Rules documentation with no mention of memories; persistence is via Project, User and Team Rules and AGENTS.md (https://cursor.com/docs/context/memories) [V]. Forum staff posts conflict on whether Memories was removed in 2.1 or only lost its UI [S].
- **Hermes agent (Nous Research):** https://hermes-agent.nousresearch.com/docs/user-guide/features/memory. MIT [V][M].
  - `MEMORY.md` (2,200 chars) and `USER.md` (1,375 chars) are hard-capped; an over-limit write errors rather than silently dropping.
  - They load as a frozen snapshot at session start to preserve the prompt cache.
  - Tool actions are add / patch / remove.
  - Past sessions sit in SQLite FTS5 and return raw messages, not summaries.
  - A background self-improvement review after turns can write memory or create and update skills, gated by `skills.write_approval`.
  - External providers include Honcho, Hindsight, Supermemory and Mem0.
- **OpenClaw:** https://docs.openclaw.ai/concepts/memory. MIT [V][M].
  - `MEMORY.md` (curated, loaded at start), `memory/YYYY-MM-DD.md` daily notes (today and yesterday loaded, the rest searchable), optional `USER.md` and `DREAMS.md`.
  - `memory_search` is hybrid vector plus keyword; `memory_get` reads a file or range.
  - A memory flush runs before compaction.
  - Dreaming is a cron job that promotes items into MEMORY.md only past score, recall-frequency and query-diversity gates. The live docs say it is on by default; older mirrors say off.
  - An optional Memory Wiki plugin adds claims, evidence and lint.
- **OpenCode:** No native memory documentation found in this research (I did not search for it specifically).

### B10. Multi-agent and multi-session shared memory
- **Anthropic's progress-file pattern** (B5) is the vendor-documented version [V].
- **Letta** has subagents write memory in parallel via git worktrees [V].
- **beads** uses claims, hash IDs and Dolt merges [V].
- **Community patterns [S]:** an append-only work log plus handoff files, with a SessionStart hook injecting a bounded slice and a Stop hook committing back. Examples: https://github.com/daystar7777/agent-work-mem, https://towardsdatascience.com/unified-agentic-memory-across-harnesses-using-hooks/, https://codex.danielvaughan.com/2026/04/18/git-backed-team-memory-egregore-codex-hooks/. One recurring point is that hook-driven logging does not depend on the model remembering to write.
- **"Bitácora":** No English-language source uses the term; the equivalents are `log.md` (Karpathy), `claude-progress.txt` (Anthropic) and `LOG.txt` (OptMem).

---

## Part C — Practitioner consensus, late 2026

**Where there is broad agreement**
1. **Files first for coding harnesses.** Claude Code, Codex, OpenClaw, Hermes and Letta all store memory as markdown the user can read and edit [V for each]. Letta moved from memory-block tools to git-backed files [V]. Mastra's top LongMemEval result is text-only with no vector or graph DB [V].
2. **Small always-loaded index plus on-demand detail.** Claude Code's 200-line / 25KB index, Hermes's character caps, Letta's `system/` directory and claude-mem's compact index are the same design, and it matches Anthropic's "attention budget" guidance [V].
3. **Separate human-authored rules from machine-written memory.** CLAUDE.md vs auto memory; AGENTS.md vs Codex memories; rules win conflicts and are the team-shared layer [V].
4. **Consolidation happens offline.** Dreams, OpenClaw dreaming, Letta reflection, Hermes background review, Mastra's Reflector and Codex consolidation all move cleanup out of the hot path [V]. Anthropic's version writes to a new store so the result is reviewable [V].
5. **Explicit handoff artifacts plus a start routine** for multi-session work [V].
6. **Benchmarks are weak evidence.**
   - A LoCoMo audit found 6.4% of the answer key wrong and a lenient judge (https://penfieldlabs.substack.com/p/we-audited-locomo-64-of-the-answer-key-is-wrong-and-the-judge-accepts-up-to-63-of-intentionally) [S; the auditor is itself a memory vendor].
   - Nearly all published scores are self-reported.
   - MemPalace showed how retrieval recall gets presented as if it were QA accuracy [V].

**Open disagreements**
- **Files vs structured memory at scale.** Nicolò Boschi (works on Hindsight, bias disclosed) argues files are a "necessary foundation" but not sufficient: context rot from 50 to 500 files, weak multi-hop and temporal queries. He concedes he has no controlled benchmarks (https://buttondown.com/nicoloboschi/archive/file-based-agent-memory-great-demo-good-luck-in/) [V]. One 2026 paper found a graph far ahead of flat files on structural questions (arXiv 2608.13662) [S].
- **Verbatim vs extracted.** MemPalace and OptMem keep raw text; Mem0, Mastra and claude-mem distil. The MemPalace paper notes Mem0's 2026 update narrowed the gap [V].
- **Agent-curated vs automatic capture.** Claude Code and Hermes rely on the model's judgment; claude-mem and hook-based systems capture everything; OptMem makes the agent do the summarising inline with no background process [V].
- **Delete vs never delete.** Mem0 went ADD-only, Graphiti invalidates, OptMem never deletes, Dreams replaces contradicted entries.
- **Whether lexical search is enough.** Karpathy says an index file suffices to about 100 sources and suggests qmd (BM25 plus vector) beyond that [V]; OpenClaw defaults to hybrid search [V]; Letta's "filesystem" win included a semantic search tool [V].

**Not found or unverified**
- Official Claude Code documentation of Auto Dream / `/dream`.
- A license for OptMem.
- Any project named "OptiMem".
- Internal architecture of ChatGPT memory.
- A primary source for MemOS.
- Independent head-to-head benchmarks across these systems.
- Cognee, Supermemory, LangMem, Zep, Hindsight and A-MEM details beyond repo metadata are from search snippets only.
