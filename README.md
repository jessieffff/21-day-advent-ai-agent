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

| Day  | Topic                              | Key goals |
|---|------------------------------------|---|
| **1**  | AI foundations & agent basics   | Understand agent vs. chatbot, the perceive–decide–act loop, and common patterns. |
| **2**  | LangChain primer                 | Learn LangChain core componeents (agent, models, prompts, chains)  |
| **3**  | Tool calling                     | Add simple tools (math, search) and handle structured outputs. |
| **4**  | Memory basics                    | Use LangChain memory primitives for short-term context. |
| **5**  | Retrieval setup                  | Build a basic RAG chain with a local vector store. |
| **6**  | Agent design patterns            | Compare reactive vs. plan-and-execute agents; scope tasks with SOPs. |
| **7**  | LangGraph intro                  | Model a small graph for multi-step tasks; run locally. |
| **8**  | Observability quickstart         | Add LangSmith or simple logging; capture traces for a run. |
| **9**  | Guardrails & prompt hygiene      | Add instructions, output schemas, and safety checks. |
| **10** | Tooling expansion                | Integrate a web search or file tool; handle tool errors. |
| **11** | Multi-agent patterns             | Coordinate two agents with a shared memory/toolbox. |
| **12** | Planner/worker graph             | Build a planner + executor flow in LangGraph. |
| **13** | Mid-journey reflection           | Review learnings, adjust goals, and backlog. |
| **14** | Retrieval improvements           | Add sources, citations, and rerankers; evaluate RAG quality. |
| **15** | Evaluation                       | Create eval prompts and simple quality metrics; run batch tests. |
| **16** | State & persistence              | Persist graph state to disk/DB; resume runs. |
| **17** | Async & streaming                | Add streaming outputs and concurrent tool calls. |
| **18** | External APIs                    | Wire a custom API client as a tool; handle auth securely. |
| **19** | Deployment options               | Compare FastAPI, serverless, and background workers; ship a minimal API. |
| **20** | Final project design             | Choose a multi-agent goal, sketch architecture, and define tasks. |
| **21** | Final project build & test       | Implement, evaluate, and document the project with LangChain/LangGraph. |

## Contributing and license

This repository captures a personal learning journey. Feel free to fork, follow along, and adapt the plan to your needs. Contributions are welcome via pull requests or issues. All content is provided under the MIT License; see the `LICENSE` file for details.
