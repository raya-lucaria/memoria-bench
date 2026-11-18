<!-- Salida original de un subagente de investigación web (Claude Code, 17-nov-2026). Sin editar, salvo quitar rutas locales. [P]/[V] = leído en la página; [S] = solo fragmento de búsqueda. Las páginas se leyeron a través de un resumidor: verificar cada cifra en su fuente antes de citarla. -->

All values below were read on the fetched page [P] unless marked [S]. Pages were extracted through WebFetch's summariser, so spot-check any number you plan to quote. Reporter is "independent" (academic, no product in the table) unless marked self.

## 1. arXiv 2606.24775 — "Are We Ready For An Agent-Native Memory System?" (June 2026)

The main end-to-end results (RQ1, RQ2, RQ4, RQ5) are figures, not tables, so only values quoted in the text are available. The default backbone is not stated in the extracted text; the LongMemEval judge is GPT-5.4-based. Source: https://arxiv.org/html/2606.24775 [P].

Systems in results: Mem0, MemoChat, Cognee, Zep, MemTree, Letta, LightMem, SimpleMem, MemOS, MemoryOS, A-MEM, plus Long Context and Embedding RAG baselines. MEM1, MemAgent and Mem0g appear only in the taxonomy.

**Table 2 (update robustness; the only full per-system table)**

| System | LoCoMo-Temporal EM | LoCoMo Ans F1 | LME Knowledge-Update SubEM | LME-KU ROUGE-L | LME Temporal SubEM | LME-TR ROUGE-L |
|---|---|---|---|---|---|---|
| Long Context | 8.1 | 26.9 | 20.0 | 18.0 | 12.0 | 24.0 |
| Embedding RAG | 1.6 | 7.9 | 20.0 | 17.8 | 10.7 | 22.7 |
| Mem0 | 3.2 | 6.0 | 15.6 | 17.1 | 10.7 | 22.4 |
| MemoChat | 2.4 | 15.4 | 8.9 | 12.9 | 10.7 | 25.3 |
| Cognee | 4.0 | 28.1 | 37.8 | 34.0 | 18.7 | 35.8 |
| Zep | 4.8 | 18.1 | 44.4 | 36.8 | 13.3 | 30.5 |
| MemTree | 5.6 | 18.6 | 31.1 | 30.6 | 8.0 | 29.9 |
| Letta (MemGPT) | 0.0 | 7.1 | 17.8 | 5.7 | 12.0 | 8.8 |
| LightMem | 4.0 | 20.1 | 15.6 | 20.2 | 12.0 | 28.6 |
| SimpleMem | 4.4 | 8.1 | 6.7 | 7.4 | 8.0 | 22.6 |
| MemOS | 8.9 | 28.0 | 28.9 | 30.5 | 12.0 | 31.1 |
| MemoryOS | 3.2 | 22.7 | 35.6 | 32.2 | 16.0 | 31.6 |
| A-MEM | 4.8 | 17.7 | 26.7 | 22.8 | 8.0 | 22.5 |

**Text-quoted values (from figures)**

| System | Dataset | Metric | Value |
|---|---|---|---|
| Zep | LongMemEval | LLM-judge accuracy | 48.0 |
| Cognee | LongMemEval | ROUGE-L F1 | 35.3 |
| MemOS | LoCoMo | Exact Match | 11.5 |
| Long Context | DB-Bench | Exact Match | 48.20 |
| MemoChat | DB-Bench | Task success rate | 55.40 |
| SimpleMem | LoCoMo | Recall@1 | 39.0 |
| A-MEM | LoCoMo | Recall@5 / @10 | 69.5 / 85.9 |
| MemTree | LoCoMo | Recall@5 / @10 | 59.7 / 80.5 |
| Embedding RAG | LoCoMo | Ans F1, short to wide evidence gap | 37.1 to 7.4 |
| Long Context | LongBench | Accuracy, Short to Medium (one extraction said "Long") | 42.6 to 19.0 |
| SimpleMem | LongBench | Accuracy, Short to Medium | 35.2 to 34.9 |
| MemOS | LoCoMo | Ans F1 across 4 backbones | 32.2 / 41.2 / 38.6 / 41.2 |

**Cost and latency (Figure 11, text-quoted; no token table exists)**

