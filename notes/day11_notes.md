# Day 11 Notes — Agent Skills: From Tools to Workflows

What Is an Agent Skill
--------------------------------------------------

An **Agent Skill** is a structured bundle stored in the repository that may include:
- Step‑by‑step instructions
- Examples
- Scripts
- Templates and resources

Core properties:
- **Multi‑step**: represents a complete workflow, not a single action
- **Opinionated**: encodes best practices and preferred structure
- **Deterministic**: aims for consistent outputs given similar inputs
- **Versioned**: evolves alongside the codebase

Agent Skills are intentionally *not*:
- Simple prompts
- A new execution runtime
- A replacement for tools or models

Instead, they sit **above tools** and guide how tools are used together.

Why Agent Skills Exist
--------------------------------------------------

As agent workflows grow more complex, relying on prompts and ad‑hoc tool calls becomes brittle.

Common failure modes before Agent Skills:
- Workflow logic scattered across long prompts
- Important process knowledge living as tribal knowledge
- Inconsistent execution across similar tasks
- Tools available, but no shared understanding of *how* to use them together

Agent Skills address these problems by introducing:
- **Repository‑scoped workflows** that live with the code
- **On‑demand loading**, so only relevant skills consume context
- **Explicit process definition**, not just tool availability

Key distinction:
> Tools define what an agent *can* do.  
> Skills define how an agent *should* do it.

--------------------------------------------------
Function Calling vs MCP vs Agent Skills
--------------------------------------------------

These concepts operate at different layers and solve different problems.

### Function Calling

Purpose:
- Execute a **single, well‑defined action**

Characteristics:
- Atomic and stateless
- Execution‑focused
- Defined and controlled by the host application

Best suited for:
- Clear, bounded operations (e.g., extract text, fetch data, rank items)

---

### MCP (Model Context Protocol)

Purpose:
- Standardize **how tools and data are exposed and discovered** by agents

Characteristics:
- Client–server architecture
- Tool discovery and schema‑driven access
- Enables scalable, multi‑tool systems

MCP answers the question:
> Where do tools come from, and how does an agent access them consistently?

---

### Agent Skills

Purpose:
- Encode **end‑to‑end workflows** that combine reasoning, tools, and structure

Characteristics:
- Multi‑step and procedural
- May rely on function calls or MCP‑provided tools
- Optimized for correctness, consistency, and reuse

Agent Skills answer the question:
> When this task appears, what is the *correct process* to follow?

--------------------------------------------------
How They Fit Together
--------------------------------------------------

A useful mental model is a layered stack:

Agent Skill (workflow / SOP)
    ↓
MCP (tool exposure and discovery)
    ↓
Function Calls (execution)

Important implications:
- Skills orchestrate behavior
- MCP enables scale and reuse
- Function calls perform the actual work

--------------------------------------------------
Concrete Example: note-to-video-transcript Skill
--------------------------------------------------

This project introduces a new Agent Skill: **note‑to‑video‑transcript**.

### Why this is a Skill

The task is not a single action. It requires a repeatable process:
- Detect input format (Markdown vs PDF)
- Extract and normalize content
- Build a structured outline
- Generate a spoken‑language transcript
- Apply quality and length checks

Encoding this logic as a skill ensures the process is applied consistently every time.

### What the Skill Defines

The skill specifies:
- **Activation conditions** (requests mentioning notes, PDFs, transcripts, or video scripts)
- **Processing steps** (detect → normalize → outline → generate → validate)
- **Output contract** (Title, Hook, Intro, Sections, Recap, CTA)
- **Quality constraints** (coverage, duration tolerance, minimal repetition)

Individual tools such as PDF extraction or text rewriting are implementation details; the skill defines how they fit together.

Key Takeaways
--------------------------------------------------

- Function calls handle **execution**
- MCP handles **integration and discovery**
- Agent Skills handle **workflow definition and consistency**

Robust agent systems treat workflows as first‑class assets, not just collections of tools.

--------------------------------------------------
Reflection Questions
--------------------------------------------------

- Which parts of your current agent logic are tools versus workflow knowledge?
- Where is process logic still embedded in prompts instead of skills?
- What other recurring workflows in the project deserve to become Agent Skills?

---