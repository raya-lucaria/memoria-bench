<!-- Salida original de un subagente de investigación web (Claude Code, 17-nov-2026). Sin editar, salvo quitar rutas locales. [P]/[V] = leído en la página; [S] = solo fragmento de búsqueda. Las páginas se leyeron a través de un resumidor: verificar cada cifra en su fuente antes de citarla. -->

# Memory-benchmark results, Aug–Nov 2026 (current models only where available)

Few vendors have re-run their headline numbers on current models. The current-model results that exist come mostly from Letta (FrontierMemory), Mastra, Mem0 (writer-model sweep only), Hindsight, Anthropic and a handful of smaller vendors. [P] = read on the page, [S] = search snippet only. No number below is estimated.

## A. Vendor results with current models

| System | Benchmark | Metric | Value | Reader model | Judge model | Reported by | Date | URL | Src |
|---|---|---|---|---|---|---|---|---|---|
| Mastra Observational Memory | BEAM-100K | score, avg of 2 runs | 83.3% (83.6 / 83.0) | Claude Opus 5.5 (observer: Gemini 3.8 Flash) | Gemini 3 Flash | self | 2026-10-29 | https://mastra.ai/research/observational-memory-beam | P |
| Mastra OM | BEAM-1M | score | 80.6% (80.6 / 80.7) | Claude Opus 5.5 | Gemini 3 Flash | self | 2026-10-29 | same | P |
| Mastra OM | BEAM-10M | score | 66.4% (67.2 / 65.5) | Claude Opus 5.5 | Gemini 3 Flash | self | 2026-10-29 | same | P |
| Mastra OM | BEAM 100K / 1M / 10M | score, 1 run | 78.4 / 72.8 / 57.8% | Gemini 3.8 Flash | Gemini 3 Flash | self | 2026-10-29 | same | P |
| Mem0 Platform (BYOK, extraction model varied) | LoCoMo, 1,540 q, avg of 2 runs | accuracy by writer | Opus 5.5 93.5; Sonnet 5.5 93.4; GLM-5.3 Flash 93.0; DeepSeek V4.1 Flash 92.9; GPT-6 Luna 92.6; Haiku 5.5 92.3; Gemini 3.8 Flash 92.0 | not stated | not stated | self | 2026-10-20, updated 10-23 | https://mem0.ai/blog/bring-your-own-key-accuracy-cost-latency-by-model | P |
| Mem0 BYOK | same | cost per 1,000 adds / p95 latency | Opus 5.5 $158.55 / 18.1 s; Sonnet 5.5 $78.44 / 10.4 s; GPT-6 Luna $3.55 / 15.2 s; Haiku 5.5 $4.93 / 17.7 s | — | — | self | 2026-10-20 | same | P |
| Hindsight 1.2.0 + hs-decide-1-flash | Hindsight's own system evals | quality, LLM alone → with decision model | glm-5.3-flash 73.8 → 87.1; gemma-4-26b 76.6 → 81.1; deepseek-v4.1-flash 81.9 → 85.1; gemini-3.1-flash-lite 87.1 → 86.6; gemini-3.8-flash 89.0 alone; gpt-6-luna 87.0 with | as listed | gemini-3.1-flash-lite | self | 2026-11-03 | https://hindsight.vectorize.io/blog/2026/11/03/hindsight-models | P |
| Hindsight | same | cost per 1,000 cases, alone → with | gemini-3.8-flash $147 → $61; claude-haiku-5.5 $31 → $18; gpt-6-luna $16 → $9.88 | — | — | self | 2026-11-03 | same | P |
| Hindsight | same | LLM calls per case; reflect input tokens | 4.5 → 3.1; 45K → 7.5K per question (gemini-3.8-flash) | — | — | self | 2026-11-03 | same | P |
| Recallium | LongMemEval-S, 500 q | QA accuracy | 98.4% | Claude Opus 5.5 | gpt-4o-2024-08-06 | self | build 2026-09-30 | https://recallium.ai/benchmarks | P |
| Recallium | LongMemEval-S | no-memory baseline | 6.6% of answerable questions | Claude Opus 5.5 | GPT-4o | self | 2026-09 | same | P |
| Recallium | LongMemEval-S | hit@10 / recall@10 / results served | 99.8% / 98.6% / 3.8 | — | — | self | 2026-09-30 | same | P |
| ContextStream | LongMemEval-S, 500 q | accuracy | 96.8% (484/500); held-out half 96.0% | Claude Opus 5.5 | gpt-4o-2024-08-06 | self | 2026-10-26 | https://contextstream.io/benchmarks | P |
| ContextStream | LoCoMo, 1,540 q | accuracy | 95.7% (1474/1540) | Claude Opus 5.5 | gpt-4o-mini, majority of 3 | self | 2026-10-26 | same | P |