| System | Avg operation latency per query (s) | Normalized utility | LongBench total latency per query (s) |
|---|---|---|---|
| LightMem | 3.67 | 48.3 | 17.3 |
| MemoChat | 15.4 | 28.0 | 460.2 |
| MemTree | 15.9 | 63.5 | 116.7 |
| A-MEM | 17.9 | 57.7 | 552.1 |
| MemoryOS | 28.6 | 82.0 | 490.0 |
| Mem0 | 35.9 | 21.4 | 374.2 |
| Cognee | 116.5 | above 84 | not found |
| Zep | 155.1 | above 84 | not found |

## 2. arXiv 2609.23570 — VibeMemBench (Sept 2026)

- **Solvers:** deepseek-v4-pro, glm-5, glm-5.2, kimi-k2.7-code, qwen3.8-max.
- **Memory systems:** Mem0, SimpleMem, MemoryOS, A-MEM.
- **Scale:** 111 targets × 4 seeds = 444 runs per cell.
- **Harness:** not found. No dollar cost is reported, only tokens and steps.
- **Source:** https://arxiv.org/html/2609.23570 [P].

| Solver | Condition | Resolved | Input tokens | Output tokens | Steps |
|---|---|---|---|---|---|
| deepseek-v4-pro | Memory off | 67.1% | 1.67M | 19.1k | 50.3 |
| deepseek-v4-pro | Frozen verified experience | 67.1% | 1.49M | 18.9k | 47.6 |
| glm-5 | Memory off | 55.0% | 2.45M | 15.4k | 77.1 |
| glm-5 | Frozen verified experience | 57.4% | 1.93M | 13.2k | 66.2 |
| glm-5.2 | Memory off | 76.8% | 4.06M | 45.9k | 68.2 |
| glm-5.2 | Frozen verified experience | 80.4% | 3.40M | 39.3k | 61.0 |
| kimi-k2.7-code | Memory off | 69.8% | 1.56M | 16.2k | 56.0 |
| kimi-k2.7-code | Frozen verified experience | 74.3% | 1.57M | 16.4k | 53.8 |
| qwen3.8-max | Memory off | 79.1% | 4.03M | 55.2k | 52.9 |
| qwen3.8-max | Frozen verified experience | 80.2% | 4.00M | 60.3k | 50.6 |

The memory-system condition was run on three solvers only.

| Solver | Mem0 (resolved / Δpp / steps) | SimpleMem | MemoryOS | A-MEM |
|---|---|---|---|---|
| deepseek-v4-pro | 62.8% / −4.3 / 51.2 | 66.9% / −0.2 / 48.7 | 64.6% / −2.5 / 50.9 | 63.1% / −4.0 / 50.0 |
| glm-5 | 49.5% / −5.5 / 71.7 | 53.2% / −1.8 / 70.2 | 57.0% / +2.0 / 67.2 | 52.5% / −2.5 / 66.5 |
| kimi-k2.7-code | 68.0% / −1.8 / 57.0 | 69.6% / −0.2 / 56.1 | 66.0% / −3.8 / 53.9 | 65.8% / −4.0 / 55.0 |

**Retrieval-budget curve (deepseek-v4-pro + Mem0), resolved by k:**

| k | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Resolved | 67.1% | 62.8% | 61.7% | 64.4% | 65.5% | 63.7% |

**Failure attribution (231 failing pairings):** coverage 37, rank 3, form 160, use 31. Stripping instruction pollution raised mean resolved seeds from 1.37 to 1.97 (random-strip control 1.85).

## 3. arXiv 2602.16313 — MemoryArena (Feb 2026, v2)

Task agent is GPT-5.1-mini per the Table 3 caption (the text says GPT-5-mini). SR = success rate, PS = progress score, sPS = soft progress score. Source: https://arxiv.org/html/2602.16313 [P].

