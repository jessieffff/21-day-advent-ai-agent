# Day 1 – AI foundations & agent basics

_Timebox: ~1 hour_

## Knowledge goals

- Distinguish agents from chatbots and simple chains; understand when to use an agent.
- Learn the core perceive–decide–act loop and how tools fit into it.
- Get a light taxonomy of agent patterns (reactive, plan-and-execute, multi-agent handoff).

## Learning materials (≈ 20–25 minutes)

- Read: [**LangChain — Agents documentation**](https://docs.langchain.com/oss/python/langchain/agents) (core reference on how agents and tools work) 
- Read: [**LangChain Overview / LangGraph introduction**](https://docs.langchain.com/oss/python/langchain/overview )(when to use LangChain vs LangGraph; architecture & workflow explanation)
- Read: [**OpenAI — “A Practical Guide to Building Agents”**](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)(framework-agnostic guide covering the perceive → decide → act loop; tool use; safety & design patterns) — h
- Optional (tutorial-style): [**LangGraph + agent/workflow patterns guide**](https://docs.langchain.com/oss/python/langgraph/workflows-agents)(for multi-step agents & orchestration patterns)
## Activities (about 30 minutes)

- Draft your own one-paragraph definition of an AI agent vs. chatbot vs. chain.
- Sketch the perceive–decide–act loop and annotate where tools are called.
- List 3–5 real tasks where an agent is useful and 3 where a simple chain/RAG is enough.
- Create a small backlog for this journey: note skills you want to emphasize (e.g., tool use, evaluation, deployment).
- Capture notes in `notes/day01_notes.md` (or your journal) so you can revisit later.

## Knowledge check

- In your words: why use an agent instead of a plain chat or RAG chain?
- Describe the perceive–decide–act loop and how tool calls fit in.
- Give one example each: a task suited for a reactive agent, and a task better handled by plan-and-execute.
