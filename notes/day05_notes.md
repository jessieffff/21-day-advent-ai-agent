# Day 05 Notes  — Building Reliable LLM Workflows with LangGraph

## Why LangGraph

- **Graph workflows:** Nodes perform steps; edges control state transitions. Great for multi-step systems with memory and control flow.
- **Typed state:** Shared, well-defined state merged deterministically for reproducibility and safe retries.
- **Subgraphs:** Reusable building blocks (planners, evaluators, tools) that compose into larger systems.

## LangChain and LangGraph: How They Relate

- **Ecosystem vs. Runtime:** LangChain is a broad framework/ecosystem for building LLM apps (prompting, tools, retrieval, integrations). LangGraph is a runtime/modeling layer for stateful, graph-structured workflows on top of LLMs.
- **Complementary Layers:** Use LangChain for components (LLMs, tools, retrievers, document loaders, vector stores). Use LangGraph to orchestrate those components with typed state, control flow, and checkpointing.
- **Structured Outputs & Tools:** Both support tool calling and structured outputs; LangGraph emphasizes schema-driven state transitions and deterministic merges, while LangChain provides the primitives and integrations.
- **Migration Path:** Start with a LangChain pipeline. As complexity grows (parallelization, routing, retries, auditability), wrap steps in LangGraph nodes/subgraphs to gain determinism and observability without rewriting integrations.
- **When to choose which:**
	- Simple, single-pass app → LangChain alone is sufficient.
	- Multi-step, stateful, auditable workflow → LangGraph orchestrating LangChain components.

## Essential Augmentations

- **Tool calling:** Invoke APIs/functions when needed; ground answers with real data.
- **Structured outputs:** Enforce schemas (JSON/Pydantic) to reduce hallucinations and enable validation.
- **Short-term memory:** Scratchpads/buffers to capture intermediate reasoning within a run; checkpoint selectively.

## Design Patterns Comparison to Day 04 (Pattern Catalog)
- **Parallelization ≈ Concurrent:** Both reduce latency via independent runs; require deterministic aggregation and conflict handling.
- **Routing ≈ Handoff:** Both direct tasks to specialists; Day 05 stresses schema-driven, auditable decisions vs. Day 04’s triage-style handoffs.
- **Orchestrator–Worker ≈ Magentic (Planning):** Both decompose and iterate plans; Day 05 highlights deterministic synthesis and dynamic fan-out.
- **Evaluator–Optimizer vs. Group Chat:** Both add quality gates; Day 05 uses explicit tests/metrics, while Day 04 leverages debate/consensus.
- **Prompt chaining ≈ Sequential:** Linear, verifiable steps, provenance, and targeted retries.
- **LangGraph state/determinism vs. Day 04 control:** Formal typed state and checkpoints (Day 05) vs. heuristic pattern choice (Day 04).

## Implementation Tips
- **Schema-first:** Define inputs/outputs up front; treat prompts as functions.
- **Deterministic merges:** Use explicit reducers when joining parallel results.
- **Guardrails:** Add time/budget caps and termination criteria to avoid loops.
- **Observability:** Log decisions, checkpoints, and evaluation outcomes for auditability.

## When to Use What

- **Start simple:** Single-agent + tools; add orchestration only when specialization/parallelism is needed.
- **Choose by task shape:** Linear → chaining; independent analyses → parallel; dynamic triage → routing; open-ended → orchestrator–worker + evaluator–optimizer.

## Project Workflow: Newsletter Agent (LangGraph)

This project uses a three-node LangGraph pipeline to generate a personalized newsletter end-to-end. It demonstrates typed state, deterministic control flow, and checkpointing in practice.

- **Graph (sequential):** `START → Fetch Candidates → Grounded Search → Select & Write → END`
- **Typed state (`AgentState`):** `subscription`, `candidates`, `selected`, `newsletter`, `errors` (optional fields; nodes add incrementally).
- **Node 1 — Fetch Candidates:**
	- Aggregates content from RSS (sync) and optionally NYT + X/Twitter (async) using topic-based queries.
	- Best-effort error handling; failures accumulate in `errors[]` without stopping the run.
- **Node 2 — Grounded Search:**
	- Augments candidates via Azure AI Foundry grounding (fresh web results, last 7 days).
	- Merges new items non-destructively; gracefully degrades if Foundry is unconfigured.
- **Node 3 — Select & Write:**
	- Deduplicates, ranks heuristically, selects top N, summarizes with Azure OpenAI (`gpt-4o-mini`, temperature 0.2), and renders HTML + text.
	- Current parsing uses regex; roadmap includes structured outputs to enforce JSON schemas.
- **Execution entry:** `run_once(subscription)` builds the graph, runs with initial state, and returns the final `Newsletter`.
- **Performance & future work:**
	- Parallelize RSS fetches with `asyncio.gather()`; expect 40–60% Node 1 speedup.
	- Replace regex parsing with structured outputs; improve ranking; persist checkpoints.

Refer to `notes/workflow-reference.md` for detailed architecture, configuration, and testing guidance.