## B. Letta FrontierMemory v1.1 (15 tasks, 3 runs, verifier-scored, no LLM judge)

Memory is written by the listed model in Letta Dream. Tasks are run in Letta Code by Opus 5.5 and GPT-6 Sol at max effort, and the better of the two is the score. The v1.1 corpus dates from 2026-10-29; all rows are self-reported by Letta. One task is worth about 6.7 points.

| Memory writer | Score | Task cost | Src |
|---|---|---|---|
| Qwen4 Max [xhigh] | 73.3% | $0.98 | P |
| Opus 5.5 [max] | 73.3% | $3.42 | P |
| Fable 5.2 [max] | 73.3% | $3.71 | P |
| DeepSeek V4.1 Flash | 71.1% | $3.86 | P |
| Gemini 4 Carbon [high] | 71.1% | $3.99 | P |
| Kimi K3 | 71.1% | $4.16 | P |
| Haiku 5.5 | 68.9% | $3.98 | P |
| GLM-5.3 | 68.9% | $4.08 | P |
| Gemini 4 Argon [high] | 64.4% | $1.05 | P |
| Gemini 4 Hydrogen [xhigh] | 64.4% | $4.02 | P |
| GPT-6.1 Sol | 51.1% | $4.00 | P |
| GPT-6.1 Terra | 46.7% | $3.97 | P |
| Grok 4.7 | 37.8% | $3.70 | P |
| GPT-6 Luna | 28.9% | $4.05 | P |

| Harness | Opus 5.5 memory + task | GPT-6.1 Sol memory + GPT-6 Sol task | Src |
|---|---|---|---|
| Letta Dream | 73.3% | 42.2% | P |
| Hermes Agent | 64.4% | 4.4% | P |
| Claude Managed Agents | 55.6% | — | P |
| Prime Agent | 53.3% | 13.3% | P |
| OpenAI Agents SDK | — | 26.7% | P |

