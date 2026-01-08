# Day 14 — Agentic Protocols: MCP, A2A, and NLWeb

_Timebox: ~1 hour_

## Knowledge goals

- Understand why agentic protocols matter (standardization, interoperability, security boundaries).
- Distinguish the roles of **MCP** (tools + context), **A2A** (agent-to-agent collaboration), and **NLWeb** (natural-language interface to websites and web content).
- Identify where each protocol fits in an end-to-end agentic system (single-agent tool use vs. multi-agent delegation vs. “agent-accessible” websites).

## Learning materials (≈ 20–25 minutes)

- Read/Watch: **“Using Agentic Protocols (MCP, A2A and NLWeb)”** lesson (repo + video link in README).  [GitHub](https://raw.githubusercontent.com/microsoft/ai-agents-for-beginners/main/11-agentic-protocols/README.md)
- Read: **MCP Specification / Docs** (authoritative spec + conceptual overview).  [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25?utm_source=chatgpt.com)
- Read: **A2A protocol overview/spec** (core concepts: AgentCard, tasks/artifacts, interaction model).  [Agent2Agent](https://agent2agent.info/specification/?utm_source=chatgpt.com)
- Read: **NLWeb repo + overview** (how NLWeb enables natural-language access to site content and how it relates to MCP).  [GitHub](https://github.com/nlweb-ai/NLWeb?utm_source=chatgpt.com)
- Optional (security perspective): A brief write-up on early NLWeb security learnings and the importance of patching/updating reference implementations.  [The Verge](https://www.theverge.com/news/719617/microsoft-nlweb-security-flaw-agentic-web?utm_source=chatgpt.com)

## Activities (about 30 minutes)

### 1) Build a “protocol selection matrix” for a concrete product
Pick a product context (example: a newsletter agent, research assistant, or internal DevOps helper) and fill in:

- **When MCP is the right fit**
  - Need a consistent way to expose **tools**, **resources**, and **prompt templates** behind a stable interface.  
- **When A2A is the right fit**
  - Need to delegate subtasks to **specialized remote agents** (potentially owned by different teams/orgs) with clear capabilities and an execution/result contract.  
- **When NLWeb is the right fit**
  - Need a website (or web property) to become naturally queryable by humans and agents, using embeddings + retrieval, and optionally to be consumable as an MCP endpoint. 

Deliverable: a 1-page decision note with 3 columns (MCP / A2A / NLWeb) listing “use it when…”, “avoid it when…”, and “what it standardizes”.

### 2) MCP exercise: design a minimal MCP server surface area
Draft an MCP server capability outline (no code required) for a domain you know. Include:

- **Tools** (actions): 3–6 functions with clear I/O schemas (e.g., `search_web`, `fetch_rss_items`, `summarize_url`).
- **Resources** (read-only): what data should be retrievable on demand (e.g., `newsletter_archive/{date}`, `run_logs/{run_id}`).
- **Prompts** (templates): 2–3 reusable prompts (e.g., “rank items”, “write executive summary”). 

Deliverable: a short capabilities listing (names + one-line descriptions + inputs/outputs).

### 3) A2A exercise: decompose one complex request into agent delegation
Take a single user goal (e.g., “Plan a trip” or “Produce a weekly AI newsletter”) and define:

- **AgentCard** entries for 2–4 specialized agents (name, description, skills, endpoint, capabilities).  [oai_citation:9‡GitHub](https://raw.githubusercontent.com/microsoft/ai-agents-for-beginners/main/11-agentic-protocols/README.md)
- A delegation plan:
  - What context each downstream agent needs
  - What artifacts each agent returns
  - How the orchestrator agent merges results into a final response (including error handling / partial completion)

Deliverable: a short “handoff contract” per agent: `inputs → artifact → success criteria`.

### 4) NLWeb exercise: make a site “agent-accessible” (conceptual)
Pick a website content set (docs, product catalog, blog posts, internal wiki) and outline:

- What structured data is available (Schema.org or analogous structured formats; RSS if applicable).  [oai_citation:10‡GitHub](https://raw.githubusercontent.com/microsoft/ai-agents-for-beginners/main/11-agentic-protocols/README.md)
- Embedding + retrieval approach (what gets embedded, update cadence, what vector store is used).
- Query flows:
  - Human query through a chat UI
  - Agent query through an MCP-style `ask` interface (conceptually)

Deliverable: a one-page architecture sketch with ingestion → embeddings → vector DB → response formatting.

## Knowledge check

- In one paragraph, explain the difference between:
  - **MCP** connecting an agent to tools/data vs.
  - **A2A** connecting an agent to another agent vs.
  - **NLWeb** connecting natural language queries to a website’s content.  
- MCP:
  - Name the **three core primitives** an MCP server can expose, and give one example of each.  
- A2A:
  - What is an **AgentCard** and why does it matter for discovery and interoperability? 
  - What is an **artifact** in A2A terms?  
- NLWeb:
  - What role do **embeddings** and a **vector database** play in NLWeb? 
  - How does NLWeb relate to MCP conceptually (what additional interface does it provide)?  
- Scenario questions:
  1) A local IDE assistant needs to discover and call tools from multiple backends without hardcoding each integration. Which protocol pattern fits best and why?
  2) A “travel orchestrator” agent needs to delegate booking to multiple vendor-owned agents. Which protocol pattern fits best and why?
  3) A website wants users (and agents) to ask natural-language questions over its catalog and return grounded results. Which protocol pattern fits best and why?