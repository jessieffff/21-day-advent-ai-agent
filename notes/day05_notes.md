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

## Key Components and Concepts in LangGraph Workflows

- **Graph (nodes & edges):** A directed workflow where nodes perform steps and edges define control flow. Supports sequential paths, branches, loops, and parallel fan-out/fan-in.
- **Nodes:** Stateless functions or composites that consume typed state and emit partial updates. Use **subgraphs** to encapsulate reusable planners, evaluators, or tool chains.
- **Typed state (schema):** A shared, well-defined state object (e.g., `AgentState`) with optional fields. Each node adds or updates fields; merges are deterministic to enable reproducibility and safe retries.
- **Reducers & deterministic merges:** Per-key merge strategies (replace, append, set/union, numeric ops, or custom reducers) resolve updates from parallel branches in a confluent, audit-friendly way.
- **Control flow primitives:** Conditional routing, map/fan-out across items, join/fan-in, bounded loops with explicit termination criteria (time/budget caps, convergence tests).
- **Tool calling & structured outputs:** Nodes may call external APIs/functions; enforce JSON/Pydantic schemas to validate outputs and reduce hallucinations.
- **Short-term memory:** Scratchpads/buffers capture intermediate reasoning within a run; promote only validated artifacts into the typed state.
- **Checkpointing & persistence:** Automatic per-step snapshots enable resume, targeted retries, and full provenance. Plug persistence stores to retain run history.
- **Observability:** Run IDs, event logs, decisions, and metrics for auditability and evaluation. Instrument nodes to track latency, cost, and quality signals.
- **Error handling & guardrails:** Best-effort execution, structured error accumulation, retries/backoff, and cancellation. Guardrails prevent runaway loops and budget overruns.
- **Concurrency semantics:** Parallel branches via async execution (e.g., `asyncio.gather()`), bounded by resource limits; results merged deterministically.
- **Execution API:** Build/compile a graph, then `invoke` for single-pass runs or `stream` for stepwise outputs. Provide thin entry functions (e.g., `run_once(subscription)`) to initialize state and kick off the workflow.


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

## Project Workflow: Newsletter Agent (LangGraph)

This project uses a three-node LangGraph pipeline to generate a personalized newsletter end-to-end. It demonstrates typed state, deterministic control flow, and checkpointing in practice.

### Workflow Code Snippets (Newsletter Agent)

Quick start — one-shot run:

```python
from newsletter_agent.workflow import run_once
from newsletter_agent.types import Subscription

sub = Subscription(
	id="demo",
	topics=["AI agents", "LangGraph"],
	sources=[{"kind": "rss", "value": "https://blog.langchain.dev/feed"}],
	item_count=5,
	tone="concise, professional",
)

newsletter = await run_once(sub)
print(newsletter.subject)
print(newsletter.text)
```

Typed state schema:

```python
from typing import List, TypedDict

class AgentState(TypedDict, total=False):
	subscription: Subscription
	candidates: List[Candidate]
	selected: List[SelectedItem]
	newsletter: Newsletter
	errors: List[str]
```

Node 1 — Fetch Candidates:

```python
async def node_fetch_candidates(state: AgentState) -> AgentState:
	sub = state.get("subscription")
	errors = state.get("errors", [])
	candidates: list[Candidate] = []

	# RSS (sequential)
	for s in sub.sources:
		if s.get("kind") == "rss":
			try:
				candidates += fetch_rss(s["value"], topic_hint=sub.topics[:3])
			except Exception as e:
				errors.append(f"rss:{s['value']}:{e}")

	# Optional sources (NYT/X) if configured
	try:
		candidates += await fetch_nyt_async(sub.topics)
	except Exception as e:
		errors.append(f"nyt:{e}")

	try:
		candidates += await fetch_x_async(sub.topics)
	except Exception as e:
		errors.append(f"x:{e}")

	state["candidates"] = candidates
	state["errors"] = errors
	return state
```

Node 2 — Grounded Search (Azure AI Foundry):

```python
import os

async def node_grounded_search(state: AgentState) -> AgentState:
	sub = state.get("subscription")
	topics = sub.topics or []
	if not topics:
		return state

	if not (os.getenv("FOUNDRY_PROJECT_ENDPOINT") and os.getenv("FOUNDRY_BING_CONNECTION_ID")):
		return state

	try:
		results = await grounded_search_via_foundry(
			query=" OR ".join(topics[:3]), freshness="7d", count=10
		)
		state["candidates"] = (state.get("candidates") or []) + results
	except Exception as e:
		state.setdefault("errors", []).append(f"foundry:{e}")
	return state
```

Node 3 — Select & Write (LLM summarization):

```python
from langchain_openai import AzureChatOpenAI

def build_llm() -> AzureChatOpenAI:
	return AzureChatOpenAI(
		azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
		api_key=os.environ["AZURE_OPENAI_API_KEY"],
		api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
		azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
		temperature=0.2,
		timeout=45,
	)

async def node_select_and_write(state: AgentState) -> AgentState:
	sub = state.get("subscription")
	llm = build_llm()

	candidates = dedupe_candidates(state.get("candidates") or [])
	ranked = simple_rank(candidates)
	picked = ranked[: sub.item_count]

	sys = "You are an expert newsletter editor. Do not invent facts."
	prompt = render_prompt(sub, picked)
	resp = await llm.ainvoke([sys, prompt])

	selected = parse_llm_items(resp)  # robust parsing + fallbacks
	subject = f"Your news digest: {', '.join(sub.topics[:2]) or 'Latest'}"
	state["selected"] = selected
	state["newsletter"] = render_newsletter(subject, selected)
	return state
```

Graph construction and entry:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint import InMemorySaver

def build_graph():
	g = StateGraph(AgentState)
	g.add_node("fetch_candidates", node_fetch_candidates)
	g.add_node("grounded_search", node_grounded_search)
	g.add_node("select_and_write", node_select_and_write)

	g.add_edge(START, "fetch_candidates")
	g.add_edge("fetch_candidates", "grounded_search")
	g.add_edge("grounded_search", "select_and_write")
	g.add_edge("select_and_write", END)

	return g.compile(checkpointer=InMemorySaver())

async def run_once(subscription: Subscription) -> Newsletter:
	graph = build_graph()
	thread_id = f"sub:{subscription.id}"
	final_state = await graph.ainvoke({"subscription": subscription}, thread_id=thread_id)
	return final_state["newsletter"]
```


Refer to `notes/workflow-reference.md` for detailed architecture, configuration, and testing guidance.