| Method | Type | Shop SR/PS | Travel SR/PS/sPS | Search SR/PS | Math SR/PS | Phys SR/PS | Avg SR | Task latency avg (s) |
|---|---|---|---|---|---|---|---|---|
| GPT-5.1-mini | Long context | 0.01/0.58 | 0.00/0.00/0.52 | 0.06/0.05 | 0.21/0.30 | 0.50/0.59 | 0.16 | 557.8 |
| GPT-4.1-mini | Long context | 0.00/0.43 | 0.00/0.00/0.19 | 0.02/0.03 | 0.13/0.27 | 0.30/0.45 | 0.09 | 216.8 |
| Gemini-3-Flash | Long context | 0.12/0.76 | 0.00/0.01/0.62 | 0.07/0.04 | 0.17/0.30 | 0.60/0.61 | 0.19 | 276.2 |
| Claude-Sonnet-4.5 | Long context | 0.12/0.79 | 0.00/0.06/0.44 | 0.02/0.03 | 0.20/0.25 | 0.45/0.59 | 0.16 | 385.6 |
| Letta | Memory agent | 0.00/0.50 | 0.00/0.00/0.35 | 0.16/0.09 | 0.11/0.26 | 0.45/0.65 | 0.14 | 698.4 |
| Mem0 | Memory agent | 0.00/0.45 | 0.00/0.00/0.24 | 0.24/0.09 | 0.18/0.28 | 0.25/0.43 | 0.13 | 706.4 |
| Mirix | Memory agent | 0.00/0.41 | 0.00/0.00/0.36 | 0.10/0.06 | 0.18/0.28 | 0.35/0.50 | 0.13 | 622.6 |
| Mem0-g | Memory agent | 0.00/0.43 | 0.00/0.00/0.24 | 0.15/0.08 | 0.19/0.32 | 0.25/0.50 | 0.12 | 792.0 |
| ReasoningBank | Memory agent | 0.00/0.27 | 0.00/0.00/0.00 | 0.10/0.06 | 0.13/0.27 | 0.35/0.53 | 0.12 | 771.6 |
| BM25 | RAG | 0.00/0.56 | 0.00/0.01/0.45 | 0.28/0.09 | 0.18/0.29 | 0.40/0.58 | 0.17 | 706.8 |
| text-embedding-3-small | RAG | 0.00/0.55 | 0.00/0.01/0.50 | 0.23/0.09 | 0.25/0.33 | 0.50/0.68 | 0.20 | 506.4 |
| MemoRAG | RAG | 0.00/0.54 | 0.00/0.03/0.50 | 0.22/0.21 | 0.24/0.30 | 0.40/0.55 | 0.17 | 622.4 |
| GraphRAG | RAG | 0.00/0.52 | 0.00/0.01/0.51 | 0.04/0.05 | 0.23/0.31 | 0.60/0.63 | 0.17 | 573.8 |

No cost table was found.

## 4. arXiv 2602.22769 — AMA-Bench (Feb 2026, v4)

Real-world subset, accuracy with F1 in parentheses; judge is Qwen3-32B (92.67% agreement with humans). AMA-Agent is the authors' own method (self). A per-capability synthetic-subset table was not found. Source: https://arxiv.org/html/2602.22769 [P].

**Long-context models**

| Model | Recall | Causal | State update | State abstraction | Avg |
|---|---|---|---|---|---|
| GPT 5.2 | 0.7741 | 0.8047 | 0.6563 | 0.6037 | 0.7226 (0.3988) |
| GPT-5-mini | 0.6951 | 0.7157 | 0.6575 | 0.6235 | 0.6784 (0.3464) |
| Qwen3-32B | 0.6149 | 0.5178 | 0.4903 | 0.3657 | 0.5181 (0.3545) |
| Gemini 2.5 Flash | 0.5834 | 0.5087 | 0.5000 | 0.4196 | 0.5168 (0.2878) |
| Qwen3-14B | 0.5675 | 0.4430 | 0.4502 | 0.3176 | 0.4659 (0.3203) |
| Qwen2.5-14B-1M | 0.5570 | 0.4111 | 0.4728 | 0.3368 | 0.4638 (0.3622) |
| Claude Haiku 3.5 | 0.4943 | 0.4507 | 0.4287 | 0.3090 | 0.4361 (0.3067) |
| Qwen3-8B | 0.5024 | 0.3776 | 0.3987 | 0.2923 | 0.4109 (0.3240) |

**RAG and memory systems (Qwen3-32B backbone)**

