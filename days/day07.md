# Day 7 – AI Agents in Production: Observability & Evaluation

_Timebox: ~1 hour_

## Knowledge goals

- Understand why observability turns agents from “black boxes” into “glass boxes”
- Learn core observability primitives (traces, spans) and what to log/measure
- Design a practical evaluation loop (offline eval → deploy → online eval → improve)
- Identify the key metrics that matter in production (latency, cost, quality, errors)
- Apply cost-control strategies without sacrificing reliability

## Learning materials (≈ 20–25 minutes)

- Read: [**AI Agents in Production: Observability & Evaluation** (Lesson 10)](https://github.com/microsoft/ai-agents-for-beginners/tree/main/10-ai-agents-production)
  - Observability concepts: traces and spans
  - Why observability matters: debugging, latency/cost management, trust/compliance, continuous improvement
  - Key metrics to track: latency, costs, request errors, user feedback (explicit/implicit), accuracy, automated eval metrics
  - Instrumentation approaches: OpenTelemetry (OTel), framework wrappers, manual span attributes (e.g., `user_id`, `session_id`, `model_version`)
  - Evaluation types: offline vs online, and how to combine them into a feedback loop
  - Production issues and mitigations: loops, tool-call failures, multi-agent inconsistency
  - Managing costs: smaller models, routing models, caching

## Activities (about 30–40 minutes)

### Step 1: Define “Success” for One Agent (5–8 minutes)
Pick one agent from your PRD (ideally the most important or risky) and write:
- The agent’s primary user-facing outcome (“what good looks like”)
- 3–5 success criteria you can measure (e.g., correctness, task completion, policy compliance)
- 3–5 failure modes you must detect (e.g., tool loops, hallucinated facts, unsafe outputs)

Capture this in `notes/day07_notes.md`.

### Step 2: Choose Your Observability Events & Fields (8–10 minutes)
Design a minimal “telemetry schema” for an agent run.
- Trace-level fields (whole run): `trace_id`, `user_id` (or pseudonymous), `session_id`, `agent_name`, `agent_version`, `model`, `env`, `start_time`, `end_time`, `success`, `error_type`
- Span-level fields (step): `span_name` (LLM call, retrieval, tool call), `latency_ms`, `token_in`, `token_out`, `tool_name`, `tool_status`, `retry_count`
- Quality signals: `user_rating`, `user_comment`, `implicit_signal` (retries, rephrases)

Write it as a table or bullet list in `notes/day07_notes.md`.

### Step 3: Map Spans to Your Agent Workflow (8–10 minutes)
Sketch your agent’s runtime as a trace tree.
Example (adapt to your agent):
- Trace: “Handle user request”
  - Span: “Classify intent”
  - Span: “Retrieve context (RAG)”
  - Span: “Plan / choose tools”
  - Span: “Tool call: search”
  - Span: “LLM synthesize answer”
  - Span: “Safety/policy check”

Add this trace tree to `notes/day07_notes.md`.

### Step 4: Build an Offline Eval Set (8–10 minutes)
Create a small offline evaluation dataset (start tiny; expand later):
- 10 “smoke tests” (fast, critical cases)
- 10 “edge cases” (tricky or adversarial/ambiguous)
- For each item: input, expected behavior, acceptance rubric (pass/fail or 1–5)

Store this in `notes/day07_notes.md` (or a simple Markdown table).

### Step 5: Design an Online Feedback Loop (5 minutes)
Define what you will collect in production:
- Explicit feedback: thumbs up/down, star rating, short comment
- Implicit feedback: user retries, rephrases, session abandonment, escalation requests
- Triage workflow: how often you review traces, and how you turn failures into new offline eval cases

Document the loop (who/when/how) in `notes/day07_notes.md`.

## Implementation hints

- **Start with one agent**: Instrument one high-value agent first; scale the schema later.
- **Prefer trace/span consistency**: Stable naming enables dashboards and regression detection.
- **Add custom attributes**: Record business-relevant tags (e.g., `tenant`, `plan_tier`, `feature_flag`).
- **Watch for loops**: Add termination conditions, max steps, and “repeated tool call” detection.
- **Measure cost drivers**: Track tokens + tool invocations; identify hotspots and unnecessary LLM calls.
- **Cost controls**: Consider smaller models for simple steps, router models for complexity, and caching for repeated queries.

## Knowledge check

- What’s the difference between a trace and a span, and why do you need both?
- Which 5 metrics best predict your agent’s production health?
- What is your offline evaluation dataset’s acceptance rubric?
- How will you convert production failures into new offline eval cases?
- Where are your biggest cost hotspots (tokens vs tools), and how will you reduce them?

## Next steps

- Instrument your agent with a tracing strategy (OTel + a tool like Langfuse/Azure AI Foundry).
- Create a baseline offline eval and run it on every meaningful change.
- Deploy with online monitoring and a weekly review cadence for failures and costs.
- Add guardrails learned in Day 6 so traces also support safety/compliance audits.
