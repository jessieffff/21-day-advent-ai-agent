# Observability & Evaluation Plan (Azure Application Insights)

This document captures the **minimum viable** observability plan for `newsletter-agent`, aligned to `docs/obervability.md`, with an implementation approach using **OpenTelemetry (OTel)** exporting to **Azure Application Insights**.

## Goals

- Make every API-triggered run debuggable end-to-end (API request → agent workflow → LLM/tool calls).
- Track core operational metrics: latency, error rate, fallback rate.
- Track cost proxies: tokens (real if available, otherwise estimated).
- Enable an improvement loop: offline eval set + online feedback labels.

Non-goals (v1): full prompt/content logging, complex A/B testing, or a comprehensive evaluation harness.

## Trace Model

### Trace boundary

- **One trace per API request** that triggers a run.
- Inside that trace, create a **child span** for the agent run.

### Span tree (naming)

- `api.request` (created by OTel FastAPI/ASGI instrumentation)
  - `agent.run`
    - `agent.node.fetch_candidates`
      - `tool.call.rss`
      - `tool.call.nyt`
      - `tool.call.x`
    - `agent.node.grounded_search`
      - `tool.call.foundry`
    - `agent.node.select_and_write`
      - `llm.call.generate_newsletter`
    - `agent.summary` (optional, can be merged into `agent.run`)

## Minimum Viable Telemetry Schema

Principles:
- Prefer **low-cardinality** fields.
- Do **not** log raw prompts, full URLs, article text, or user emails.
- Use IDs and counts, plus optional hashes/lengths.

### Required attributes (attach where available)

Attach to `agent.run` and propagate into child spans via context:

- `app.component`: `api|agent|tool`
- `app.env`: `local|dev|prod`
- `request_id`: generated per HTTP request if missing
- `run_id`: newsletter run record ID (when created)
- `subscription_id`
- `user_id`: internal user ID (not email)
- `success`: boolean
- `error_code`: string (stable enum-like)
- `fallback_used`: boolean
- `latency_ms_total`: integer (on `agent.run`)

### Recommended attributes by span type

**Agent node spans** (e.g., `agent.node.fetch_candidates`):
- `node.name`
- `node.latency_ms`
- `error_count`

**Tool spans** (e.g., `tool.call.rss`):
- `tool.name`: `rss|nyt|x|foundry`
- `tool.status`: `ok|error`
- `http.status_code`: if applicable
- `retry.count`: integer
- `items.returned`: integer

**LLM spans** (e.g., `llm.call.generate_newsletter`):
- `llm.provider`
- `llm.model`
- `usage.total_tokens` (if provider returns usage)
- `usage.estimated_tokens` (fallback)
- `llm.status`: `ok|error|fallback`

**Run quality proxies** (attach to `agent.run`):
- `candidate_count`
- `selected_count`
- `duplicate_url_count`

## Success Definition (v1)

A run is considered **successful** if:
- The workflow completes without fatal error, and
- A `newsletter` object is produced (even if fallback), and
- The API returns a 2xx response.

We separately track:
- `fallback_used = true` (newsletter produced but degraded)

## App Insights Setup

### Configuration

Use connection string:

- `APPLICATIONINSIGHTS_CONNECTION_STRING`

Sampling:
- Dev/local: 100% sampling
- Prod: start with head-based sampling (e.g. 10–20%), but keep **errors sampled at 100%** if possible.

## Implementation Checklist

### API (FastAPI)

- Add OTel SDK + FastAPI/ASGI instrumentation.
- Configure App Insights exporter.
- Add middleware to ensure `request_id` exists and is returned in response headers.
- Add per-request log correlation (include `trace_id`, `span_id`, `request_id`).

### Agent (packages/agent)

- Add helper to start spans and attach common attributes.
- Wrap nodes in spans: `fetch_candidates`, `grounded_search`, `select_and_write`.
- Wrap LLM call span inside `generate_newsletter_content`.
- Wrap tool calls (RSS/NYT/X/Foundry) in spans.

## Offline Eval (next)

- Add a small dataset of deterministic cases with mocks.
- Add a runner that checks invariants:
  - no duplicate URLs
  - all selected items have URLs
  - summary length bounds

## Online Feedback (next)

- Add endpoint to attach a label to `run_id`:
  - thumbs up/down
  - optional comment
- Store feedback in Cosmos and attach as attributes when querying traces.