| Method | Recall | Causal | State update | State abstraction | Avg | End-to-end latency per trajectory (s) |
|---|---|---|---|---|---|---|
| AMA-Agent (self) | 0.6238 | 0.6145 | 0.5305 | 0.4719 | 0.5722 | 8.50 |
| EMem | 0.4631 | 0.4925 | 0.4512 | 0.3421 | 0.4610 | not found |
| MemoRAG | 0.4708 | 0.5497 | 0.4257 | 0.3659 | 0.4606 | not found |
| HippoRAG2 | 0.4579 | 0.5080 | 0.4403 | 0.3538 | 0.4480 | 12.10 |
| Qwen3-Emb-4B | 0.4843 | 0.4974 | 0.3520 | 0.3011 | 0.4227 | not found |
| BM25 | 0.3301 | 0.4264 | 0.3450 | 0.2498 | 0.3436 | not found |
| MemoryBank | 0.3231 | 0.4100 | 0.3006 | 0.3332 | 0.3397 | not found |
| MemGPT | 0.3289 | 0.4404 | 0.2809 | 0.2526 | 0.3304 | not found |
| GraphRAG | 0.3077 | 0.3905 | 0.3140 | 0.2879 | 0.3258 | not found |
| A-mem | 0.3084 | 0.3653 | 0.3088 | 0.2873 | 0.3186 | not found |
| Mem-alpha | 0.2876 | 0.4172 | 0.3064 | 0.2171 | 0.3117 | not found |
| HiMem | 0.2945 | 0.4018 | 0.3126 | 0.2238 | 0.2995 | not found |
| MemAgent | 0.2550 | 0.3380 | 0.2849 | 0.2202 | 0.2768 | 5.54 |
| Mem0 | 0.2011 | 0.2645 | 0.2101 | 0.1516 | 0.2104 | 2.85 |
| SimpleMem | 0.2012 | 0.1884 | 0.1764 | 0.1373 | 0.1811 | 24.35 |
| Mem1 | 0.1180 | 0.1427 | 0.1205 | 0.1080 | 0.1229 | 22.03 |

**Other backbones and end-to-end task success**

| Method | Avg acc, Qwen3-8B | Avg acc, GPT-5-mini (synthetic) | TextWorld E2E % | ScienceWorld E2E % | LoCoMo acc (Qwen3-32B) |
|---|---|---|---|---|---|
| AMA-Agent (self) | 0.4814 | 0.2075 | 51.5 | 26.2 | 76.20 |
| Long Context | not found | not found | 47.5 | 23.5 | not found |
| HippoRAG / HippoRAG2 | 0.3836 | 0.0732 | 27.5 | 23.8 | 72.10 |
| Embedding | not found | not found | 37.5 | 21.4 | not found |
| MemoryBank | 0.2648 | 0.0725 | 31.5 | 17.2 | not found |
| Mem0 | 0.2770 | 0.1141 | 30.0 | 15.6 | 63.51 |
| A-mem | 0.3498 | 0.1158 | not found | not found | 60.84 |
| Mem1 | 0.1429 | 0.0928 | not found | not found | not found |
| GraphRAG | not found | not found | not found | not found | 65.39 |

## 5. leaderboard.letta.com — Context-Bench

Self-reported by Letta. Last updated Mar 13, 2026. No memory leaderboard appears on the page. Source: https://leaderboard.letta.com [P].

**Filesystem suite**

| Model | Score | Cost |
|---|---|---|
| gpt-5.2-codex-xhigh | 93% | $44.46 |
| gpt-5.4-xhigh | 89% | $43.52 |
| claude-sonnet-4-6 | 88% | $116.09 |
| gpt-5.2-xhigh | 87% | $76.72 |
| gpt-5.3-codex-xhigh | 85% | $40.83 |
| claude-opus-4-6 | 84% | $268.44 |
| gemini-3-flash | 82% | $37.80 |
| gemini-3.1 | 79% | $97.68 |
| gpt-5-mini-high | 67% | $35.93 |
| claude-opus-4-5 | 63% | $567.66 |
| kimi-k2.5 | 57% | $27.36 |
| claude-sonnet-4-5 | 48% | $405.01 |
| claude-haiku-4-5 | 43% | $117.55 |
| glm-5 | 39% | $85.87 |
| minimax-m2.5 | 37% | $50.28 |

**Skills suite (no cost column on the page)**

| Model | Task completion | Skill use |
|---|---|---|
| gpt-5.2 xhigh | 85.31% | 63.12% |
| gpt-5.2 high | 84.47% | 54.21% |
| claude-opus-4-6 | 81.32% | 62.64% |
| claude-sonnet-4-6 | 79.08% | 64.8% |
| gpt-5.2 medium | 77.55% | 49.74% |
| claude-sonnet-4-5 | 76.5% | 72% |
| claude-opus-4-5 | 75.54% | 68.82% |
| deepseek-chat | 75.33% | 53.62% |
| claude-opus-4-1 | 74.4% | 71.8% |
| gemini-3-pro | 72.73% | 64.29% |
| deepseek-reasoner | 70.48% | 56.12% |
| gpt-5 | 70.2% | 51.4% |
| claude-haiku-4-5 | 69.7% | 57.3% |
| gpt-5-mini | 68.8% | 45.5% |
| glm-4.6 | 65.9% | 50% |
| gpt-5.1-codex | 64.84% | 55.73% |
| gpt-5.1 | 63.75% | 55.75% |
| gemini-3-flash | 59.54% | 59.54% |
| mistral-large-3 | 56.25% | 36.93% |
| gpt-5-nano | 52.8% | 24% |
| gpt-5.1-codex-mini | 49.72% | 23.58% |
| gpt-4.1 | 36.1% | 31.3% |

