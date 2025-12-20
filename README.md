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
| **6**  | Building Trustworthy AI Agents       | Safety guardrails via system messages; threat modeling and mitigations; add human-in-the-loop approvals for sensitive actions. | [Guidance](days/day06.md) \| [Notes](notes/day06_notes.md) |
| **7**  | Observability & Evaluation in Production | Design trace/span telemetry; track latency, cost, and success; build an offline eval set and design an online feedback loop for continuous improvement. | [Guidance](days/day07.md) \| [Notes](notes/day07_notes.md) |
| **8**  | Prompt Engineering Fundamentals        | Build robust prompts with components; apply core techniques (clear + recency, priming, syntax, decomposition); use few-shot and non-chat patterns; add grounding with strict schemas; tune `temperature`/`top_p`. | [Guidance](days/day08.md) \| [Notes Template](notes/day08_notes_template.md) |
| **9**  | Function Calling & Tools               | Understand tool calling lifecycle; define tools with JSON Schema & LangChain decorators; handle outputs; apply best practices (strict mode, security). | [Guidance](days/day09.md) \| [Notes](notes/day09_notes.md) |
| **10** | MCP & Function Calling                 | Understand Model Context Protocol (MCP); compare function calling vs. MCP; learn client-server architecture and when to use each approach for scalable AI systems. | [Guidance](days/day10.md) \| [Notes](notes/day10_notes.md) |
| **11** | Agent Skills: From Tools to Workflows  | Encode repository-scoped workflows; distinguish tools vs. skills; apply the layered stack (Skills → MCP → Function Calls) to build consistent, scalable agents. | [Guidance](days/day11.md) \| [Notes](notes/day11_notes.md) \| [Transcript (XHS)](notes/day11_transcript_xhs.md) |

## Product I made during this learning 
Industry Newletter AI agent: https://github.com/jessieffff/newsletter-agent


## Contributing and license

This repository captures a personal learning journey. Feel free to fork, follow along, and adapt the plan to your needs. Contributions are welcome via pull requests or issues. All content is provided under the MIT License; see the `LICENSE` file for details.
