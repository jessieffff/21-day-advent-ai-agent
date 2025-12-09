# Day 4 – AI Agent Orchestration Patterns

_Timebox: ~1 hour_

## Knowledge goals

- Understand the core benefits of multi-agent systems vs. single-agent approaches
- Learn the 5 fundamental orchestration patterns: Sequential, Concurrent, Group Chat, Handoff, and Magentic
- Know when to use each pattern and when to avoid it
- Recognize implementation considerations and design trade-offs

## Learning materials (≈ 20–25 minutes)

- Read: [**Microsoft Learn — AI Agent Orchestration Patterns**](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
  - Overview: benefits of multi-agent architecture (specialization, scalability, maintainability, optimization)
  - Sequential Orchestration: linear pipelines with clear dependencies
  - Concurrent Orchestration: parallel agents for independent analysis
  - Group Chat Orchestration: collaborative decision-making and validation
  - Handoff Orchestration: dynamic delegation between specialized agents
  - Magentic Orchestration: planning and iterating on complex open-ended problems
  - Implementation considerations: context windows, reliability, security, observability

## Activities (about 30 minutes)

### Step 1: Compare the 5 Patterns (10 minutes)
Create a comparison table with these patterns:
1. **Sequential** — Agents hand off work in a predefined order
2. **Concurrent** — Multiple agents run in parallel on the same task
3. **Group Chat** — Agents collaborate through shared discussion
4. **Handoff** — Dynamic routing based on context/expertise
5. **Magentic** — Manager agent builds and refines plans iteratively

For each, note:
- **When to use** (the ideal scenario)
- **When to avoid** (the pitfalls)
- **One real-world example**

### Step 2: Map a Use Case (10 minutes)
Pick a complex task from your domain (e.g., document review, customer support, incident response, content creation, data analysis). For this task:
- Identify 3–5 specialized sub-tasks or roles needed
- Decide which pattern(s) would work best: Sequential? Concurrent? Handoff? A combination?
- Sketch how agents would interact and what context flows between them
- Note any reliability or security concerns (timeouts, error handling, data privacy)

### Step 3: Identify an Anti-Pattern (10 minutes)
Read through the "Common pitfalls" section in the Microsoft article. Choose one anti-pattern and:
- Describe what goes wrong when you apply the wrong pattern
- Sketch how you would redesign to avoid it
- Capture notes in `notes/day04_notes.md`

## Knowledge check

- In your words: why use multiple agents instead of one large agent with many tools?
- Give one scenario each where Sequential and Concurrent orchestration are the right choice.
- What does the "Handoff" pattern solve that Sequential cannot?
- When would you combine multiple patterns in a single application?