## 6. arXiv 2607.26611 — CAPA (July 2026)

300 held-out sessions. ES = executable success, FT-ES = first-turn executable success, TTC = turns to completion. Source: https://arxiv.org/html/2607.26611 [P].

| Model | No history ES / FT-ES / TTC | Same-user history ES / FT-ES / TTC |
|---|---|---|
| GPT-5.5 | 74.3% / 2.3% / 4.417 | 84.3% / 31.0% / 2.970 |
| ChatGPT-5.6-Sol | 79.0% / 2.7% / 4.277 | 78.7% / 18.3% / 3.483 |
| Claude Opus 4.8 | 88.0% / 24.3% / 2.800 | 90.0% / 60.3% / 2.113 |
| Claude Sonnet 4.6 | 76.0% / 6.3% / 3.970 | 83.7% / 14.0% / 3.380 |
| Gemini 3.5 Flash | 79.3% / 17.0% / 3.663 | 81.7% / 38.7% / 2.927 |
| DeepSeek V4 Pro | 76.3% / 15.3% / 4.087 | 79.0% / 17.7% / 3.667 |
| Kimi K2.6 | 77.0% / 22.3% / 3.710 | 82.0% / 32.3% / 3.083 |
| GLM-5.2 | 85.3% / 18.7% / 3.217 | 89.7% / 46.7% / 2.457 |
| Qwen3.7-Max | 77.7% / 17.7% / 3.933 | 82.7% / 29.7% / 3.120 |
| Llama-3.3-70B | 10.0% / 5.7% / 7.450 | 30.0% / 16.0% / 6.250 |
| Qwen3-8B | 23.3% / 18.3% / 6.443 | 27.7% / 23.0% / 6.133 |
| Qwen3.5-27B | 56.0% / 10.7% / 5.337 | 74.3% / 21.3% / 3.990 |

**Controls (ES / FT-ES / TTC)**

| Condition | GPT-5.5 | DeepSeek V4 Pro | GLM-5.2 |
|---|---|---|---|
| Shuffled history | 85.00% / 29.00% / 3.010 | 77.67% / 15.67% / 3.763 | 89.00% / 34.67% / 2.643 |
| mem0 | 85.67% / 11.67% / 3.313 | 73.33% / 9.33% / 4.300 | 83.67% / 18.67% / 3.527 |
| A-mem | 85.67% / 29.33% / 2.980 | 74.67% / 11.67% / 4.260 | 81.33% / 22.67% / 3.313 |
| History gated ("Ours", self) | 83.33% / 44.33% / 2.793 | 79.00% / 18.33% / 3.733 | 90.67% / 51.33% / 2.280 |

## 7. New or relevant studies

**7a. SCLATE (Apple), arXiv 2609.32391v2, 29 Sep 2026** — MetaClaw pass accuracy %, 346 rounds over a 30-workday arc; total tokens in millions in parentheses. Source: https://arxiv.org/html/2609.32391 [P].

