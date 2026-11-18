<!-- Salida original de un subagente de investigación web (Claude Code, 17-nov-2026). Sin editar, salvo quitar rutas locales. [P]/[V] = leído en la página; [S] = solo fragmento de búsqueda. Las páginas se leyeron a través de un resumidor: verificar cada cifra en su fuente antes de citarla. -->

# Long-term memory benchmarks for LLM agents: what exists and what systems score (as of 2026-11-17)

**Provenance legend.** **[P]** = I fetched the source page and the number was on it. **[S]** = seen only in a search-result snippet; not verified on the page. Page reads went through WebFetch's summarizing model, so re-open the source before quoting any figure publicly. Almost every vendor number is self-reported.

---

## 1. "OptMem": what it actually is

- **It is a memory system, not a benchmark or a paper.** OptMem is a small persistent-memory tool for coding agents. The page I read is a fork, [sabitm/optmem](https://github.com/sabitm/optmem), of VictorTaelin/OptMem. [P]
- **Design.** A "426-token prompt" plus one dependency-free Python script. Memories go into fixed-width slots in an append-only log, with a rebuildable summary tree on top. Commands are `wake`, `note`, `recall`, `zoom`, `nap`, `forget`, `edit`, `delete`, `migrate`. It installs as a manual skill for Claude Code and pi. [P]
- **Benchmark claims: none.** The repo page reports no LoCoMo, LongMemEval or other scores and compares itself to no other system. [P]
- **Third-party notes.** Reviews describe retrieval as regex-based rather than semantic, and there is a Hermes plugin, [rarf/optmem-hermes-plugin](https://github.com/rarf/optmem-hermes-plugin), described as "append-only, decay-compressed, BM25 search". [S]
- **Not found.** I found no benchmark or arXiv paper named OptMem or OptiMem. The other hits are unrelated (an Illinois Tech memory-architecture project and an IBM HMC command). [S]

---

## 2. Benchmarks

### LoCoMo
- **Creators and year:** Maharana et al., UNC Chapel Hill, USC and Snap, Feb 2024. [arXiv 2402.17753](https://arxiv.org/abs/2402.17753) [P]
- **Measures:** QA in five categories (single-hop, multi-hop, temporal, open-domain, adversarial), plus event summarization and multimodal dialogue generation. [P]
- **Shape per the paper:** 50 dialogues, about 19.3 sessions (up to 35), about 305 turns and about 9.2K tokens per conversation, with 7,512 questions. [P]
- **Shape as actually used:** 1,986 QA pairs, of which 1,540 are non-adversarial. Vendors score the 1,540 and drop category 5. [P: [MemPalace BENCHMARKS.md](https://github.com/MemPalace/mempalace/blob/main/benchmarks/BENCHMARKS.md), [Penfield audit](https://penfieldlabs.substack.com/p/we-audited-locomo-64-of-the-answer)] The released subset is 10 conversations; that figure is from my background knowledge, not read on a page this session.
- **Metric:** the paper uses F1 (human 87.9, best model 41.4). [P] Vendors use an LLM-judge "J" score instead, usually with gpt-4o-mini as judge.
- **Criticisms:**
  - **Fits in context.** Conversations are about 16–26K tokens. Mem0's own paper has full-context at 72.90 against Mem0's best of 68.44. [P: [Zep blog](https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/), [Mem0 paper](https://arxiv.org/html/2504.19413)]
  - **Wrong answer key.** 99 of 1,540 golden answers are wrong (6.4%), giving a ceiling of about 93.57%. [P: [locomo-audit](https://github.com/dial481/locomo-audit)]
  - **Lenient judge.** The gpt-4o-mini judge accepted 62.81% of intentionally wrong but on-topic answers, and 10.61% of specific-but-wrong ones. [P: same audit]
  - **Prompt beats memory.** GPT-4.1-mini with full context and a chain-of-thought answer prompt scored 92.62%, above EverMemOS's claimed 92.32%. [P: same audit]
  - **Design gaps.** No knowledge-update questions, category 5 lacks ground truth, there are speaker-attribution errors, and some image questions are unanswerable. [P: Zep blog]

### LongMemEval (v1)
- **Creators and year:** Wu et al., Oct 2024, ICLR 2025. [arXiv 2410.10813](https://arxiv.org/abs/2410.10813) [P]
- **Measures:** information extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention. [P]
- **Shape:** 500 questions over user-assistant histories. [P] The S split is about 115K tokens per question. [P: [Zep paper](https://arxiv.org/html/2501.13956)]
- **Metric:** LLM-judge binary accuracy, with GPT-4o as the official judge. [P: [Redis report](https://redis.io/resources/agent-memory-benchmark-report/)]
- **Criticisms:**
  - **S now fits in context windows**, so it rewards context compression rather than memory. [P: Penfield]
  - **Small categories.** Preferences has 30 questions (about ±18% margin) and some subgroups have as few as 6. [P: [ConvoMem](https://arxiv.org/html/2511.10523v1)]
  - **Exploitable filler.** Filler conversations come from other datasets and differ in style. [P: ConvoMem]
  - **Metric mixing.** Vendors mix retrieval recall@k with QA accuracy, and swap judge and answer models.

### LongMemEval-V2
- **Creators and year:** Wu et al., UCLA, 2026. [arXiv 2605.12493 / project page](https://xiaowu0162.github.io/longmemeval-v2/) [P]
- **Measures:** static state recall, dynamic state tracking, workflow knowledge, environment gotchas, premise awareness. It targets agent experience, not chat. [P]
- **Shape:** 451 curated questions over up to 500 multimodal web-agent trajectories, 25M–115M tokens. [P]
- **Metric:** accuracy plus latency, and a "LAFS Gain" frontier score. [P]
- **Status:** leaderboard submissions are "coming soon"; no vendor numbers yet. [P]

### DMR (Deep Memory Retrieval)
- **Creators and year:** introduced with MemGPT (Packer et al., Oct 2023, [arXiv 2310.08560](https://arxiv.org/abs/2310.08560)).
- **Shape:** 500 conversations drawn from MSC, each with 5 sessions of up to 12 messages and one QA pair. [P: Zep paper]
- **Metric:** LLM-judge accuracy.
- **Criticisms (Zep's own paper):** single-turn fact retrieval only, ambiguous questions, about 60 messages fits any context window, and full-conversation scores 94.4–98.0%. It is saturated and effectively retired. [P]

### MSC (Multi-Session Chat)
- **Creators and year:** Xu, Szlam and Weston (Facebook AI), "Beyond Goldfish Memory", 2021/ACL 2022. [arXiv 2107.07567](https://arxiv.org/pdf/2107.07567)
- **Shape:** human-human crowdworker chats over up to 5 sessions of up to 14 utterances each; 4,000 three-session and 1,001 four-session training episodes. [S]
- **Role today:** a dialogue-generation dataset that is the substrate for DMR, not a memory-system leaderboard.

### PerLTQA
- **Creators and year:** Du et al., SIGHAN 2024. [arXiv 2402.16288](https://arxiv.org/pdf/2402.16288)
- **Shape:** 8,593 QA pairs, 141 character profiles (30 annotated), 23,697 memory anchors; Chinese. [S]
- **Measures:** memory classification (semantic vs episodic), retrieval and synthesis.
- **Criticism:** no interactive dialogue. [P: ConvoMem]
- **Vendor scores:** none found.

### MemoryAgentBench
- **Creators and year:** Hu, Wang and McAuley (UCSD), July 2025. [arXiv 2507.05257](https://arxiv.org/html/2507.05257v3) [P] Reported as ICLR 2026. [S]
- **Measures:** Accurate Retrieval, Test-Time Learning, Long-Range Understanding, and Selective Forgetting (called conflict resolution in v1).
- **Shape:** long-context datasets chunked and fed incrementally, from 124K to 1.44M tokens. It adds two new datasets, EventQA and FactConsolidation. [P]
- **Metrics:** accuracy, F1, Recall@5, depending on task. [P]
- **Key finding:** nothing masters all four, and multi-hop forgetting tops out at 7%. [P]
- **Criticism:** too small for statistical significance. [P: ConvoMem]

### MemBench
- **Creators and year:** Tan et al., Renmin University and Huawei Noah's Ark, June 2025. [arXiv 2506.21605](https://arxiv.org/html/2506.21605v1) [P] MemPalace labels it "ACL 2025"; I did not verify the venue.
- **Measures:** factual vs reflective memory, in participation vs observation scenarios.
- **Shape:** 500 user-relation graphs; multiple-choice questions. [P]
- **Metrics:** accuracy, recall, capacity, temporal efficiency. [P]
- **Evaluated:** research mechanisms only (FullMemory, RetrievalMemory, RecentMemory, GenerativeAgent, MemoryBank, MemGPT, SCMemory) on Qwen2.5-7B. No commercial systems. [P]

### BEAM
- **Creators and year:** Tavakoli et al., University of Alberta and UMass Amherst, Oct 2025. [arXiv 2510.27246](https://arxiv.org/html/2510.27246v1) [P] A v2 is labelled ICLR 2026. [S]
- **Shape:** 100 conversations at 100K, 500K, 1M and 10M tokens, with 2,000 questions. [P]
- **Measures (10 abilities):** abstention, contradiction resolution, event ordering, information extraction, instruction following, knowledge update, multi-hop, preference following, summarization, temporal reasoning. [P]
- **Metric:** nugget-based LLM judge scoring 0, 0.5 or 1; Kendall tau-b for event ordering. [P]
- **Why it matters:** it is the only widely used test where context-stuffing fails. At 10M tokens, long-context scores 0.10–0.13. [P]
- **Criticism:** synthetic, and the vendor numbers so far are all self-run.

### ConvoMem
- **Creators and year:** Pakhomov, Nijkamp and Xiong (Salesforce AI Research), Nov 2025. [arXiv 2511.10523](https://arxiv.org/html/2511.10523v1) [P]
- **Shape:** 75,336 QA pairs. [P]
- **Measures:** user facts, assistant facts, changing facts, abstention, preferences, implicit connections; evidence spread over 1–6 messages. [P]
- **Key finding:** long context wins for the first 30 or so conversations and is viable to about 150. Mem0 scored 30–45% on preferences and implicit connections, but is up to 95x cheaper. [P]
- **Caveat:** the paper's own thresholds are internally inconsistent across sections. [P]

### LoCoMo-Plus
- **Creators and year:** Li et al., Xi'an Jiaotong and Tencent, Feb 2026. [arXiv 2602.10715](https://arxiv.org/html/2602.10715) [P] Accepted at ACL 2026. [S]
- **Measures:** "cognitive" memory (causal, state, goal and value constraints) where the cue and the trigger are semantically disconnected. [P]
- **Metric:** LLM judge (gemini-2.5-flash or GPT-4o). [P]
- **Criticisms:** it inherits LoCoMo's 99 answer-key errors, and its judge was validated only on the new questions. [P: Penfield]

### Newer benchmarks found (2026)

| Benchmark | What it is | Provenance |
|---|---|---|
| AMA-Bench ([arXiv 2602.22769](https://arxiv.org/abs/2602.22769)) | Memory over agent-environment trajectories. Existing memory systems underperform; the authors' AMA-Agent reaches 57.22%. | [S] |
| MemoryArena ([arXiv 2602.16313](https://arxiv.org/abs/2602.16313)) | Multi-session tasks where memory and action are coupled. Agents that saturate LoCoMo struggle. | [S] |
| SWE-ContextBench ([arXiv 2602.08316](https://arxiv.org/abs/2602.08316)) | Coding-agent memory: does memory help fix related bugs (99 tasks). | [P via [Supermemory's compare page](https://supermemory.ai/compare/supermemory-vs-mem0.md)] |
| CAPA (arXiv 2607.26611) | Coding: does the agent stop re-asking questions answered in earlier sessions (600 sessions). | [S] |
| DreamBench-SWE (arXiv 2608.20664) | Coding: multi-session memory hygiene, scored by hidden executable oracles. | [S] |
| LongMemCode | Retrieval component of coding-agent memory. | [S] |
| ContextWeave (arXiv 2608.04830) | Office-work streams with and without prior history. | [S] |
| "Are We Ready For An Agent-Native Memory System?" ([arXiv 2606.24775](https://arxiv.org/abs/2606.24775)) | Independent academic study of 12 systems and 2 baselines over 11 datasets. I did not extract its numbers. | [S] |
| Letta Leaderboard / Context-Bench / FrontierMemory | Letta-run benchmarks of how well models manage agentic memory. | [S] |
| DolphinBench | Mem0-built; 600 tests, about 500K tokens of history per persona. | [P: [Mem0 post](https://mem0.ai/library/agent-memory/ai-memory-benchmarks-in-2026)] |
| STATE-Bench | Microsoft; GPT-5.1 without memory solves about 30% of travel tasks. | [P: same Mem0 post] |

---

## 3. Reported scores

"Self" means the vendor reported its own system. "Competitor" means a rival vendor ran or cited it. "Independent" means academic or a party with no product in the table.

### LoCoMo (LLM-judge accuracy unless noted)

| System | Score | Model / config | Reported by | Source | Prov. |
|---|---|---|---|---|---|
| Full-context | 72.90 ± 0.19 | gpt-4o-mini | Mem0 paper | [arXiv 2504.19413](https://arxiv.org/html/2504.19413) | P |
| Mem0 graph | 68.44 ± 0.17 | gpt-4o-mini | Self | same | P |
| Mem0 base | 66.88 ± 0.15 | gpt-4o-mini | Self | same | P |
| Zep | 65.99 ± 0.16 | — | Competitor (Mem0) | same | P |
| RAG (best: k=2, 256-token chunks) | 60.97 ± 0.20 | — | Mem0 paper | same | P |
| LangMem | 58.10 ± 0.21 | gpt-4o-mini | Competitor (Mem0) | same | P |
| OpenAI memory | 52.90 ± 0.14 | gpt-4o-mini | Competitor (Mem0) | same | P |
| A-MEM (re-run) | 48.38 ± 0.15 | gpt-4o-mini | Competitor (Mem0) | same | P |
| MemGPT / Letta | Not reported in the tables I read | — | — | same | P |
| Zep, original claim | 84% | — | Self, later retracted | [zep-papers issue #5](https://github.com/getzep/zep-papers/issues/5) | P |
| Zep, Mem0's re-run | 58.44 ± 0.20 | — | Competitor (Mem0) | same | P |
| Zep, corrected | 75.14 ± 0.17 | — | Self | same; [Zep blog](https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/) | P |
| Zep, 2026 claim | 94.7% (1,459/1,540) | gpt-5.4 reader and judge | Self | getzep.com/research | S |
| Letta filesystem (grep/file tools) | 74.0% | gpt-4o-mini | Self | [Letta blog](https://www.letta.com/blog/benchmarking-ai-agent-memory) | P |
| Mem0, new algorithm (Apr 2026) | 92.5 (old: 71.4) | models undisclosed; managed platform | Self | [Mem0 blog](https://mem0.ai/blog/mem0-the-token-efficient-memory-algorithm) | P |
| Hindsight | 89.61% | "larger backbone" | Self | [arXiv 2512.12818](https://arxiv.org/abs/2512.12818) | P |
| Hindsight | 83.18% / 85.67% | OSS-20B / OSS-120B | Self | hindsight-benchmarks repo | S |
| Memobase v0.0.37 | 75.78 (temporal 85.05) | — | Self | memobase repo README (via mirror) | S |
| MemOS-1031 | 75.80 | — | Self | MemOS paper / HF card | S |
| Memobase, in MemOS's table | 72.01 | — | Competitor | same | S |
| MIRIX / Mem0, in MemOS's table | 64.33 / 59.22 | — | Competitor | same | S |
| EverMemOS | 92.32% | GPT-4.1-mini | Self | [locomo-audit](https://github.com/dial481/locomo-audit) | P |
| EverMemOS, third-party reproduction | 38.38% | — | Independent | same | P |
| Full-context + CoT prompt | 92.62% | GPT-4.1-mini | Independent | same | P |
| Cognee | 80.3% | — | Aggregator | search result | S |
| Dakera / ByteRover / ZeroMemory | 88.2% / 92.2% or 96.1% / 96.1% | — | Self | [Mem0 post](https://mem0.ai/library/agent-memory/ai-memory-benchmarks-in-2026) | P (as cited by Mem0) |
| Supermemory | "#1", no number published | — | Self | [supermemory.ai/research](https://supermemory.ai/research.md) | P |
| MemPalace | 100% at top-50; 60.3% R@10 (session, no rerank); 88.9% R@10 (hybrid v5) | retrieval recall, not QA accuracy | Self | [BENCHMARKS.md](https://github.com/MemPalace/mempalace/blob/main/benchmarks/BENCHMARKS.md) | P |
| A-MEM, own paper | F1 45.85 vs MemGPT 25.52 | gpt-4o-mini; F1, not J | Self | [arXiv 2502.12110](https://arxiv.org/pdf/2502.12110) | S |

LoCoMo-Plus, from the paper (independent academic) [P]: on LoCoMo / LoCoMo-Plus, with GPT-4o as backbone where applicable:

| System | LoCoMo | LoCoMo-Plus |
|---|---|---|
| Mem0 | 57.24 | 15.80 |
| A-Mem | 59.64 | 17.20 |
| SeCom | 57.53 | 14.90 |
| RAG (text-embedding-large) | 45.32 | 15.55 |
| GPT-4o full context | 62.99 | 21.05 |
| Gemini-2.5-pro full context (best) | 71.78 | 26.06 |

### LongMemEval (S split, QA accuracy unless noted)

| System | Score | Model | Reported by | Source | Prov. |
|---|---|---|---|---|---|
| Full-context | 60.2% / 55.4% | gpt-4o / gpt-4o-mini | Zep paper | [arXiv 2501.13956](https://arxiv.org/html/2501.13956) | P |
| Zep | 71.2% / 63.8% | gpt-4o / gpt-4o-mini | Self | same | P |
| Zep, 2026 claim | 90.2% | gpt-5.4 reader and judge | Self | getzep.com/research | S |
| Oracle (evidence sessions only) | 82.4% | gpt-4o | Mastra | [Mastra research](https://mastra.ai/research/observational-memory) | P |
| Mastra Observational Memory | 84.23% / 93.27% / 94.87% | gpt-4o / gemini-3-pro / gpt-5-mini | Self | same | P |
| Mastra OM | 84.2% | Gemini + GPT-4o | Reproduced by Redis | [Redis report](https://redis.io/resources/agent-memory-benchmark-report/) | P |
| Mastra plain RAG (topK 20) | 80.05% | gpt-4o | Self | Mastra research | P |
| Hindsight | 91.4% / 89.0% / 83.6% | gemini-3-pro / OSS-120B / OSS-20B | Self | [arXiv 2512.12818](https://arxiv.org/abs/2512.12818); Mastra table | P |
| Hindsight, full-context baseline | 39% | same 20B model | Self | Hindsight abstract | P |
| Supermemory | 81.6% / 84.6% / 85.2% | gpt-4o / gpt-5 / gemini-3-pro | Cited by Mastra and Redis | Mastra research; Redis report | P |
| Supermemory | 97% | gpt-4o; page labels the metric "Recall@20 with aggregation" | Self | [supermemory.ai/research](https://supermemory.ai/research.md) | P |
| Supermemory "ASMR" | ~99% (experimental) | — | Self | cited in MemPalace BENCHMARKS.md | P (secondary) |
| EmergenceMem | 86.0% internal / 82.4% Simple / 79.0% Simple Fast | gpt-4o | Self | Mastra research; emergence.ai | P (via Mastra) |
| Emergence-fast | 81.3% (reported 82.4%) | — | Reproduced by Redis | Redis report | P |
| Mem0, new algorithm | 94.4 (old: 67.8) | undisclosed | Self | [Mem0 blog](https://mem0.ai/blog/mem0-the-token-efficient-memory-algorithm) | P |
| Mem0 hosted, observed | 57.5% before / 73.8% after the Apr 14 update | gpt-5, 5 seeds, author's own judge prompt | Competitor (Maximem/Synap) | [DEV post](https://dev.to/gaurav_dadhich/the-state-of-ai-memory-in-2026-claimed-vs-observed-1n94) | P |
| Mem0, older | 49.0% | — | Cited by Redis and Vectorize | Redis report; [Vectorize](https://vectorize.io/articles/mempalace-benchmarks) | P (secondary) |
| Redis Remis + Instruct / Remis / AMS | 86.5% / 83.4% / 64.0% | gpt-4o | Self | Redis report | P |
| RAG-mem k=20 | 61.5% | gpt-4o | Redis | same | P |
| Oracle Agent Memory | 93.8% claimed; 86.0% reproduced; 78.1% on gpt-4o | gpt-5.5 xhigh | Self / Redis | same | P |
| Amazon Bedrock AgentCore | 73.6% reported; 77.0% reproduced | — | Redis | same | P |
| Google Vertex Memory Bank | ~70% (paper); 42.4% reproduced | gpt-4o | Redis | same | P |
| LangMem | Not found — Redis row was garbled in extraction | — | — | same | — |
| OMEGA / PwC Chronos | 95.4% / 92.6% | GPT-4.1 / GPT-4o | Self, as cited by Redis | same | P |
| MemOS / Memobase | 77.8% / 72.4% | — | Self (MemOS) | MemOS HF card | S |
| EverMemOS / ByteRover | 82% / 92.8% | — | Self, as cited by Mem0 | [Mem0 post](https://mem0.ai/library/agent-memory/ai-memory-benchmarks-in-2026) | P |
| Exabase M-1 | 96.4% | Gemini 3 Flash | Self (press release) | hpcwire | S |
| MemPalace, raw ChromaDB | 96.6% R@5 | retrieval recall, no LLM | Self; reproduced in GitHub issue #39 | BENCHMARKS.md; Vectorize | P |
| MemPalace, hybrid v4 | 100% R@5 (tuned on 3 failing questions); 98.4% held-out | retrieval recall | Self | BENCHMARKS.md | P |
| MemPalace, rooms on / AAAK compression | 89.4% / 84.2% R@5 | retrieval recall | Issue #39, per competitor | Vectorize | P |
| BM25 / Contriever / Stella | ~70% / ~78% / ~85% | retrieval, not QA | Cited by MemPalace | BENCHMARKS.md | P |
| Letta / MemGPT | 65.0% | — | Unofficial aggregator | search result | S |

LongMemEval-V2 baselines (benchmark authors, independent) [P], Small / Medium splits:

| Method | Small | Medium |
|---|---|---|
| No retrieval | 1.3% | 1.3% |
| RAG (query to slice) | 42.8% | 38.1% |
| RAG + notes | 51.0% | 45.9% |
| AgentRunbook-R | 58.6% | 57.0% |
| Codex (coding agent) | 69.9% | 68.7% |
| AgentRunbook-C | 74.9% | 70.1% |

### DMR
From the [Zep paper](https://arxiv.org/html/2501.13956) [P]; rows marked † are taken from the MemGPT paper.

| System | gpt-4-turbo | gpt-4o-mini |
|---|---|---|
| Recursive summarization † | 35.3% | — |
| Conversation summaries | 78.6% | 88.0% |
| MemGPT † | 93.4% | — |
| Full-conversation | 94.4% | 98.0% |
| Zep | 94.8% | 98.2% |

### BEAM

| System | 100K | 500K | 1M | 10M | Reported by | Source | Prov. |
|---|---|---|---|---|---|---|---|
| Hindsight | 73.4 | 71.1 | 73.9 | 64.1 | Self | [Hindsight blog](https://hindsight.vectorize.io/blog/2026/04/02/beam-sota) | P |
| Honcho | 63.0 | 64.9 | 63.1 | 40.6 | "Published", cited by Hindsight | same | P |
| LIGHT (Llama-4-Maverick) | 35.8 | 35.9 | 33.6 | 26.6 | BEAM authors | [BEAM paper](https://arxiv.org/html/2510.27246v1) | P |
| RAG (Llama-4-Maverick) | 32.3 | 33.0 | 30.7 | 24.9 | BEAM authors | same | P |
| Long-context (4 models) | 24–28 | 19–28 | 19–26 | 10–13 | BEAM authors | same | P |
| Mem0, new algorithm | — | — | 64.1 | 48.6 | Self | [Mem0 blog](https://mem0.ai/blog/mem0-the-token-efficient-memory-algorithm) | P |
| Exabase M-1 | — | — | — | 68.0 | Self (press release) | hpcwire | S |

### MemoryAgentBench
Independent academic; gpt-4o-mini backbone unless noted. [arXiv 2507.05257v3](https://arxiv.org/html/2507.05257v3) [P]

| Agent | AR | TTL | LRU | SF | Overall |
|---|---|---|---|---|---|
| GPT-4o long-context | 58.1 | 50.0 | 54.9 | 32.5 | 48.8 |
| GPT-4o-mini long-context | 49.2 | 48.6 | 46.2 | 25.0 | 42.2 |
| HippoRAG-v2 | 65.1 | 35.8 | 36.2 | 29.5 | 41.6 |
| BM25 | 60.5 | 44.5 | 35.6 | 25.5 | 41.5 |
| Text-Embed-3-Small RAG | 53.8 | 42.7 | 36.3 | 15.5 | 37.1 |
| MIRIX (GPT-4.1-mini) | 63.0 | 35.7 | 40.5 | 11.5 | 37.7 |
| MemGPT | 34.3 | 40.8 | 22.4 | 15.5 | 28.3 |
| Zep | 37.5 | 37.5 | 16.2 | 5.0 | 24.0 |
| GraphRAG | 40.9 | 24.8 | 19.9 | 8.0 | 23.4 |
| Mem0 | 32.6 | 21.2 | 20.7 | 10.0 | 21.1 |
| Cognee | 28.3 | 22.8 | 16.0 | 15.5 | 20.6 |

### ConvoMem, MemBench, SWE-ContextBench, other

| System | Benchmark | Score | Reported by | Source | Prov. |
|---|---|---|---|---|---|
| Long context (Gemini) | ConvoMem | 70–82% on the hardest multi-message cases; about 82% falling to about 65% at 300 conversations | Independent (Salesforce) | [arXiv 2511.10523](https://arxiv.org/html/2511.10523v1) | P |
| Mem0 | ConvoMem | 30–45% on preferences and implicit connections; user facts 77.5% vs 94.7% for long context | Independent (Salesforce) | same | P |
| MemPalace | ConvoMem | 92.9%, on a 300-item sample (about 0.4% of the set) | Self | BENCHMARKS.md; [Vectorize](https://vectorize.io/articles/mempalace-benchmarks) | P |
| MemPalace | MemBench | 80.3% R@5 | Self | BENCHMARKS.md | P |
| Supermemory | ConvoMem | "#1", no number | Self | supermemory.ai/research | P |
| Supermemory / Mem0 / no memory | SWE-ContextBench, tasks resolved | 30.30% / 24.24% / 26 of 99 | Described as independent (Zhu et al.); read only via Supermemory's page | [compare page](https://supermemory.ai/compare/supermemory-vs-mem0.md) | P (secondary) |
| Cognee | HotPotQA, 24-question subset | 0.93 human-like correctness; LightRAG 0.96 | Self, tuned only for Cognee | cognee.ai | S |
| Hermes + GPT-5.6-Luna + Mem0 | DolphinBench | 70.67% | Self (Mem0's own benchmark) | Mem0 post | P |

**Not found on any primary page:** LangMem's own scores (only Mem0's competitor-run 58.10 on LoCoMo), an official Letta LongMemEval number, a Supermemory LoCoMo number, and any Cognee, Memobase or A-MEM score on LongMemEval that I could verify on-page.

---

## 4. The disputes

- **Mem0 vs Zep (May 2025).** Mem0's paper put Zep at 65.99. Zep had claimed 84%. Mem0's CTO opened an issue saying the true figure was 58.44, because Zep had counted category 5 in the wrong place. Zep conceded the calculation error and corrected to 75.14, then accused Mem0 of misconfiguring Zep (both speakers given the user role, timestamps appended instead of using `created_at`, sequential searches). The issue was closed without agreement. [P: [issue #5](https://github.com/getzep/zep-papers/issues/5), [Zep blog](https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/)]
- **Mem0 vs Letta (Aug 2025).** Letta says it could not find a way to backfill LoCoMo into MemGPT, and that Mem0 never explained how it produced MemGPT numbers. Letta then scored 74.0% with an agent using plain file tools, against Mem0's 68.5%. [P: [Letta blog](https://www.letta.com/blog/benchmarking-ai-agent-memory)]
- **Mem0's 2026 jump.** Mem0 claims LoCoMo 71.4 to 92.5 and LongMemEval 67.8 to 94.4, on its managed platform with answer and judge models undisclosed. A competitor (Maximem) observed 57.5% and then 73.8% on LongMemEval with a neutral harness, and attributes the gap to benchmark-specific answer and judge prompts. That reading is the author's and unverified. That post quotes Mem0's claim as 93.4%, while Mem0's page says 94.4%. [P]
- **MemPalace (Apr 2026).** The headline "100%" figures were retrieval recall, not QA accuracy. The LongMemEval 100% was tuned on the three failing questions. The LoCoMo 100% used top-50 retrieval over conversations with only 19–32 sessions, so retrieval was bypassed. The clean 96.6% is plain ChromaDB with none of the "palace" features, and enabling those features lowers the score. The project's own BENCHMARKS.md now concedes most of this and removed its comparison table. [P] The sharpest critique is published by Vectorize, which makes Hindsight. [P]
- **Zep's 2026 numbers (94.7% / 90.2%)** use gpt-5.4 as both reader and judge, so they are not comparable with its 2025 gpt-4o figures. [S]

---

## 5. Takeaways

1. **LoCoMo is broken as a ranking tool.** It fits in context, 6.4% of the key is wrong (ceiling about 93.6%), and the usual judge passes about 63% of vague wrong answers. A full-context run with a better answer prompt reaches 92.6%, so scores in the 90s mostly measure prompt and judge choices.
2. **Only matched comparisons mean anything.** The same system swings 20 to 45 points with the answer model alone: Hindsight's baseline goes from 39% to 83.6% with memory on a 20B model, and Mastra goes from 84% to 95% by swapping gpt-4o for gpt-5-mini. Compare only rows with the same reader, judge and split.
3. **Vendor numbers for rivals are unreliable.** Zep on LoCoMo has been reported as 58, 66, 75, 84 and 94.7. The most trustworthy sources here are the academic ones (MemoryAgentBench, ConvoMem, LoCoMo-Plus, BEAM) and the Redis reproductions; Redis has its own product in the table but used one harness and judge throughout.
4. **Independent results are humbling.** On MemoryAgentBench, plain BM25 (41.5) and long-context GPT-4o (48.8) beat Mem0 (21.1), Zep (24.0), Cognee (20.6) and MemGPT (28.3). On ConvoMem, long context beats Mem0 for the first 150 or so conversations. Letta's grep-over-a-file agent matched dedicated memory layers on LoCoMo.
5. **Memory pays off on cost, latency and scale, not accuracy on short histories.** ConvoMem puts Mem0 at up to 95x cheaper, and Zep uses 1.6K tokens against 115K. Accuracy gains appear only where context-stuffing fails: BEAM at 1M–10M tokens and LongMemEval-V2 at 25M–115M.
6. **Check the metric before the number.** Retrieval recall@k (MemPalace, and Supermemory's 97%) is not QA accuracy. F1 (the original LoCoMo paper, A-MEM) is not the LLM-judge score.
7. **The hard abilities are still unsolved.** Selective forgetting peaks at 7% for multi-hop on MemoryAgentBench. Implicit-constraint memory tops out at 26% on LoCoMo-Plus. On BEAM at 10M, Mem0 scores 16% on temporal reasoning and 33% on contradiction resolution.
8. **The field is moving to agentic and coding memory.** LongMemEval-V2, AMA-Bench, MemoryArena, SWE-ContextBench, CAPA and DreamBench-SWE test whether memory improves later task execution. Early signals: coding agents with file tools lead LongMemEval-V2 (74.9%), and on SWE-ContextBench, Mem0 resolved fewer tasks than no memory at all (24 vs 26 of 99, as relayed by Supermemory).

**Gaps to close before relying on this:** I did not extract the tables from arXiv 2606.24775 (the 12-system independent study) or from the MemOS paper (the fetch truncated before the evaluation section and the Hugging Face card returned 401). Zep's 94.7% / 90.2% figures and Memobase's 75.78 are snippet-only.
