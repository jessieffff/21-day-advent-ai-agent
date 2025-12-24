# Day 12 – Agentic RAG (Retrieval‑Augmented Generation)

_Timebox: ~1 hour_

## Knowledge goals

- Understand the basic RAG loop: retrieve → augment → generate
- Identify limitations of vanilla RAG (recall, grounding, multi‑hop reasoning)
- Define Agentic RAG and how it extends RAG with planning, tools, and verification
- Compare RAG vs Agentic RAG in capabilities, complexity, and trade‑offs
- Know when to use each approach and how to iterate from RAG → Agentic RAG

## Learning materials (≈ 20–25 minutes)

- Read: What is Agentic RAG?  
  Overview of how agents add planning, multi‑step retrieval, and verification to classic RAG.  
  Reference: Weaviate Blog — What is Agentic RAG  
  https://weaviate.io/blog/what-is-agentic-rag

## Core concepts

### What is RAG?

- RAG augments an LLM with external knowledge at inference time. The typical pipeline:
  1) Embed and index documents in a vector store  
  2) At query time, retrieve top‑k chunks relevant to the question  
  3) Provide the retrieved context to the LLM to generate an answer
- Strengths:
  - Reduces hallucinations by grounding answers in retrieved context  
  - Keeps models up‑to‑date without retraining  
  - Straightforward to implement end‑to‑end
- Limitations:
  - One‑shot retrieval may miss context (recall and coverage issues)  
  - No decomposition for multi‑hop or complex tasks  
  - Limited self‑checking or verification  
  - Fixed prompt and static retrieval hyperparameters

### What is Agentic RAG?

- Agentic RAG introduces an agent loop around the RAG core to plan, act, observe, and revise. Instead of a single retrieve→generate step, the agent can:
  - Decompose a question into sub‑tasks (planning)  
  - Perform iterative retrieval with query reformulation  
  - Use tools (e.g., search, re‑rankers, web APIs, code execution)  
  - Cross‑check answers with verification or self‑consistency  
  - Decide when more evidence is needed before finalizing
- A helpful mental model (Sense→Plan→Retrieve→Reason→Verify→Answer):
  - Sense: read the user goal and current context  
  - Plan: break down into steps; pick tools and retrieval strategy  
  - Retrieve: run one or more retrieval passes, possibly with re‑ranking  
  - Reason: integrate evidence; draft a candidate answer  
  - Verify: check citations, detect gaps, optionally retrieve again  
  - Answer: produce a grounded response with sources
- Benefits:
  - Better recall and coverage for complex queries  
  - Multi‑hop reasoning across documents and tools  
  - Higher factuality through iterative verification
- Costs:
  - Higher latency and compute  
  - More moving parts (planning, tools, state management)  
  - Requires observability and evaluation to tune

## How they fit together

- Vanilla RAG is a solid baseline for single‑turn, fact‑seeking tasks with clear scope and good chunking.  
- Agentic RAG wraps RAG with a decision‑making loop that can reformulate queries, chain retrieval steps, invoke additional tools, and verify outputs before answering.  
- In practice, many systems start with RAG, then add agentic behaviors selectively where they improve quality (e.g., query decomposition, re‑ranking, citation checks).

## RAG vs Agentic RAG — trade‑offs

- Simplicity vs Capability: RAG is simpler and faster; Agentic RAG solves harder questions but adds complexity.  
- Determinism vs Adaptivity: RAG has fixed hyperparameters; Agentic RAG adapts strategy per query.  
- Cost/Latency: Expect higher cost/latency for Agentic RAG due to extra steps.  
- Governance: Agentic loops need guardrails (max steps, verification gates, tool access controls).

## Activities (≈ 25–35 minutes)

### Step 1: Baseline RAG (8–10 minutes)
- Define a small corpus; index with embeddings and metadata.  
- Implement retrieve(k) → prompt(LLM) → answer.  
- Log retrievals, prompts, and answers for inspection.

### Step 2: Quality boosters (8–10 minutes)
- Add a re‑ranking step to improve top‑k quality.  
- Implement query reformulation (e.g., expand synonyms, add entities).  
- Output citations and highlight which chunks support each claim.

### Step 3: Agentic upgrades (10–15 minutes)
- Add a planning step: if the question seems multi‑hop, split into sub‑queries.  
- Iterative retrieval: loop with a stop condition (confidence, step cap).  
- Verification: run a lightweight fact‑check pass (e.g., retrieve‑to‑verify or consensus across two samples).  
- Tool use: allow a web/doc search tool for missing pieces; optionally add a calculator or code runner for quantitative checks.

## Knowledge check

- Describe the classic RAG pipeline and its main benefits.  
- What failure modes of vanilla RAG does Agentic RAG address?  
- Give two examples of agentic behaviors that improve factuality.  
- When would you prefer baseline RAG over Agentic RAG?  
- What guardrails would you add to an agentic loop?
