# Day 7 Notes — AI Agents in Production: Observability & Evaluation

Reference lesson: https://github.com/microsoft/ai-agents-for-beginners/tree/main/10-ai-agents-production

These notes distill the lesson into actionable guidance, aligned with `days/day07.md`.

## Step 1: Define “Success” for One Agent

Core idea: meaningful evaluation starts with a clear definition of success.

- Define success up front: what outcome should the agent reliably produce?
- Decide what to label/score: pass/fail, accuracy proxy, user satisfaction, task completion.
- Tie success to measurable signals:
  - **Accuracy/desirability**: correctness, relevance, policy compliance
  - **Reliability**: consistent behavior, no loops
  - **Operational health**: low error rate, acceptable latency/cost

Why it matters: in production, observability underpins diagnosis, trust, and improvement.

### Action Items for `newsletter-agent`:

#### What to capture (minimum)
- A stable run outcome label and a concise set of reasons for failure or degradation.

#### Implementation
- Define v1 success criteria (pass/fail + degraded-but-successful).
- Define stable `error_code` values (enum-like strings) for common failure modes.
- Attach run-level attributes to `agent.run` spans:
  - `success` (boolean)
  - `fallback_used` (boolean)
  - `error_code` (string)
  - `latency_ms_total` (integer)

- Success definition (v1): workflow completes, a `newsletter` object is produced (even if fallback), and the API returns 2xx.
- Attach to `agent.run`: `success` (boolean), `fallback_used` (boolean), `error_code` (stable string enum).

#### What to look for in App Insights
- Filter traces where `success=false` to find failures.
- Filter traces where `fallback_used=true` to identify degraded-but-successful runs.

## Step 2: Observability Events & Fields (Telemetry Schema)

### Core Concepts (from the lesson)

- **Trace**: complete agent run end-to-end (e.g., handling one user query).
- **Span**: individual step inside the trace (e.g., an LLM call, retrieval, tool call).
- Observability turns agents from black boxes into glass boxes by making steps, timing, costs, and failures visible.

### Why Observability Matters in Production

- **Debugging & root-cause analysis**: traces pinpoint failures in multi-step workflows.
- **Latency & cost management**: measure slow/expensive steps to optimize prompts, models, or workflows.
- **Trust, safety, compliance**: keep an audit trail of decisions/actions; detect prompt injection, harmful output, or PII mishandling.
- **Continuous improvement loop**: production insights inform offline test sets and changes.

### Key Metrics to Track (lesson list)

- **Latency**: total run + per-step timing; identify bottlenecks.
- **Costs**: cost per run; token usage; number of calls; unexpected spikes.
- **Request errors**: API/tool failures; support retries/fallbacks (e.g., provider A → provider B).
- **User feedback (explicit)**: ratings (thumbs/stars) and comments.
- **User feedback (implicit)**: rephrases, retries, repeated questions, aborts.
- **Accuracy/success rate**: define success, then label traces succeeded/failed.
- **Automated evaluation metrics**:
  - Use LLM-as-a-judge to score helpfulness/accuracy.
  - Use task-specific tools (e.g., RAG evaluation libraries like RAGAS; safety tooling such as LLM Guard) where relevant.

### Instrumentation Approaches

- **OpenTelemetry (OTel)**: emerging standard for LLM observability; generate/export telemetry.
- **Instrumentation wrappers**: libraries that automatically capture spans for agent frameworks.
- **Manual spans**: add custom spans and attributes/tags for business context.
  - Example attributes: `user_id`, `session_id`, `model_version`.

### Action Items for `newsletter-agent`:

#### What to capture (minimum)
- Run context (IDs + environment), outcome labels, and a few quality/cost proxies.
- Tool and LLM spans with status, latency, and usage.

#### Implementation checklist
- Create a single telemetry context helper that provides common attributes (reused across nodes/tools/LLM calls).
- Ensure run-level attributes are attached on `agent.run`:
  - `app.env`, `app.component`, `request_id`, `run_id`, `subscription_id`, `user_id`
  - `success`, `error_code`, `fallback_used`, `latency_ms_total`
  - Quality proxies: `candidate_count`, `selected_count`, `duplicate_url_count`

- Ensure span-level attributes are attached consistently:
  - Tool calls (e.g., `tool.call.rss`): `tool.name`, `tool.status`, `retry.count`, `items.returned`, `http.status_code`
  - LLM call (e.g., `llm.call.generate_newsletter`): `llm.provider`, `llm.model`, `usage.total_tokens` (or `usage.estimated_tokens`), `llm.status`

Privacy callout (what I will not log):
- Raw prompts, full URLs, article text, or user emails.

## Step 3: Map Spans to Your Agent Workflow

Think in trace trees: one trace per request, with spans for each meaningful step.

