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
![Product Architecture](images\productArchitecture.png)
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

### A. Start with a “context packet,” not a blank prompt
- Give the AI the essentials upfront: target users, the problem, why now, business goal, constraints (time/tech/legal), and what “success” means.
- Ask it to restate the problem and assumptions first, so you can correct misalignment early.

### B. Use the AI to force clarity on scope (and kill scope creep)
Have it draft: In-scope / Out-of-scope / Non-goals and a short MVP definition. 

### C. Turn fuzzy requirements into testable acceptance criteria
Ask for requirements in the format: User story → acceptance criteria → edge cases.

---

## 4) Decisions and open questions

### Decisions made
- Build the agent as a **workflow** (gather → dedupe → rank → write → render) rather than a single prompt, to support reliability and future extension.

### Open questions to resolve soon
- What’s the **minimum “sources” feature** for MVP: RSS-only vs RSS + web grounding?
- What’s the best **scheduling model** for v1: daily/weekly only vs cron?
- What’s the **ranking policy**: freshness-first vs source-trust-first vs balanced?

---

