# Day 1 Notes – AI Foundations & Agent Basics

## Key Concepts Learned

### Agents vs. Chatbots vs. Chains
_Your one-paragraph definition:_

An AI agent is an autonomous system that perceives its environment, makes decisions based on observations, and takes actions (including tool calls) to achieve goals—iterating until completion. A chatbot is a reactive conversational interface that responds to user input without persistent goals or tool use. A chain is a deterministic sequence of predefined steps that executes a fixed workflow. Agents differ because they possess agency: they can reason about multiple solution paths, call tools dynamically based on task requirements, adapt to intermediate results, and iterate toward objectives without human intervention at each step.

### The Perceive–Decide–Act Loop
_Sketch and annotate where tools are called:_
sss
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PERCEIVE: Agent observes the environment & user input     │
│  • Read current state (task, context, available tools)     │
│  • Gather information                                      │
│                        ↓                                    │
│  DECIDE: LLM reasons about the situation                   │
│  • Analyze what's needed to progress                       │
│  • Determine next action(s)                                │
│  • [TOOL CALLS HAPPEN HERE] ← Select & format tools        │
│  • Process tool outputs                                    │
│                        ↓                                    │
│  ACT: Execute the decision                                 │
│  • Invoke selected tools (API calls, searches, etc.)       │
│  • Update environment state                                │
│                        ↓                                    │
│  FEEDBACK LOOP: Check if goal is achieved                  │
│  • If goal met → Return result                             │
│  • If not → Loop back to PERCEIVE (now with new state)     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key insight:** Tool calls are the bridge between decision and action—they give agents the power to interact with the real world beyond pure reasoning.

## Real-World Task Analysis

### Tasks Well-Suited for Agents (3–5 examples)
1. **Research & synthesis**: "Find recent news on AI safety, summarize key themes, and identify trends" (multiple searches, filtering, integration)
2. **Multi-step debugging**: "Fix this error in my code" (read files, run tests, search docs, iterate based on output)
3. **Data analysis with decisions**: "Analyze my sales data, identify the bottom 10% of products, and recommend actions" (query, compute, reason)
4. **Booking/scheduling**: "Find available flights matching my criteria and book the cheapest one" (search, compare, validate, execute)
5. **Content generation with research**: "Write a blog post on quantum computing using recent papers" (search, read, synthesize, write)

### Tasks Better Handled by Simple Chain/RAG (3 examples)
1. **FAQ/straightforward Q&A**: "What is the return policy?" (retrieve from docs, return answer—no reasoning/iteration needed)
2. **Static content generation**: "Generate a haiku about winter" (pure generation task, no tools or context-gathering required)
3. **Document summarization**: "Summarize this PDF" (read source, apply transformation, return—no multi-step decisions or tool switching)

## Backlog & Skill Priorities

_Skills to emphasize in this 21-day journey:_
- [x] Tool use (how to design & integrate tools effectively)
- [x] Evaluation (testing agents & measuring success)
- [x] Deployment (moving agents from dev to production)
- [x] Multi-agent coordination (when & how to split work)
- [x] Safety & reliability (error handling, guardrails)

## Knowledge Check Answers

### Why use an agent instead of a plain chat or RAG chain?

Agents enable **autonomous problem-solving**. While a chatbot answers one question at a time and a RAG chain retrieves + returns info, an agent can reason about multi-step workflows, dynamically choose which tools to use, handle failures gracefully, and iterate toward a goal. Agents shine when:
- The solution path isn't predetermined (must decide what to do based on intermediate results)
- Multiple tools may be needed in sequence
- The task requires reasoning, validation, or error recovery
- You want the system to be goal-driven rather than reactive

### Perceive–Decide–Act Loop & Tool Calls

The loop is **Perceive** (sense environment + goal) → **Decide** (LLM reasons what action helps) → **Act** (execute tools) → **Feedback** (loop until goal reached).

**Tool calls** happen in the Decide phase: the LLM examines available tools, determines which one(s) help progress, formats the call with parameters, and executes it. The tool's output becomes new perception for the next iteration. This closes the loop: each tool output refines the agent's understanding and informs the next decision.

### Example Comparison
- **Reactive agent task:** "Help me troubleshoot my laptop" — agent observes symptoms → decides to check system logs → reads output → iterates based on findings. Needs multiple tool calls & decisions based on results.
- **Plan-and-execute task:** "Book a flight matching my criteria and show me alternatives" — agent can plan the sequence (search → filter → validate → book) upfront, then execute the plan. More structured.

**Bonus note:** Plan-and-execute is a specific agent pattern; the raw perceive–decide–act applies to both reactive and planned agents.

## Additional Insights & Questions

**Key Takeaways:**
- Agents are powerful precisely because they can iterate—they don't need a pre-scripted path.
- The distinction between agent patterns (reactive, plan-and-execute, multi-agent) matters for design—choose based on task complexity & predictability.
- Tool design is critical: agents are only as good as the tools available to them.

**To revisit:**
- How to design tools that are robust & trustworthy for agents?
- What are the latency/cost tradeoffs of multiple tool calls?
- How do we evaluate agent reliability vs. simple chains?
