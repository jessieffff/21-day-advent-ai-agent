# Day 8 – Prompt Engineering Fundamentals

_Timebox: ~1 hour_

## Knowledge goals

- Understand core prompt components: instructions, primary content, examples, cues, supporting content
- Apply essential techniques: clear/recency-aware instructions, priming, syntax, task decomposition
- Use few-shot learning and non-chat patterns effectively with Chat Completions
- Control style/variance with `temperature` and `top_p`; choose one to tune at a time
- Ground model outputs in source data and specify output schemas to reduce hallucinations
- Design prompts for space efficiency and operational reliability in production contexts

## Learning materials (≈ 20–25 minutes)

- Read: **Prompt engineering techniques (Azure AI Foundry)**
  - https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/prompt-engineering?view=foundry-classic
  - Prompt components: instructions, primary content, examples (zero/one/few-shot), cue, supporting content
  - Techniques: start with clear instructions, repeat at end (recency bias), prime output, add syntax/section markers, break tasks down, use affordances (e.g., search/tools), specify output structure
  - Modes: few-shot learning with Chat Completions roles (system/user/assistant), non-chat scenarios
  - Controls: `temperature` vs `top_p` (tune one), grounding context for reliability
  - Best practices: be specific/descriptive, ordering matters, give the model an “out”
  - Space efficiency: tokens, whitespace, tables; when/why Markdown/XML helps

## Activities (about 30–40 minutes)

### Step 1: Decompose a Prompt into Components (6–8 minutes)
Pick a real task from your PRD (e.g., summarize a support email with citations) and rewrite the prompt using the five components:
- Instructions (what to do; constraints; audience)
- Primary content (the text/data to transform)
- Examples (1–2 succinct input→output pairs)
- Cue (prime the start of the desired output)
- Supporting content (date, user/org context, policy notes)
Capture before/after versions in `notes/day08_notes.md`.

### Step 2: Apply Three Techniques to Improve Output (8–10 minutes)
Using the same task, apply at least three of the following and compare outputs:
- Clear instructions first, and repeat key constraints at end (recency)
- Prime the output (e.g., “Key Points:\n- ”) to lock format
- Add clear syntax: separators (`---`), section headings, variables in UPPERCASE
- Break the task into steps (extract facts → propose actions → draft answer)
Record the changed prompt and the observed deltas in quality/format.

### Step 3: Add Grounding and an Output Schema (8–10 minutes)
- Provide a short grounding passage or search snippets. Instruct: “Answer only from the provided text; cite inline.”
- Specify an output schema (e.g., JSON with fields or a Markdown table). Include an “unknown/not found” option.
- Re-run and evaluate whether citations improved factuality and structure.
Document examples and any remaining failure modes in `notes/day08_notes.md`.

### Step 4: Few-shot and Non-chat Variants (6–8 minutes)
- Add one or two few-shot examples using Chat Completions roles (system for policy, user+assistant pairs as demonstrations).
- Create a non-chat version of the same task and compare behavior.
Note where examples materially help or harm generalization.

### Step 5: Explore `temperature` vs `top_p` (5 minutes)
- Run with `temperature=0.2` then `0.8` (keep `top_p` default). Observe determinism/creativity trade-offs.
- Then fix `temperature` and vary `top_p`. Note differences. Avoid changing both at once.
Summarize recommended settings for your task profile.

## Implementation hints

- System vs user roles: Put durable policy, persona, and safety constraints in the system message; task-specific instructions and content in user; optional exemplars as user/assistant turns.
- Recency bias: Repeat key constraints at the end of the prompt to reinforce them.
- Prime & syntax: Use explicit section markers (`---`), headings, and cues to stabilize formatting and enable stop conditions.
- Break down tasks: Extract → reason → generate improves reliability and auditability.
- Grounding: Supply source snippets; require inline citations near claims. Prefer shorter hops from evidence to claim.
- Output schemas: Define strict JSON or bullet templates to reduce fabrication and ease parsing.
- Controls: Tune `temperature` OR `top_p` (not both). Low for precision, higher for brainstorming.
- Space efficiency: Prefer compact tables, mindful whitespace, and concise examples to fit context windows.
- Chain-of-thought: Don’t elicit private reasoning from models that restrict it; use “show your steps” only where permitted and needed, or request concise reasoning summaries.

## Knowledge check

- Which five components can you combine to make robust prompts, and when do you omit each?
- How does recency bias affect instruction placement, and how do you mitigate it?
- When would you choose few-shot over zero-shot, and what’s the minimal number of examples that help?
- How do `temperature` and `top_p` differ, and why tune only one at a time?
- What schema and grounding strategy will you use to reduce hallucinations in your top task?

## Next steps

- Standardize a prompt template for one critical task, including roles, syntax, grounding, and schema.
- Create 3–5 few-shot exemplars and a short eval set to regression-test changes.
- Define default `temperature`/`top_p` per task type and document in your PRD.
- Add guardrails from Day 6 and telemetry from Day 7 to monitor prompt drift and failures.
