# Day 5 – LangGraph Workflows & Agent Patterns

_Timebox: ~1 hour_

## Knowledge goals

- Understand LangGraph concepts for building LLM workflows and agents
- Learn core workflow patterns: Prompt Chaining, Parallelization, Routing, Orchestrator–Worker, Evaluator–Optimizer
- Distinguish when to use workflows vs. agents and how to mix them
- Translate your Day 3 PRD into a concrete LangGraph workflow design

## Learning materials (≈ 20–25 minutes)

- Read: [**LangGraph — Workflows and Agents**](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
  - LLM augmentations: tool calling, structured outputs, short-term memory
  - Prompt chaining: break tasks into verifiable steps
  - Parallelization: run independent subtasks concurrently
  - Routing: send inputs to specialized branches via schema-guided decisions
  - Orchestrator–Worker: plan, dispatch workers, synthesize outputs (dynamic fan-out)
  - Evaluator–Optimizer: iterate until success criteria are met
  - Agents: tool-using, autonomous loops for unpredictable problems

## Activities (about 30–40 minutes)

### Step 1: Extract Requirements From Your PRD (10 minutes)
Use your `day03` PRD to identify:
- Key user flows and success criteria (inputs, outputs, constraints)
- Subtasks/roles (e.g., plan, retrieve, analyze, verify, synthesize)
- Data sources, tools, and structured outputs needed
- Where determinism vs. autonomy is required

Capture these notes in `notes/day05_notes.md` or your PRD doc.

### Step 2: Choose Workflow Pattern(s) (10 minutes)
Map each PRD flow to one or more LangGraph patterns:
- **Prompt Chaining**: linear, verifiable steps (e.g., generate → review → polish)
- **Parallelization**: speed/coverage via concurrent subtasks
- **Routing**: schema-driven branching by request type
- **Orchestrator–Worker**: dynamic fan-out for unknown task counts
- **Evaluator–Optimizer**: quality loops against explicit criteria
- **Agent**: tool-using loop where steps are unpredictable

For each chosen pattern, note why it fits, expected inputs/outputs, and any guardrails.

### Step 3: Sketch the Workflow Graph (10 minutes)
Draft your initial graph design:
- Define `State` keys (inputs, intermediate artifacts, final outputs)
- List `nodes` and their responsibilities
- Specify `edges`: sequential, conditional routes, or parallel fan-out
- Identify augmentations: tools, structured outputs schemas, memory
- Add evaluators or human-in-the-loop checkpoints where needed

Optional: Draw a simple diagram or Mermaid graph reference.

### Step 4: Pseudocode Your Graph (10 minutes)
Write high-level pseudocode aligned with LangGraph primitives:
- `StateGraph(State)` with `START`/`END`
- `add_node(...)` for each step
- `add_edge(...)` for sequential flow
- `add_conditional_edges(...)` for routing/evaluation loops
- `Send(...)` for orchestrator–worker fan-out

Keep it language-agnostic but concrete enough to implement next.

## Implementation hints

- **Structured outputs**: define `pydantic` models to make routing/planning deterministic.
- **Tool calling**: bind tools where the LLM must act (search, calc, retrieve).
- **State design**: keep keys minimal and composable; use shared keys for aggregation.
- **Observability**: add prints/logging or visualize with `get_graph().draw_mermaid_png()`.
- **Guardrails**: add evaluators and conditional edges to catch low-quality outputs.

## Knowledge check

- When would you prefer a workflow over an agent for your PRD?
- Which pattern best handles unknown numbers of subtasks and why?
- How would you use structured outputs to enable reliable routing?
- Where in your PRD would an evaluator–optimizer loop improve quality?
- Identify one tool your agent/workflow must bind and its purpose.

## Next steps

- Implement your sketch using LangGraph APIs based on today’s design.
- Start with the narrowest user flow and expand iteratively.
- Add tests or checkpoints for each node to validate outputs against PRD success criteria.
