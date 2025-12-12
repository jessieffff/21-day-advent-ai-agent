# Day 6 – Building Trustworthy AI Agents

_Timebox: ~1 hour_

## Knowledge goals

- Understand core safety concepts for agentic systems
- Learn a reusable system message framework (meta prompting → system prompt)
- Identify common threat vectors and mitigation strategies
- Apply human-in-the-loop (HITL) to control and approve agent actions

## Learning materials (≈ 20–25 minutes)

- Read: [**Building Trustworthy AI Agents** (Lesson 06)](https://github.com/microsoft/ai-agents-for-beginners/tree/main/06-building-trustworthy-agents)
  - Safety via robust system prompts and guardrails
  - System message framework: meta prompt → basic prompt → optimized system message → iteration
  - Understanding threats: task/instruction hijack, access to critical systems, service overloading, knowledge base poisoning, cascading errors
  - Human-in-the-loop patterns and example (AutoGen)
  - Additional resources: Responsible AI overview, Evaluation of GenAI apps, Safety system messages, Risk Assessment Template

## Activities (about 30–40 minutes)

### Step 1: Draft Your Meta System Message (10 minutes)
Create a reusable meta system message template your LLM will use to generate concrete system prompts for agents in your project.
- Include fields: company/app name, agent role, responsibilities, constraints, tools, escalation/HITL, tone/style.
- Emphasize structure so outputs are machine-usable (lists, sections, explicit instructions).

Capture this template in `notes/day06_notes.md`.

### Step 2: Write a Basic System Prompt (5 minutes)
Author a concise, plain-English description of one agent (pick a critical agent from your PRD):
- Role and scope, tasks it can perform, responsibilities, and boundaries.
- Keep it short but specific (1–2 paragraphs) focusing on allowed actions and expected outcomes.

Add this draft to `notes/day06_notes.md`.

### Step 3: Generate the Optimized System Message (5 minutes)
Combine your meta system message (as the system instruction) with the basic prompt (as input) to produce a structured, detailed system message for the agent.
- Ensure sections like Objective, Key Responsibilities, User Interaction Instructions, Tone/Style, Tools/Access, Guardrails.
- Make it explicit about approvals, logging, and when to halt or escalate.

Paste the final result into `notes/day06_notes.md`.

### Step 4: Map Threats to Your Agent Design (5–10 minutes)
Using the lesson’s threat list, create a table or bullet list mapping each risk to concrete mitigations in your design:
- Task/Instruction hijack → input validation, content filters, turn limits
- Access to critical systems → least privilege, authN/authZ, secure channels
- Resource/service overloading → rate limits, quotas, backoff/retry
- Knowledge base poisoning → data verification, provenance checks, protected write paths
- Cascading errors → isolation (containers), circuit breakers, fallbacks

Store this mapping in `notes/day06_notes.md`.

### Step 5: Add Human-in-the-Loop Touchpoints (5 minutes)
Define where a human must approve or can terminate:
- Approval gates before sensitive actions (e.g., purchases, data writes)
- Review checkpoints on low-confidence outputs
- Clear termination keywords/signals and logging for audit

Note these checkpoints in your agent’s system message and in `notes/day06_notes.md`.

## Implementation hints

- **System message framework**: Treat meta prompt as a generator of system prompts; iterate versioned prompts to improve reliability.
- **Least privilege**: Scope tool credentials and capabilities per agent; never share broad secrets.
- **Validation**: Add input sanitization and pre-checks before tool calls; enforce schemas for tool I/O.
- **Isolation**: Run risky operations in sandboxes/containers; add circuit breakers and retry policies.
- **Observability**: Log decisions, approvals, and errors; capture provenance of retrieved or generated content.

## Knowledge check

- What sections must your agent’s system message include to promote safety?
- Which threat is most relevant to your PRD and how are you mitigating it?
- Where should HITL approvals happen, and what is the termination condition?
- How will you rate-limit tools and handle retries/fallbacks?
- What data verification or provenance checks are needed for your KB?

## Next steps

- Integrate the optimized system message into your agent code and bind tools with least privilege.
- Implement HITL gating for sensitive actions and add observability.
- Add automated checks for inputs/outputs (schemas, filters) and test failure paths.
- Use the Risk Assessment Template to document impacts and mitigations.