- **Sources:** https://frontiermemory.com/ (v1.1 boards) and https://www.frontiermemory.com/blog/v1/ (per-pairing harness numbers, October 2026).
- **Conflicting secondary figures:** some coverage of v1.0 gives Prime Agent 60%, OpenAI Agents SDK 40%, Claude Managed Agents 33.3% and Hermes 26.7% [S]. These do not match the primary pages; I could not open The New Stack article (403) to reconcile them.
- **Writer × reader detail** (via Maximem's summary, 2026-11-04, https://www.maximem.ai/blog/which-model-should-write-agent-memory [P]):
  - Opus 5.5 memory: 73.3% read by Opus 5.5, 64.4% read by GPT-6 Sol.
  - Fable 5.2 memory: 73.3% / 71.1%.
  - Qwen4 Max memory: 68.9% / 73.3%.

## C. Harness makers

| Maker | Test | Metric | Value | Model | Judge | Date | URL | Src |
|---|---|---|---|---|---|---|---|---|
| Anthropic | CL-Bench 1.0 database task | mean reward, stateless → with memory | Opus 5.5 0.655 → 0.838; Sonnet 5.5 0.644 → 0.833; Opus 5 0.564 → 0.828; Sonnet 5 0.306 → 0.610; Opus 4.7 0.383 → 0.700; Sonnet 4.6 0.330 → 0.364 (0.641 with refined instructions) | as listed | benchmark reward | 2026-11-06 | https://www.anthropic.com/research/components-of-agent-memory | P |
| Anthropic | Stainless wiki, ~350K files, ~420M tokens, 25 questions | % of graded criteria | wiki only 13% → 48% as dreaming scales from 2 to 128 sessions; search alone 53%; search + wiki 54% → 61%; about 20,000 fewer tokens per question | Opus 5 agents | graded criteria | 2026-11-06 | same | P |
| Anthropic | Harvey LAB merger questions (24) | score on multi-document / judgment / math items | wiki 87% vs search alone 73%; a second task (57 criteria) showed no clear gain | not stated | — | 2026-11-06 | same | P |
| Anthropic | Contract-terms wiki | facts surviving | shared page 41/57 (72%); one page per contract 57/57 | not stated | — | 2026-11-06 | same | P |
| Anthropic | "Record only failures" instruction | change in memory gain | Opus 5 −0.234; Opus 4.7 −0.150; Sonnet 4.6 −0.020 | as listed | — | 2026-11-06 | same | P |
| Anthropic | Pokémon Red | memory files / badges | Sonnet 3.7: 413 files, 1 badge; Claude Fable 5: 10 files, 4 badges | as listed | — | 2026-11-06 | same | P |
| Zep Agent Skills (procedural memory) | τ³-bench banking, AppWorld, EnterpriseOps-Gym | pass-rate lift on 3 weaker executors | +4.5 to +18.8 points | not named in abstract | — | 2026-11-01 | https://arxiv.org/abs/2611.01386 | P |
| Hindsight on coding agents | AMB sdebench, 61 tasks, 3 runs | corrections per task, no memory → with | Claude Code 0.85 → 0.36; Codex CLI 1.34 → 0.47; opencode 1.20 → 0.80 | not stated | — | undated (2026) | https://vectorize.io/benchmarks | P |
| Hindsight on coding agents | same | cost per task | Claude Code $0.445 → $0.338; Codex CLI $0.577 → $0.276; opencode $0.634 → $0.553; solve rate unchanged at 60–61/61 | not stated | — | undated | same | P |
| MemOS on OpenClaw | 5 agent tasks | average completion | 36.63% → 50.87% | not stated | — | 2026-07-02 | https://github.com/MemTensor/MemOS | P |

## D. Independent or cross-system comparisons

| Source | System | Benchmark | Value | Reader | Judge | Type | Date | Src |
|---|---|---|---|---|---|---|---|---|
| MemoryTax (arXiv 2610.29823) | Full context | LoCoMo conv-26, 152 q, 1 run | 74 / 92 / 95% | GPT-4o-mini / GPT-6 Luna / Opus 5.5 | GPT-4o-mini | independent | 2026-10-21 | P |
| MemoryTax | BM25 | same | 74 / 82 / 90% | same | same | independent | same | P |
| MemoryTax | Mem0 | same | 78 / 80 / 95% | same | same | independent | same | P |
| MemoryTax | Zep | same | 43 / 51 / 87% | same | same | independent | same | P |
| MemoryTax | Pi agent | same | 63 / 91 / 99% | same | same | independent | same | P |
| MemoryTax | Codex | same | 28 / 88 / 98% | same | same | independent | same | P |
| MemoryTax | Claude Code | same | 29 / 91 / 97% | same | same | independent | same | P |
| MemoryTax | cost per rollout, Opus 5.5 | same | Pi $6.95; full context $17.84; Codex $25.41; Claude Code $28.41 | Opus 5.5 | — | independent | same | P |
| Redis report | Redis Remis + instruct | LongMemEval-S, task-averaged | 86.5% reproduced | gpt-4o (old model) | GPT-4o | competitor | 2026-09-21 | P |
| Redis report | Oracle Agent Memory | same | 93.8% claimed; 86.0% reproduced (78.1% with gpt-4o) | gpt-5.5 xhigh | GPT-4o | competitor | same | P |
| Redis report | Mastra OM | same | 84.2% | gemini + gpt-4o | GPT-4o | competitor | same | P |
| Redis report | Amazon Bedrock AgentCore | same | 73.6% claimed; 77.0% reproduced | gpt-4o | GPT-4o | competitor | same | P |
| Redis report | Google Vertex Memory Bank | same | 42.4% reproduced (~70% in the underlying paper) | gpt-4o | GPT-4o | competitor | same | P |
| Redis report | Mem0 / Supermemory | same | 49.0% / 81.6% (vendor-claimed column, not re-run) | — | — | cited | same | P |
| DolphinBench (Mem0 authors, arXiv 2609.24971) | Hermes built-in / Mem0 / Honcho / Hindsight / Supermemory | 600 tasks | 65.67 / 70.67 / 68.50 / 69.50 / 59.17% | GPT-5.6-Luna | GPT-5.6-Sol | vendor (Mem0) | 2026-09-21 | P |
| DolphinBench | same five | same | 26.50 / 47.83 / 47.33 / 41.00 / 20.00% | MiniMax M3 | GPT-5.6-Sol | vendor | same | P |
| DolphinBench | Claude Code built-in / Mem0 / Honcho | same | 26.33 / 32.33 / 35.83% | Claude Sonnet 5 | GPT-5.6-Sol | vendor | same | P |
| agent-memory-bench (GitHub, hamza-dev-tech) | GoodMem / Letta 0.11.7 / Mem0 2.1.0 / LangMem 0.0.30 / Zep-Graphiti 0.30.2 | 419 turns, 120 probes, recall@10 | 57.6 / 52.2 / 50.0 / 45.7 / 37.0% | gpt-4o-mini (old model) | gpt-4o-mini | independent | 2026-09-23 | P |
| agentmemory retrieval report | BM25 vs grep | LongMemEval-S, strict recall-all@5 | 84.7% vs 72.1% | none (retrieval only) | none | self | 2026-10-28 | P |
| agentmemory | BM25 vs grep | coding-agent-life-v1, 15 queries | 93.3% vs 100% | none | none | self | 2026-10-28 | P |
| RIME (CMU, via Maximem) | Opus 5.5 with memory | Codebase Adaptation cumulative reward | 17.40, +0.90 over no memory; GPT-5.6 Sol gain +4.71 | as listed | unnamed LLM judge | independent, second-hand | 2026-11 | P (secondary) |
| Maximem "claimed vs observed" | Mem0 hosted | LongMemEval | 93.4% claimed; 57.5% then 73.8% observed | gpt-5 (old model) | unnamed | competitor | 2026-07-28 | P |
| techsy.io re-score | Honcho | LoCoMo, same 1,540 q | 89.9% vs Haiku 4.5 alone 83.6% (lead 6.3 points, not the published 14.3) | Claude Haiku 4.5 (old model) | not stated | independent | 2026-10-28 | P |

URLs for this table:
- MemoryTax: https://arxiv.org/abs/2610.29823
- Redis: https://redis.io/resources/agent-memory-benchmark-report/
- DolphinBench: https://arxiv.org/abs/2609.24971
- agent-memory-bench: https://github.com/hamza-dev-tech/agent-memory-bench
- agentmemory: https://github.com/rohitg00/agentmemory/blob/main/docs/benchmarks/2026-10-28-retrieval-evaluation.md
- Honcho re-score: https://techsy.io/de/blog/honcho-memory-review

Two caveats on the Redis table: the page's rows for "Redis instruct", LangMem and Zep rendered garbled (95.4% in every column; "$71.2"), so I left them out. MemoryTax is a single conversation with one run per cell and a lenient judge, by the author's own statement.

## E. Sources with no current-model results (newest found)

| Source | Newest numbers | Model | Date | Src |
|---|---|---|---|---|
| Mem0 headline | LoCoMo 92.5, LongMemEval 94.4, BEAM-1M 64.1, BEAM-10M 48.6 | page names none; Recallium lists it as GPT-5 reader and judge. OSS table: GPT-5 91.0%, GPT-OSS-120B 89.8%, Llama 4 Maverick 88.6%, Gemma 4 31B 88.6% | April 2026 algorithm; page updated 2026-10-10 | P |
| Zep | LoCoMo 94.7% (1459/1540), LongMemEval 90.2% (451/500), median context 5,760 / 4,408 tokens | gpt-5.4 reader and judge (old) | page modified 2026-11-04 | P |
| Letta leaderboard (Context-Bench) | filesystem top 93% | gpt-5.2-codex-xhigh (old) | 2026-03-13 | P |
| Hindsight headline | LongMemEval-S 94.6, LoCoMo 92.0, BEAM-10M 64.1, PersonaMem 86.6, LifeBench 71.5 | not stated on page | BEAM post 2026-04-02; page undated | P |
| Supermemory | LongMemEval-S 85.2% (Gemini 3 Pro), 84.6% (GPT-5), 95% (GPT-4o setup); recall@20 97%. SMFS token use 3× lower on "Claude", 1.75× on "Codex" (versions unnamed) | old | May 2026; post 2026-09-17 | P |
| Cognee | BEAM-100K 0.79, BEAM-10M 0.67; LoCoMo 90.7% / 91.3% (from a card dated 2026-11-11; source post not found) | not stated | page updated 2026-09-03 | P |
| Mastra LongMemEval | 95% (94.87%) | gpt-5-mini (old) | 2026-02-09 | P |
| MemPalace BENCHMARKS.md | LongMemEval R@5 96.6% raw, 98.4% held-out; LoCoMo R@10 88.9% | Haiku / Sonnet 4.6 rerank (old) | 2026-03-26 | P |
| MemOS | LoCoMo 88.83, LongMemEval 89.20, HaluMem 80.91, BEAM-10M 56.75 | not stated | 2026-07-02 | P |
| Honcho | LongMemEval-S 90.4%, LoCoMo 89.9%, BEAM-10M 40.9% | Haiku 4.5 (old) | Dec 2025 | P (secondary) |
| Exabase M-1 | BEAM 76.9 / 75.0 / 68.0%; LongMemEval 96.4% top-50 | Gemini 3 Flash (old) | 2026-07-28; May 2026 | S |
| ByteRover | LoCoMo 96.1%, LongMemEval-S 92.8% | Gemini 3 Flash judge (old) | April 2026 paper | S |
| EverMemOS | LoCoMo 93.05%, LongMemEval 83.00%, HaluMem recall 90.04% | GPT-4.1-mini (old) | paper Jan 2026; HaluMem Aug 2026 | P |
| Oracle Agent Memory | LongMemEval 93.8%, 10.7× fewer tokens | not stated in abstract | 2026-07-14 | P |
| OpenViking | LoCoMo 82.9% vs 33.4% for Hermes built-in; 91% token reduction | not stated | May 2026 | P (secondary) |
| Memobase | LoCoMo 72.4% in MemOS's eval | not stated | undated | S |
| LangMem | only third-party rows (45.7% recall above) | gpt-4o-mini (old) | 2026-09-23 | P |
| Bedrock AgentCore, Vertex Memory Bank | no vendor accuracy numbers found; only the Redis reproductions | gpt-4o (old) | 2026-09-21 | P |
| Anthropic memory tool + context editing | +39% / +29% on agentic search; 84% token reduction over 100 turns | 2025-era models (old) | 2025-09-29 | S |

No measured memory results found at all:
- **OptMem:** no evaluation of any kind, only the "426-token prompt" description.
- **Other memory tools:** claude-mem (an unsourced "~10×" claim only), GBrain, basic-memory, beads.
- **Harness makers:** OpenAI Codex memories (changelog has feature and fix entries only, and I read only its first half), Cursor, Gemini CLI, Warp Agent Memory (design claims only), OpenClaw, OpenCode, Pi, Factory, Devin, Amp. Nous Hermes has no first-party numbers; it appears only as a harness in FrontierMemory and DolphinBench.

Not verified: agentmemorybenchmark.ai returned an empty page, and the HPCwire Exabase release and The New Stack article returned 403. Memobase, GBrain, claude-mem, basic-memory, beads and the harness makers in the last list were checked by search only, not by opening their own pages.
