# Day 3 Notes — Project Planning

**Focus:** translate the product idea into execution-ready artifacts (PRD, plan, repo scaffold).

---

## 1) What I completed today with help from ChatGPT

- Drafted a **PRD** for the “industry news newsletter agent” (scope, MVP flow, requirements).
- Chose an initial **tech stack** and rationale:
  - Web: Next.js + (planned) Tailwind UI layer
  - Backend: FastAPI + LangChain/LangGraph workflow
  - Storage: Cosmos DB
  - Scheduling: Azure Functions timer trigger
  - Email: ACS Email or SendGrid
- Created a **14-day development plan** with one primary focus per day.
- Generated a **GitHub repo scaffold** aligned to the architecture and plan.
- Set up the repo locally and installed dependencies (fixed setup issues as they appeared).
- Wrote supporting docs:
  - `docs/data-model.md`
  - `docs/launch-checklist.md`

---

## 2) What I learned (key takeaways)

- An **agent is only one component** of a complete product. To ship value, the “agent workflow” must be wrapped with:
  - configuration UI (topics/sources/frequency),
  - orchestration (scheduler),
  - storage (history + preferences),
  - delivery (email),
  - observability (debuggability + evaluation).
- AI can accelerate the **first 60%** (structure, templates, scaffolding), but I still need to:
  - verify assumptions,
  - define measurable acceptance criteria,
  - implement reliability + guardrails.

---

## 3) Practical notes: how to write a stronger PRD (what I’ve applied)

### A. Start with “just enough” structure and context
A solid PRD typically includes: project specifics, goals, background/strategy, assumptions, user stories, and success metrics. 

### B. Write user stories in a consistent format
User stories are commonly expressed as **persona + need + purpose** (“As a…, I want…, so that…”). 

### C. Make acceptance criteria testable
Acceptance criteria should be **clear, concise, and testable** (describe outcomes, not implementation).  
**Example (for this product):**
- Given a saved subscription, when I click “Send test,” then I receive an email that contains *N* items and each item includes a valid source URL.

### D. Iterate the PRD like code
Instead of trying to get it perfect in one pass:
- Start with a skeleton (sections + placeholders),
- Fill sections one by one (stories, flows, edge cases),
- Tighten ambiguity (metrics, constraints, non-goals).

### E. Use “review lenses”
Ask for feedback explicitly from different viewpoints:
- Engineering: unclear requirements, missing edge cases, feasibility
- Design: what UI states are implied (loading, errors, empty history)
- QA: what should be tested and what “done” means

---

## 4) Decisions and open questions

### Decisions made
- Build the agent as a **workflow** (gather → dedupe → rank → write → render) rather than a single prompt, to support reliability and future extension.

### Open questions to resolve soon
- What’s the **minimum “sources” feature** for MVP: RSS-only vs RSS + web grounding?
- What’s the best **scheduling model** for v1: daily/weekly only vs cron?
- What’s the **ranking policy**: freshness-first vs source-trust-first vs balanced?

---