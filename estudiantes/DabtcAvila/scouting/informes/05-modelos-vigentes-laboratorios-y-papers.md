<!-- Salida original de un subagente de investigación web (Claude Code, 17-nov-2026). Sin editar, salvo quitar rutas locales. [P]/[V] = leído en la página; [S] = solo fragmento de búsqueda. Las páginas se leyeron a través de un resumidor: verificar cada cifra en su fuente antes de citarla. -->

Research complete. All values were read on the primary page or PDF ([P]) unless marked [S] (search snippet or secondary write-up, not verified at source). Nothing is estimated.

**Headline:** no vendor publishes a dedicated memory, memory-tool, file-based-memory or multi-session evaluation for any current flagship. Every memory leaderboard I checked is empty or stale. The only memory-system numbers on current-generation models come from four independent arXiv papers, covering Opus 5.5, Sonnet 5.5, GPT-6 Luna, GPT-6 Sol and GPT-6 Astra.

## 1. Vendor system cards and model cards: long-context, context-management, long-horizon

| Model | Harness | Memory setup | Benchmark | Metric | Value | Reported by | Date | URL | Src |
|---|---|---|---|---|---|---|---|---|---|
| Fable 5.2 | mini-swe-agent, single 1M window, no remaining-context signal | none | ProgramBench (166 tasks) | hidden-test pass rate | 85.6% | self | 2026-11-09 | anthropic.com/document/claude-fable-5-2-mythos-5-2-system-card §8.10 | P |
| Fable 5.2 | same, plus remaining-context counter shown each step | none | ProgramBench | pass rate | 91.6% | self | 2026-11-09 | same | P |
| Fable 5.2 | same as row 1 | none | ProgramBench | tasks that ran out of context before submitting | 68% | self | 2026-11-09 | same | P |
| Opus 5.5 | mini-swe-agent, 1M | none | ProgramBench | pass rate / with counter / ran out of context | 91.2% / 91.1% / 39% | self | 2026-09-22, 2026-11-09 | anthropic.com/claude-opus-5-5-system-card §8.10; Fable 5.2 card | P |
| Fable 5.1 | mini-swe-agent, 1M | none | ProgramBench | pass rate / with counter / ran out of context | 87.6% / 86.8% / 28% | self | 2026-11-09 | Fable 5.2 card | P |
| Opus 5 | mini-swe-agent | none | ProgramBench | pass rate | 85.4% | self | 2026-09-22 | Opus 5.5 card | P |
| Sonnet 5.5 | mini-swe-agent | none | ProgramBench | pass rate | 79.7% | self | 2026-09-28 | anthropic.com/claude-sonnet-5-5-system-card §8.10.1 | P |
| Sonnet 5 | mini-swe-agent | none | ProgramBench | pass rate | 77.3% | self | 2026-09-28 | same | P |
| Haiku 5.5 | mini-swe-agent | none | ProgramBench | pass rate | 82.0% | self | 2026-10-07 | anthropic.com/claude-haiku-5-5-system-card §8.7.1 | P |
| Fable 5.2 | ARC Prize Standard harness / Provider Adapter harness (provider's own context-management features), high effort | provider context management | ARC-AGI-3 | score | 79.26% / 97.72% | independent (ARC Prize), quoted in card | 2026-11-09 | Fable 5.2 card §8.15 | P |
| Fable 5.2 | same, max effort | same | ARC-AGI-3 | score | 65.66% / 94.90% | independent, quoted | 2026-11-09 | same | P |
| GPT-6 Astra | Standard / Provider Adapter, max | same | ARC-AGI-3 | score | 62.7% / 98.6% | independent, quoted | 2026-11-09 | same | P |
| GPT-6.1 Sol | Standard / Provider Adapter, max | same | ARC-AGI-3 | score | 52.7% / 96.2% | independent, quoted | 2026-11-09 | same | P |
| Fable 5.2 | 82-task offline set, 500-step cap | not restated in the Fable 5.2 card | OSWorld 2.1 | partial / strict | 89.3% / 54.6% | self | 2026-11-09 | Fable 5.2 card §8.13.3 | P |
| GPT-6 Astra | same 82 tasks via OpenAI API | OpenAI's own compaction | OSWorld 2.1 | partial | 79.5% | Anthropic-run | 2026-11-09 | same | P |
| Opus 5.5 | keeps every screenshot | Claude API server-side compaction above 100k tokens | OSWorld 2.0 | partial / strict | 81.8% / 48.7% | self | 2026-09-22 | Opus 5.5 card | P |
| Opus 5.5 / Sonnet 5.5 | re-evaluated for the Haiku 5.5 card | card says "same conditions" | OSWorld 2.1 offline | partial / strict | 87.2% / 53.2%; 83.9% / 48.8% | self | 2026-10-07 | Haiku 5.5 card | P |
| Gemini 4 Carbon | not stated | none | GraphWalks 256k–1M, BFS | F1 | 96.2% | self | 2026-11-10 | deepmind.google/models/model-cards/gemini-4-carbon/ | P |
| Gemini 4 Argon | not stated | none | GraphWalks ≤128k / 256k–1M | F1 | 99.7% / 84.2% | self | 2026-10-13 | deepmind.google/models/model-cards/gemini-4-argon/ | P |
| GPT-6 Astra | not stated (Google-run) | none | GraphWalks ≤128k / 256k–1M | F1 | 98.7% / 71.8% | Google | 2026-10-13 | Argon card | P |
| Opus 5.5 | not stated (Google-run) | none | GraphWalks ≤128k / 256k–1M | F1 | 90.6% / 66.8% | Google | 2026-10-13 | Argon card | P |
| Fable 5.1 | not stated (Google-run) | none | GraphWalks ≤128k / 256k–1M | F1 | 91.4% / 65.0% | Google | 2026-10-13 | Argon card | P |
| Mythos 5.2 | internal | not stated | "internal long-horizon task" | qualitative only | "nearly saturates" (earlier models about half to three quarters) | self | 2026-11-09 | Fable 5.2 card | P |

- The Fable 5.2, Opus 5.5, Sonnet 5.5 and Haiku 5.5 cards contain no memory-tool, file-memory, multi-session or Vending-Bench evaluation; I grepped the full text of each.
- Both the Fable 5.2 and Opus 5.5 cards state that context compaction was not used for HLE.
- Compaction appears only as a setup detail: the multi-agent single-agent baseline uses compaction with a 20M-token budget.
- The OpenAI GPT-6.2 launch post returned 403. Secondary coverage (the-decoder, eesel) shows no memory, compaction, GraphWalks or MRCR numbers [S].
- The GPT-6 Astra system card had none in the 200k of 217k characters I read.

## 2. Long-horizon coherence: Vending-Bench 2 (mean final bank balance, harness is Andon's)

| Model | Value | Runs | Src |
|---|---|---|---|
| Gemini 4 Carbon | $16,484.21 ± 1,096 | 6 | P (andonlabs.com/evals/vending-bench-2) |
| GPT-6 Astra | $15,514.70 ± 1,074 | 6 [S] | P |
| Gemini 4 Hydrogen | $14,549.49 ± 495 | 6 | P |
| GPT-6 Sol | $14,427.85 ± 1,051 | not shown | P |
| Gemini 4 Argon | $13,718.16 ± 3,100 | 6 | P |
| GPT-6.1 Sol | $12,860.61 ± 1,043 | 6 | P |
| Opus 5 | $11,181.87 ± 2,094 | not shown | P |
| Sonnet 5.5 | $11,165.28 ± 1,585 | 6 | P |
| Fable 5.2 | $9,628.48 ± 726 (rank 12 of 76) | 6 | S (benchlm.ai mirror, updated 2026-11-17) |
| Opus 5.5 | $9,235.25 ± 785 | 6 | S (benchlm); $9,235 also on the Carbon card, P |
| GPT-6.1 Terra | $9,107.46 ± 768 | 6 | S (benchlm); $9,107 on the Hydrogen card, P |
| Fable 5.1 | $5,421.56 ± 1,244 | 6 | S (benchlm); $5,422 on the Carbon card, P |
| Haiku 5.5 | $3,602.46 ± 691 | 6 | S (benchlm) |
| GPT-6.2 Astra / Sol, GPT-6 Luna | not found | | |

Andon's page shows only the top 10 without expanding; ranks 11–76 come from the benchlm mirror. Reported by Andon Labs (independent); no dates per entry.

## 3. Independent papers with memory or compaction numbers on current models

| Model | Harness | Memory setup | Benchmark | Metric | Value | Date | URL | Src |
|---|---|---|---|---|---|---|---|---|
| Opus 5.5 (effort high) | none (prompt) | full context | LoCoMo conv-26, 152 questions | correct % / $ per question | 95 / 0.117 | 2026-10-21 | arxiv.org/abs/2610.29823 (MemoryTax) | P |
| Opus 5.5 | none | BM25 top-8 | same | same | 90 / 0.013 | | | P |
| Opus 5.5 | none | Mem0 OSS 2.1.0 | same | correct % / $ per question / build $ | 95 / 0.074 / 25.876 | | | P |
| Opus 5.5 | none | Zep (Graphiti 0.30.2) | same | same | 87 / 0.0077 / 6.224 | | | P |
| Opus 5.5 | Pi 1.1.0 | history as one JSON file, default tools | same | correct % / $ per question | 99 / 0.046 | | | P |
| Opus 5.5 | Codex 0.159.2 | same file | same | same | 98 / 0.167 | | | P |
| Opus 5.5 | Claude Code 2.1.295 | same file | same | same | 97 / 0.187 | | | P |
| GPT-6 Luna (high) | none | full / BM25 / Mem0 / Zep | same | correct % | 92 / 82 / 80 / 51 | | | P |
| GPT-6 Luna | Pi / Codex / Claude Code | file | same | correct % | 91 / 88 / 91 | | | P |
| Opus 5.5 reading a GPT-6 Luna-written store | none | Mem0 / Zep | same | correct % | 81 / 55 | | MemoryTax Table 3 | P |
| GPT-6 Luna reading an Opus 5.5-written store | none | Mem0 / Zep | same | correct % | 91 / 71 | | same | P |
| Opus 5.5 | mini-swe-agent, 200-step cap | no memory | ChainSWE test (48 chains) | resolve % / steps / resolves per USD | 38.5 / 12.6 / 162 | 2026-11-12 | arxiv.org/abs/2611.17316 (CoReMem) Table 3 | P |
| Opus 5.5 | same | full history | same | same | 40.6 / 10.4 / 170 | | | P |
| Opus 5.5 | same | Mem0 | same | same | 39.6 / 13.0 / 137 | | | P |
| Opus 5.5 | same | MemOp | same | same | 39.6 / 17.8 / 109 | | | P |
| Opus 5.5 | same | ReasoningBank | same | same | 40.6 / 14.2 / 101 | | | P |
| Opus 5.5 | same | CoReMem without training (self-written notes) | same | same | 38.5 / 11.8 / 188 | | | P |
| GPT-5.6 Luna | same | none / full / Mem0 / MemOp / ReasoningBank / CoReMem without training | same | resolve % | 23.6 / 24.0 / 22.6 / 22.9 / 23.3 / 25.7 | | | P |
| Opus 5.5 | data agent (authors') | baseline → with compaction | 5 data-agent benchmarks, 1,514 tasks | mean accuracy % | 68.8 → 65.2 | 2026-10-22 | arxiv.org/abs/2610.20959 Table 2 | P |
| GPT-6 Astra | same | baseline → with compaction | same | same | 69.6 → 65.1 | | | P |
| Sonnet 5.5 | same | baseline → with compaction | same | same | 61.3 → 57.7 | | | P |
| Opus 5.5 / GPT-6 Astra / Sonnet 5.5 | same | orchestration → orchestration with compaction | same | same | 61.9→64.0 / 61.0→56.4 / 60.0→58.4 | | | P |
| GPT-6 Sol | none (chat) | no memory / full history / NaiveRAG / MemoryBank / A-Mem / mem0 / MemoryOS | MemBubble (1,000 histories) | Adapted Distinct-k | 3.67 / 3.54 / 2.67 / 2.41 / 2.28 / 2.16 / 2.81 | 2026-10-18 | arxiv.org/abs/2610.25127 | P |
| GPT-5.6 Luna | same | same order | same | same | 3.56 / 3.50 / 2.72 / 2.43 / 2.23 / 2.21 / 2.71 | | | P |
| Sonnet 5.5 | Claude Code 2.1.308 | malicious project memory file | 36 SecRepoBench tasks | names the file in its final message | "about two thirds" | 2026-10-28 | arxiv.org/abs/2610.38521 | P |
| Sonnet 5.5, Qwen 3.8 27B, DeepSeek V4.1 Flash | Claude Code / OpenCode 2.1.1 | same | same | change in secure-completion rate | −8 to +6 pp across agents (no per-model split in abstract) | | | P |
| Sonnet 5 | Claude Code | built-in memory / Mem0 / Honcho | DolphinBench (600 tasks) | accuracy % | 26.33 / 32.33 / 35.83 | Sept 2026 | arxiv.org/abs/2609.24971 (Mem0 authors, self-interested) | P |
| GPT-5.6 Luna | Hermes | built-in / Mem0 / Honcho / Hindsight / Supermemory | DolphinBench | accuracy % | 65.67 / 70.67 / 68.50 / 69.50 / 59.17 | | | P |
| Qwen3.8-27B | PrisMem (task, reflection, judge) | PrisMem / Mem0 / A-MEM / HippoRAG2 | BEAM-1M | overall score % | 63.39 / 48.95 / 51.56 / 51.86 | 2026-10 | arxiv.org/abs/2610.06361 | P |
| Qwen3.8-27B | none | Mem0 / A-MEM / SimpleMem | LongMemEval-M | overall score % | 62.50 / 67.33 / 66.50 | | | P |
| DeepSeek V4.1 Flash (thinking) | Mnemon | raw records plus consolidated index | LoCoMo (revised labels) / LongMemEval-S | accuracy | 95.3 / 94.4 | 2026-09 | arxiv.org/abs/2609.36059 (self-reported by system authors) | P |
| Kimi-K3 / Qwen3.8-27B / GPT-5.6-Sol | DyadMem pipeline | model-built memory | DyadMem | Full-Pipeline QA % | 74.85 / 53.81 / 70.35 | 2026-10 | arxiv.org/abs/2610.03020 | P |

**Re-opened as requested:**
- **MemoryTax:** only three models (GPT-4o-mini, GPT-6 Luna, Opus 5.5). There are no extra model rows beyond what you have; the full grid is above. It is one conversation with one run per cell.
- **Doc2Harness (2610.20344):** 19 models, harness-building rather than memory. Pass rate over 328 tests, with the "Session" (session-state) sub-score in brackets:

| Model | All (%) | Session (%) |
|---|---|---|
| GPT-6 Astra | 53.05 ± 0.25 | 44.0 |
| Opus 5 | 46.65 ± 1.80 | 38.1 |
| Qwen3.8 Max | 45.83 ± 0.14 | 43.3 |
| GPT-5.6-sol | 43.80 ± 2.44 | 29.4 |
| GLM 5.3 | 42.07 ± 1.39 | 33.3 |
| DeepSeek V4.1 Flash | 40.24 ± 0.86 | 34.5 |
| Kimi K3 | 38.31 ± 1.28 | 25.4 |
| DeepSeek V4 Pro | 31.91 ± 1.23 | 21.0 |
| GLM 5.2 | 27.64 ± 1.01 | 21.8 |

No Opus 5.5, Fable, GPT-6.1/6.2 or Gemini 4 in that paper.

**New papers found with current or predecessor models but no usable memory row:**
- **2611.22017 SkillBuffBench (2026-11-17):** memory on/off crossed with 4 harnesses and 11 models, including Fable 5.2, Opus 5.5, Gemini 4 Argon, GPT-6 Astra, GPT-6.1 Sol, Kimi K3.1 Pro, GLM-5.3, Qwen3.8. It is design-only: "results will be added once the runs are complete."
- **2611.03223 (rule compliance under compaction):** GPT-6 Luna-Pro, GPT-6.1 Sol and Sonnet 5.5 are judges only. The model-membership table lists DeepSeek-V4-Flash and GLM-5.3-Flash among the studied models; no numbers extracted.
- **2610.27435 RiseHarness:** GPT-6-sol, harness evolution rather than memory. Terminus-2 → RiseHarness Pass@1 is 50.25 → 55.50 on TBH and 78.65 → 81.74 on TB2.1.
- **2610.29869 Compaction Laundering:** GPT-5.6 Luna/Sol/Terra laundering 2/3, 3/3, 3/3 in the pi harness; claude-opus-5 "refused to summarize".
- **Predecessor models only, not extracted:** 2611.04867 (Sonnet 5, GPT-5.6), 2610.14431 MemForm (Sonnet 5, GPT-5.6 Luna, Qwen3.8-Flash), 2610.18052 (GPT-5.6 Luna, DeepSeek V4.1), 2611.17808 CarryOn (Sonnet 5, Qwen3.8-27B), 2610.30499 (Opus 5, Fable 5, GPT-6 Astra on ARC-AGI-3 harness), 2610.04433 (Opus 5, Qwen3.8, GLM-5.3), 2611.09721 MemoryDojo (GPT-5.6 Luna, GLM-5.3), 2610.21405 MemCut (DeepSeek V4.1 Flash, Qwen3.8-Flash, GLM-5.3-Flash).
- **Current models only as judges or incidental mentions:** 2611.14320 (Opus 5.5), 2611.02361 (Opus 5.5), 2611.05731, 2611.14009.

## 4. Memory leaderboards read today

| Leaderboard | State today | Current-model entries |
|---|---|---|
| LongMemEval-V2 (xiaowu0162.github.io/longmemeval-v2) | "Leaderboard entries coming soon" on both Small and Medium | none [P] |
| Letta leaderboard (leaderboard.letta.com) | last updated 2026-03-13; top is gpt-5.2-codex-xhigh at 93% | none; newest are Opus 4.6 and GPT-5.4 [P] |
| Letta "Evaluating memory in production agents" (Context-Bench V2, 2026-07-28) | qualitative only, no numbers | Fable 5, Opus 5, Sonnet 5, GPT-5.6 Sol/Luna, Kimi-K3, GLM-5.2 ranked in prose [P] |
| MemoryArena (memoryarena.github.io) | no leaderboard rows on the page | none [P] |
| AMA-Bench (ama-bench.github.io) | fetch returned title only (likely JS-rendered) | not readable |
| METR time horizons (metr.org/time-horizons) | last updated 2026-09-08, "no longer actively updated"; newest entry is Claude Mythos Preview (early) | none for Fable 5.x, Opus 5.x, GPT-6.x, Gemini 4 [P]; secondary sources give Mythos Preview at about 17.4 h (50%) [S] |
| Chroma context rot | no 2026 update with these models found | none |
| BEAM, MemoryAgentBench, LOCA-bench, LongCodeBench | no leaderboard with current models found by search | not found |

## 5. Agentic coding, context only

| Model | Harness | Benchmark | Value | Reported by | Src |
|---|---|---|---|---|---|
| Fable 5.2 | not stated in §8.2 | SWE-bench Pro / Multilingual / Multimodal | 93.0 / 96.6 / 74.1 | self | P |
| Opus 5.5 | not stated | same | 89.9 / 93.9 / 61.4 | self | P |
| Sonnet 5.5 | not stated | same | 81.3 / 90.3 / 54.3 | self | P |
| Haiku 5.5 | not stated | same | 64.8 / 83.7 / 30.7 | self | P |
| Fable 5.1 / Opus 5 | not stated | SWE-bench Pro | 81.2 / 79.2 | self | P |
| Fable 5.2 | Claude Code `--bare`, max, no internet | Terminal-Bench 4.0 | 67.6% ± 1.8 (Mythos 5.2 70.5%) | self | P |
| Opus 5.5 | Claude Code `--bare`, xhigh | Terminal-Bench 4.0 | 66.4% ± 2.6 (max: 64.8%) | self | P |
| Sonnet 5.5 / Haiku 5.5 | not captured | Terminal-Bench 4.0 | 70.6% / 39.2% | self | P |
| GPT-6 Astra | high effort | Terminal-Bench 4.0 | 57.9% | OpenAI, quoted by Anthropic | P |
| Gemini 4 Carbon / Argon | not stated, labelled "(AA)" | Terminal-Bench 4.0 | 65.2% / 57.1% | Google | P |
| GPT-6.2 Astra | not stated | Terminal-Bench 4.0 | 63.13% ± 1.34 (rank 5/68) | Vals AI | P |

Public tbench.ai Terminal-Bench 4.0 leaderboard, read today [P]:

| Agent | Model (effort) | Resolution rate |
|---|---|---|
| GitHub Copilot | Copilot Fusion (max) | 71.2% |
| Claude Code | Opus 5.5 (max) | 65.8% |
| Claude Code | Fable 5.2 (max) | 65.8% |
| Antigravity CLI | Gemini 4 Carbon (high) | 64.5% |
| Claude Code | Sonnet 5.5 (max) | 63.9% |
| Codex | GPT-6.2 Astra (max) | 62.1% |
| Codex | GPT-6.2 Sol (max) | 61.5% |
| Codex | GPT-6.1 Sol (max) | 60.9% |
| Codex | GPT-6 Astra (max) | 60.3% |
| Claude Code | Kimi K3.1 Pro (max) | 59.7% |
| Claude Code | Fable 5.1 (xhigh) | 57.6% |
| Antigravity CLI | Gemini 4 Hydrogen (high) | 56.4% |
| Antigravity CLI | Gemini 4 Argon (high) | 55.5% |
| Claude Code | Opus 5 (xhigh) | 53.3% |
| Codex | GPT-6.1 Terra (max) | 53.3% |
| Codex | GPT-6 Sol (max) | 50.3% |
| Claude Code | GLM-5.3 (max) | 41.2% |
| Claude Code | Haiku 5.5 (max) | 40.0% |
| Claude Code | DeepSeek V4.1 Flash (max) | 38.5% |
| Claude Code | Qwen3.8-Max-0902 (max) | 27.0% |

SWE-bench Verified is not reported in any current card I read; they report SWE-bench Pro instead.

## 6. Current models with no published memory numbers

"Memory numbers" here means an evaluation with a memory system, memory files, cross-session state, or compaction as a variable.

| Model | Memory-system eval | Long-context / long-horizon numbers that do exist |
|---|---|---|
| Claude Fable 5.2 | not found (SkillBuffBench pending) | ProgramBench, ARC-AGI-3 Provider Adapter, Vending-Bench 2 [S] |
| Claude Mythos 5.2 | not found | qualitative long-horizon claim only |
| Claude Opus 5.5 | found: MemoryTax, CoReMem, 2610.20959 | ProgramBench, GraphWalks (Google-run), Vending-Bench 2 |
| Claude Sonnet 5.5 | found: 2610.20959 (compaction), 2610.38521 (memory-file security) | ProgramBench, Vending-Bench 2 |
| Claude Haiku 5.5 | not found (MemHarmBench, which you already have, uses it) | ProgramBench, Vending-Bench 2 [S] |
| Claude Fable 5.1 | not found | ProgramBench, GraphWalks (Google-run), Vending-Bench 2 |
| Claude Opus 5 / Sonnet 5 / Fable 5 | Sonnet 5: DolphinBench; Opus 5 and Fable 5: Letta prose only | ProgramBench (Opus 5, Sonnet 5), Vending-Bench 2 (Opus 5) |
| GPT-6.2 Astra | not found (released today) | none |
| GPT-6.2 Sol | not found (released today) | none |
| GPT-6.1 Terra | not found | Vending-Bench 2 only |
| GPT-6.1 Sol | not found | ARC-AGI-3 Provider Adapter, Vending-Bench 2 |
| GPT-6 Luna | found: MemoryTax | none |
| GPT-6 Sol | found: MemBubble (response diversity, not accuracy) | Vending-Bench 2 |
| GPT-6 Astra | found: 2610.20959 (compaction) | GraphWalks (Google-run), ARC-AGI-3, Vending-Bench 2 |
| GPT-5.6 Sol / Luna | found: CoReMem (Luna), DolphinBench (Luna), DyadMem (Sol), MemBubble (Luna) | none read |
| Gemini 4 Carbon | not found | GraphWalks, Vending-Bench 2 |
| Gemini 4 Argon | not found (SkillBuffBench pending) | GraphWalks, Vending-Bench 2 |
| Gemini 4 Hydrogen | not found | Vending-Bench 2 |
| Gemini 3.7 Flash | MemBubble only (diversity metric); 3.5 not found | none |
| Qwen 3.8 | found: 27B on BEAM-1M / LongMemEval-M and DyadMem; Max: Doc2Harness only | none |
| DeepSeek V4.1 | found: Flash in Mnemon (self-reported) | none |
| GLM-5.3 | Flash in MemBubble only (diversity metric); otherwise Doc2Harness only | none |
| Kimi K2.7 / K3.1 | not found (Kimi K3 in DyadMem; K3.1 Pro pending in SkillBuffBench) | none |
| Llama (current) | not found (only Llama 3.3-70B in MemBubble) | none |

## 7. Model lineup verified today

| Vendor | Model | API ID | Release | Source | Src |
|---|---|---|---|---|---|
| Anthropic | Claude Fable 5.2 | `claude-fable-5-2` | 2026-11-09 | platform.claude.com model page and release notes | P |
| Anthropic | Claude Mythos 5.2 (limited access) | `claude-mythos-5-2` | 2026-11-09 | release notes | P |
| Anthropic | Claude Opus 5.5 | `claude-opus-5-5` | 2026-09-22 | model page | P |
| Anthropic | Claude Sonnet 5.5 | `claude-sonnet-5-5` | 2026-09-28 | release notes | P |
| Anthropic | Claude Haiku 5.5 | `claude-haiku-5-5` | 2026-10-07 | release notes | P |
| Anthropic | Fable 5.1 / Mythos 5.1 | `claude-fable-5-1` | 2026-09-01 | release notes | P |
| Anthropic | Opus 5 | `claude-opus-5` | 2026-07-24 | release notes | P |
| Anthropic | Sonnet 5 | `claude-sonnet-5` | 2026-06-30 | release notes | P |
| Anthropic | Fable 5 / Mythos 5 | `claude-fable-5` | 2026-06-09 | release notes | P |
| OpenAI | GPT-6.2 Astra | `gpt-6.2-astra` | 2026-11-17 (today) | developers.openai.com changelog | P |
| OpenAI | GPT-6.2 Sol | `gpt-6.2-sol` | 2026-11-17 (today) | changelog | P |
| OpenAI | GPT-6.1 Terra | `gpt-6.1-terra` | 2026-10-26 | changelog | P |
| OpenAI | GPT-6.1 Sol | `gpt-6.1-sol` | 2026-09-29 | changelog | P |
| OpenAI | GPT-6 Sol / GPT-6 Luna | `gpt-6-sol`, `gpt-6-luna` | 2026-09-22 | changelog | P |
| OpenAI | GPT-6 Astra | `gpt-6-astra` | 2026-09-03 | changelog | P |
| OpenAI | GPT-5.6 Sol / Terra / Luna | `gpt-5.6-sol` etc. | 2026-07-09 | changelog | P |
| Google | Gemini 4 Carbon | `gemini-4-carbon` | 2026-11-10 | aistudio.google.com/docs/changelog and model card | P |
| Google | Gemini 4 Argon | `gemini-4-argon` | 2026-10-13 | changelog and model card | P |
| Google | Gemini 4 Hydrogen | `gemini-4-hydrogen` | 2026-11-12 | changelog and model card | P |
| Google | Gemini 3.8 Flash | `gemini-3.8-flash` | 2026-09-02 | changelog | P |
| Google | Gemini 3.7 Flash | `gemini-3.7-flash` | 2026-08-13; deprecated 2026-10-08 | changelog | P |

- **OpenAI flagship list:** the models page lists GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra and GPT-6 Luna as flagships, all with a 1.05M context window. There is no "GPT-6 Terra" entry in the changelog.
- **Open models:** I did not verify release dates on vendor pages. Dates visible on the Terminal-Bench leaderboard are GLM-5.3 (2026-08-14), Qwen3.8-Max-0902 (2026-09-02), DeepSeek V4.1 Flash 1017 (2026-10-17) and Kimi K3.1 Pro (2026-10-24). Kimi K2.7 and current Llama: not found.

**Gaps I could not close:** the OpenAI GPT-6.2 launch post (403), the last 17k characters of the GPT-6 Astra system card, AMA-Bench's page content, and Andon's hidden ranks 11–76 at source.