| Model | Claude Code no-mem | Claude Code native | Claude Code + Mem0 | Claude Code + Hindsight | Claude Code + GBrain | Hermes no-mem | Hermes native | Hermes + Mem0 | Hermes + Hindsight | Codex native |
|---|---|---|---|---|---|---|---|---|---|---|
| Haiku-4.5 | 40.2 (34) | 46.0 (38) | 69.7 (77) | 58.7 (67) | 56.7 (99) | 43.6 (78) | 59.8 (242) | 61.9 (270) | 61.0 (256) | 44.8 (42) |
| Sonnet-5 | 43.9 (51) | 51.2 (67) | 57.5 (159) | 50.9 (104) | 62.1 (179) | 43.1 (76) | 47.4 (197) | 59.0 (442) | 50.3 (310) | 56.7 (70) |
| Opus-4.6 | 48.8 (45) | 65.0 (57) | 66.5 (122) | 71.1 (100) | 74.0 (107) | 46.5 (59) | 68.5 (148) | 65.0 (252) | 66.8 (203) | 51.5 (31) |
| Opus-4.8 | 48.6 (41) | 60.4 (42) | 66.8 (176) | 74.0 (109) | 67.6 (144) | 45.4 (65) | 64.2 (166) | 64.7 (209) | 61.9 (198) | 48.6 (34) |
| Gemini-3.7F | 63.9 (227) | 79.2 (155) | 79.2 (349) | 81.8 (228) | 79.5 (295) | 73.4 (317) | 77.8 (588) | 79.5 (625) | 80.1 (528) | 73.4 (322) |
| GPT-5.4 | 40.5 (30) | 50.3 (33) | 56.4 (67) | 53.2 (63) | 53.8 (89) | 41.0 (41) | 53.8 (95) | 68.8 (130) | 57.8 (118) | 40.8 (16) |
| GLM-5.3F | 46.8 | 65.0 | 66.8 | 65.9 | 66.2 | 47.1 (74) | 60.4 (213) | 67.3 (436) | 64.5 (250) | 60.4 (108) |
| Qwen3.8-FN | 49.7 | 69.7 | 69.4 | 66.8 | 74.3 | 52.9 (56) | 71.4 (202) | 63.3 (221) | 68.2 (179) | 70.8 (503) |
| DS-Vision | 45.4 | 54.6 | 66.8 | 63.0 | 59.0 | 50.0 (62) | 69.1 (148) | 63.0 (189) | 62.1 (149) | 53.5 (52) |
| DS-V4.1 | 52.0 | 64.2 | 74.3 | 74.3 | 74.9 | 59.3 (83) | 74.0 (171) | 74.6 (236) | 68.8 (251) | 73.7 (57) |

LongMemEval-s (100 tasks, read from text and a figure, so approximate):

| Model | Claude Code native | Hermes native | Hermes + Hindsight |
|---|---|---|---|
| GLM-5.3F | 85 | 66 | 77 |
| DS-V4.1 | 91 | 51 | 74 |

PersonaMem numbers were not found.

**7b. MemoryTax, arXiv 2610.29823, 21 Oct 2026** — one LoCoMo conversation (152 questions), one run per cell, judge GPT-4o-mini. Cells are accuracy % with $ per question. Source: https://arxiv.org/html/2610.29823 [P].

| Method | GPT-4o-mini | GPT-6 Luna | Claude Opus 5.5 | Build cost (Opus 5.5) |
|---|---|---|---|---|
| Full context | 74 / $0.0028 | 92 / $0.0019 | 95 / $0.117 | none ($17.84 per rollout) |
| BM25 | 74 / $0.00028 | 82 / $0.00021 | 90 / $0.013 | none |
| Mem0 | 78 / $0.0013 | 80 / $0.0011 | 95 / $0.074 | $25.88 |
| Zep | 43 / $0.00012 | 51 / $0.00012 | 87 / $0.0077 | $6.22 |
| Pi (harness + files) | 63 / $0.016 | 91 / $0.0032 | 99 / $0.046 | none ($6.95 per rollout) |
| Codex | 28 / $0.0031 | 88 / $0.0050 | 98 / $0.167 | none ($25.41 per rollout) |
| Claude Code | 29 / $0.0020 | 91 / $0.0082 | 97 / $0.187 | none ($28.41 per rollout) |

Mem0 break-even is 372, 545 and 596 questions for the three models respectively.

**7c. Context-file effect studies**