Typical span categories:
- LLM calls (planning, drafting, judging)
- Retrieval steps (search/RAG)
- Tool calls (API, DB, file, browser)
- Safety checks/policy filters
- Retries/fallbacks

Why: consistent span naming and structure make dashboards and regression detection possible.

### Action Items for `newsletter-agent`:

#### What to capture (minimum)
- One trace per API request.
- Child spans for each agent node and each tool/LLM call.
- Consistent naming so you can compare traces across versions.

#### Implementation checklist
- Adopt a canonical span naming convention (copy/pasteable constants help).
- Wrap each major workflow node in a span:
  - `agent.node.fetch_candidates`
  - `agent.node.grounded_search`
  - `agent.node.select_and_write`
- Wrap each tool call (RSS/NYT/X/Foundry) in a span with status and returned counts.
- Wrap the newsletter drafting model call in `llm.call.generate_newsletter`.

Span naming planned:
- `api.request`
  - `agent.run`
    - `agent.node.fetch_candidates`
      - `tool.call.rss`
      - `tool.call.nyt`
      - `tool.call.x`
    - `agent.node.grounded_search`
      - `tool.call.foundry`
    - `agent.node.select_and_write`
      - `llm.call.generate_newsletter`

#### What to look for in App Insights
- Bottleneck step: the span with the largest duration.
- Failure isolation: the first span with `tool.status=error` or `llm.status=error`.

## Step 4: Build an Offline Eval Set

### Offline Evaluation (lesson summary)

- Evaluate the agent in a controlled setting using test datasets.
- Benefits:
  - Repeatable; suitable for CI/CD regression tests
  - Clearer accuracy metrics when you have ground truth
- Challenge:
  - Test sets can become stale; the agent may face different real-world queries
- Practical guidance:
  - Maintain a mix of small smoke tests (fast checks) and larger eval sets (broad coverage)
  - Keep adding new edge cases informed by production failures

### Recommended Evaluation Loop

The lesson’s loop:

`evaluate offline → deploy → monitor online → collect new failure cases → add to offline dataset → refine → repeat`

### Action Items for `newsletter-agent`:

#### Implementation checklist
- Add a tiny deterministic dataset (5–20 cases) with mocked tools.
- Build an eval runner that executes the agent workflow and checks invariants.
- Wire it into CI as a fast smoke eval (separate from slower, larger evals).

Initial invariants (from `notes/observability-appinsights-plan.md`):
- No duplicate URLs
- All selected items have URLs
- Summary length within bounds

How it connects back to observability:
- When a production trace shows `duplicate_url_count > 0` or frequent fallbacks, add that scenario to the offline eval set.

## Step 5: Design an Online Feedback Loop

### Online Evaluation (lesson summary)

- Evaluate the agent in the live environment on real user interactions.
- Benefits:
  - Captures unexpected real-world queries
  - Detects model drift (performance changes over time as inputs shift)
- Common techniques:
  - Track success rate, satisfaction, and operational metrics on real traffic
  - Collect explicit and implicit feedback
  - Consider shadow testing/A/B testing to compare agent versions
- Challenge:
  - Live labels can be noisy; rely on user feedback or downstream behaviors

### Common Production Issues (and how observability helps)

- Inconsistent task performance: refine prompts/objectives; consider decomposing tasks.
- Continuous loops: define termination conditions; consider a stronger reasoning model for planning.
- Tool calls failing: validate tools outside the agent; refine tool definitions/parameters.
- Multi-agent inconsistency: make roles distinct; use a router/controller agent.

### Cost Management Strategies (lesson list)

- Use smaller models (SLMs) for simpler steps; reserve larger models for complex reasoning.
- Use a router model to choose the right model by request complexity.
- Cache responses for common requests (optionally classify similarity before running the full agent).

### Action Items for `newsletter-agent`:

#### What to capture (minimum)
- `run_id`-keyed feedback records.
- A small label taxonomy (thumbs up/down + optional free-text comment).

#### Implementation checklist
- Add a feedback endpoint that accepts: `run_id`, `label`, optional `comment`.
- Persist feedback (Cosmos or your DB of record).
- Ensure traces carry `run_id` so you can join feedback → trace.
- Add a lightweight quality dashboard query:
  - Bad runs by label
  - Bad runs by `error_code`
  - Bad runs by `fallback_used=true`

How I plan to implement it (next step):
- Add an endpoint to attach a label (thumbs up/down + optional comment) to `run_id`.
- Store feedback and use `run_id` to join feedback → traces when investigating bad newsletters.

#### What to look for in App Insights
- Filter by `run_id` from a user report/feedback record and jump straight to the trace.

## Notes / Links

- Lesson: https://github.com/microsoft/ai-agents-for-beginners/tree/main/10-ai-agents-production
- Example notebook: https://github.com/microsoft/ai-agents-for-beginners/blob/main/10-ai-agents-production/code_samples/10_autogen_evaluation.ipynb

---


