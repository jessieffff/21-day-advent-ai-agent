# 21-Day AI Agent Learning Journey

Welcome! This repository documents a 21-day learning journey to understand and build AI agents. Over the next three weeks you will learn fundamental AI concepts, study different types of agents, explore popular agentic frameworks, and gradually build your own multi-agent application using LangChain and LangGraph. Each day is scoped to roughly one hour: a short lesson, a focused activity, and a quick knowledge check.

## About this project

The journey centers on LangChain and LangGraph for building capable, reliable agents in Python. You will still compare other frameworks (e.g., AutoGen, Semantic Kernel) to understand trade-offs, but the build path uses LangChain primitives, tool calling, and graph orchestration to ship a small but real multi-agent project.

## Using this repo

- Each day’s plan lives in the `days/` directory as `dayXX.md` (where `XX` is the day number). These files describe the knowledge goals, recommended resources, activities, and self-check questions.
- Feel free to update the plan as you go—learning is iterative! Use the repository’s issues or a personal journal to record notes and reflections.
- See the summary schedule below for a quick overview of the topics covered each day.

## Prerequisites

- Programming knowledge: familiarity with Python is required.
- Environment: Python 3.10 or later. Recommended packages:
  ```bash
  pip install "langchain>=0.3" "langgraph>=0.2" langchain-openai
  ```
- API keys: some exercises require an OpenAI or Azure OpenAI key. Configure `OPENAI_API_KEY` (or Azure equivalents) in your environment.
- Optional extras: `langchain-community` for integrations, `duckduckgo-search` for web tools, and `chromadb` or `faiss-cpu` for vector stores when adding retrieval.

## Schedule summary

The table below gives a high-level overview of the 21-day curriculum (about one hour per day). See the individual day files in the `days/` folder for details.

| Day  | Topic                              | Key goals | Materials |
|---|------------------------------------|----|---|
| **1**  | AI foundations & agent basics   | Understand agent vs. chatbot, the perceive–decide–act loop, and common patterns. | [Guidance](days/day01.md) \| [Notes](notes/day01_notes.md) |
| **2**  | LangChain primer                 | Learn LangChain core componeents (agent, models, prompts, chains)  | [Guidance](days/day02.md) \| [Notes](notes/day02_notes.md) |
| **3**  | Project Planning                | Translate the product idea into execution-ready artifacts (PRD, plan, repo scaffold) | [Guidance](days/day03.md) \| [Notes](notes/day03_notes.md) |
| **4**  | AI Agent Orchestration Patterns  | Learn 5 core patterns (Sequential, Concurrent, Group Chat, Handoff, Magentic) and when to use each. | [Guidance](days/day04.md) \| [Notes](notes/day04_notes.md) |
| **5**  | Reliable LLM Workflows with LangGraph | Model multi-step, stateful workflows using typed state, subgraphs, and deterministic control flow; understand how LangChain components plug into LangGraph orchestration. | [Guidance](days/day05.md) \| [Notes](notes/day05_notes.md) |

## Product I made during this learning 
Industry Newletter AI agent: https://github.com/jessieffff/newsletter-agent

## Day 05 overview — Building Reliable LLM Workflows with LangGraph

Day 05 focuses on using LangGraph to orchestrate reliable, multi-step LLM workflows.

- **Why LangGraph:** Graph-structured workflows with nodes and edges, typed shared state for reproducibility and safe retries, and reusable subgraphs for planners, evaluators, and tools.
- **How it relates to LangChain:** LangChain provides the ecosystem and components (LLMs, tools, retrievers, loaders, vector stores). LangGraph is the runtime/modeling layer that orchestrates those components with typed state, control flow, parallelization, and checkpointing. Start simple in LangChain, then wrap complex steps in LangGraph nodes/subgraphs as needs grow.
- **Essential augmentations:** Tool calling to ground answers in real data; structured outputs (JSON/Pydantic) to reduce hallucinations and enable validation; short-term memory with scratchpads and selective checkpoints.
- **Design patterns vs Day 04:** Parallelization/concurrent, routing/handoff, orchestrator–worker (planning), evaluator–optimizer vs. group chat, prompt chaining/sequential. LangGraph adds formal typed state, determinism, and auditability.
- **Implementation tips:** Schema-first design, deterministic merges for parallel results, clear guardrails (time/budget caps, termination criteria), and strong observability with logs and checkpoints.
- **When to use what:** Choose chaining for linear tasks, parallel for independent analyses, routing for dynamic triage, and orchestrator–worker + evaluator–optimizer for open-ended tasks.

### Case study: Newsletter Agent (LangGraph)

A three-node sequential LangGraph pipeline generates a personalized newsletter end-to-end, demonstrating typed state, deterministic control flow, and checkpointing:

- **Graph:** `START → Fetch Candidates → Grounded Search → Select & Write → END`
- **Typed state (`AgentState`):** `subscription`, `candidates`, `selected`, `newsletter`, `errors` accumulated incrementally.
- **Node 1 — Fetch Candidates:** Aggregate RSS (sync) and optional NYT/X (async) by topics; errors stored without stopping the run.
- **Node 2 — Grounded Search:** Augment candidates via Azure AI Foundry (last 7 days), non-destructive merge, graceful degradation if unconfigured.
- **Node 3 — Select & Write:** Deduplicate, rank, select top N, summarize via Azure OpenAI, render HTML + text; roadmap to replace regex parsing with structured outputs.
- **Entry point:** `run_once(subscription)` builds and executes the graph, returning a final newsletter.
- **Future work:** Parallelize RSS with `asyncio.gather()` (expect 40–60% speedup), enforce JSON schemas, improve ranking, persist checkpoints.

## Contributing and license

This repository captures a personal learning journey. Feel free to fork, follow along, and adapt the plan to your needs. Contributions are welcome via pull requests or issues. All content is provided under the MIT License; see the `LICENSE` file for details.