| Study | Date | Setup | Result | Source |
|---|---|---|---|---|
| Gloaguen et al. (ETH), "Evaluating AGENTS.md", arXiv 2602.11988v3 | v3 dated 29 Sep 2026 | SWE-bench Lite (300 tasks), none vs LLM-generated file | Claude Code/Sonnet-4.5 59.9 to 58.7; Codex/GPT-5.2 56.6 to 54.4; Codex/GPT-5.1-mini 47.7 to 47.6; Qwen Code/Qwen3-30B 31.1 to 32.4 | https://arxiv.org/html/2602.11988 [P] |
| same | same | CTXbench (138 tasks), none / LLM-generated / developer-written | Sonnet-4.5 73.2 / 65.2 / 70.3; GPT-5.2 65.2 / 68.1 / 68.1; GPT-5.1-mini 54.3 / 50.7 / 55.8; Qwen3-30B 45.7 / 47.1 / 53.6 | same [P] |
| same | same | Cost per instance, none / LLM / developer (CTXbench) | Sonnet-4.5 $1.15 / $1.33 / $1.30; GPT-5.2 $0.38 / $0.57 / $0.54; GPT-5.1-mini $0.18 / $0.20 / $0.19; Qwen $0.13 / $0.15 / $0.15 | same [P] |
| same | same | Averages | LLM files: −0.5pp (SWE-bench Lite) and −2pp (CTXbench), not significant; cost +20% and +23%. Developer files: +2.4pp (p=0.21), cost up to +19% | same [P] |
| Khatri, "Do Context Files Help Coding Agents?", arXiv 2607.27250 | 28 Jul 2026 | 288 runs, 3 Python repos; none / always-on / selective | Claude Code (sonnet-4-6) 53.3% / 55.6% / 55.6% (p=1.0); Codex CLI (gpt-5.5) 58.8% / 56.9% / 52.9% (p=0.66); Claude wall-clock on one repo 2689 / 2066 / 2032 s | https://arxiv.org/html/2607.27250v1 [P] |
| McMillan, "Instruction Adherence in Coding Agent Configuration Files", arXiv 2605.10039 | 11 May 2026 | 1,650 Claude Code sessions, 16,050 observations; Sonnet 4.6, Opus 4.6 and 4.7 | File size, position, architecture and contradictions: no detectable effect (BF10 0.05–0.10 for size and conflict). Each extra generated function in a session: about 5.6% lower odds of compliance (OR 0.944) | https://arxiv.org/abs/2605.10039 [P, abstract] |
| Treude, arXiv 2601.20404 | Jan 2026 | AGENTS.md and efficiency | Lower mean output tokens; numbers not found | [S] |

**7d. Other harness-level studies**

| Study | Date | What | Numbers | Source |
|---|---|---|---|---|
| MemHarmBench, arXiv 2611.01700 | 1 Nov 2026 | Cross-session prompt injection via persistent memory, 288 cases | Indirect-injection attack success: OpenClaw 75.00 (GPT-5) and 76.39 (Gemini-2.5-Flash); Claude Code 62.50 and 59.38. Direct injection: OpenClaw 88.10 and 90.00; Claude Code 81.82 and 75.00 | https://arxiv.org/html/2611.01700 [P] |
| Doc2Harness, arXiv 2610.20344 | 14 Oct 2026 | Models build a harness; 328 tests, 84 on session state. Not a memory benchmark | Overall / session: GPT-6 Astra 53.05 / 44.0; Opus 5 46.65 / 38.1; Qwen3.8 Max 45.83 / 43.3; GPT-5.6-sol 43.80 / 29.4; Opus 4.8 38.01 / 33.7; mean 38.30 / 29.9 | https://arxiv.org/html/2610.20344v1 [P] |
| Harness the Memory, arXiv 2608.15008 | 15 Aug 2026 | 11 memory substrates, open models; no commercial harnesses | BigCodeBench-Hard pass@1, no-memory to best: Qwen3-8B 8.1 to 15.5; Qwen3-32B 17.6 to 19.6; Gemma-4 14.2 to 20.9 | https://arxiv.org/html/2608.15008v1 [P] |
| HarnessSafe, arXiv 2608.06984 | Aug 2026 | Safety across persistent carriers | Codex CLI 62.3, Hermes 44.5 | [S] |
| Chroma Context Rot | Jul 2025 | No 2026 update with new models found | not found | [S] |
| LOCA-bench, arXiv 2602.07962 | Feb 2026 | Context growth from 8K to 256K | Per-model numbers not found | [S] |

No Sept–Nov 2026 leaderboard comparing Claude Code, Codex CLI, OpenCode, Cursor, Gemini CLI, Hermes and OpenClaw head-to-head on memory was found. SCLATE (three harnesses) and MemoryTax (three harnesses) are the closest.

## 8. Hard constraints (official docs, read 2026-11-17)

**Harnesses**

| Harness | Instruction files read | Always-loaded limits | Scope | Native cross-project/global memory | Auto-memory default | Source |
|---|---|---|---|---|---|---|
| Claude Code | CLAUDE.md (managed, `~/.claude/CLAUDE.md`, project, `CLAUDE.local.md`), `.claude/rules/`; AGENTS.md only when no CLAUDE.md is present (v2.1.277+) | CLAUDE.md: no hard cap, "target under 200 lines", imports up to 4 hops. Auto-memory MEMORY.md: first 200 lines or 25KB, whichever comes first | Instructions: org, user and project. Auto memory: per git repo, machine-local, at `~/.claude/projects/<project>/memory/` | Instructions yes (`~/.claude/CLAUDE.md`); auto memory no | On in local sessions | https://code.claude.com/docs/en/memory [P] |
| Codex CLI | AGENTS.override.md, then AGENTS.md, then `project_doc_fallback_filenames`; global in `~/.codex` | `project_doc_max_bytes` 32 KiB combined; one file per directory | Global plus project root down to cwd | Instructions yes; memories stored under `~/.codex` (`memories_v2/`), per-project scoping not stated | Off (`[features] memories = true` to enable); no size limit stated | https://learn.chatgpt.com/docs/agent-configuration/agents-md and https://learn.chatgpt.com/docs/customization/memories [P] |
| Cursor | `.cursor/rules/*.mdc`, User Rules, Team Rules, AGENTS.md (nested supported) | No hard cap; "keep rules under 500 lines"; `alwaysApply: true` rules load every session | Project, user (global) and team | User Rules are global. Memories: not in official docs; forum reports say the UI was removed in 2.1.x — not verified | not verified | https://cursor.com/docs/context/rules [P]; forum [S] |
| Gemini CLI | GEMINI.md (`~/.gemini/GEMINI.md`, workspace and ancestors, just-in-time in subdirectories); other names via `context.fileName` | No limit stated; all files concatenated into every prompt | Global plus project | Yes (`~/.gemini/GEMINI.md`) | Off; experimental (`experimental.autoMemory`), patches need approval | https://geminicli.com/docs/cli/gemini-md/ and https://geminicli.com/docs/cli/auto-memory/ [P] |
| OpenCode | AGENTS.md; CLAUDE.md as fallback per directory; global `~/.config/opencode/AGENTS.md`, else `~/.claude/CLAUDE.md`; `instructions` config | No limit stated | Global plus project | Instructions yes; no native memory feature documented | none | https://opencode.ai/docs/instructions/ and https://opencode.ai/docs/rules/ [P] |
| Hermes | SOUL.md (global, always); one project file, first match of `.hermes.md`, AGENTS.override.md, AGENTS.md, CLAUDE.md, `.cursorrules` | MEMORY.md 2,200 chars; USER.md 1,375 chars; writes over the limit error. Context files: `context_file_max_chars`, else scaled to the model window (20,000–500,000 chars); subdirectory hints 32,000 chars | Memory is per profile (`~/.hermes/memories/`), not per project | Yes: memory is global per profile; session search over `~/.hermes/state.db` | Sample config shows enabled; "default" not explicitly stated | https://hermes-agent.nousresearch.com/docs/user-guide/features/memory and .../context-files [P] |
| OpenClaw | AGENTS.md, SOUL.md, IDENTITY.md, USER.md, MEMORY.md, BOOTSTRAP.md (new workspaces) | `bootstrapMaxChars` 20,000 per file; `bootstrapTotalMaxChars` 60,000 total; today's and yesterday's daily notes load on `/new` | Per agent workspace (`~/.openclaw/workspace`) | No separate global store documented | Memory flush on; dreaming on | https://docs.openclaw.ai/concepts/system-prompt and https://docs.openclaw.ai/concepts/memory [P] |
| Letta Code | AGENTS.md/CLAUDE.md ingestion at `/init`: not verified | Per-file or `system/` char limit: not verified. Storage cap 5 MiB (Free) or 50 MiB (Pro) per memory repository | Per agent (git-backed MemFS), shared across that agent's conversations | Per agent, so it follows the agent across projects; details not verified | MemFS on by default for new agents [S]; dreaming defaults not verified | https://docs.letta.com/letta-code/memory [P] |

**Flagship models**

| Vendor | Model | Context window | Max output | Source |
|---|---|---|---|---|
| Anthropic | Claude Fable 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5 | 1M tokens | 128K (Batch API: 300K with beta header on Opus 5.5, Sonnet 5.5 and Haiku 5.5) | https://platform.claude.com/docs/en/about-claude/models/overview [P] |
| OpenAI | GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, GPT-6 Luna | 1.05M | 128K | https://developers.openai.com/api/docs/models [P] |
| Google | Gemini 4 Carbon (page updated Nov 2026) | 1,048,576 (input and output combined) | 65,536 default; up to 1,048,576 with long decode | https://aistudio.google.com/docs/models/gemini-4-carbon [P] |
| Google | Gemini 4 Argon, Gemini 4 Hydrogen | 1M | "64K / 1M" | https://aistudio.google.com/docs/models [P] |
