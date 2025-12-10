# Workflow Module Reference

**Module:** `newsletter_agent.workflow`  
**Purpose:** Core LangGraph workflow engine for newsletter generation  
**Last Updated:** December 9, 2025

---

## Overview

The workflow module orchestrates the end-to-end newsletter generation process using LangGraph. It defines a three-node sequential pipeline that fetches content, augments it with web search, and generates personalized summaries using Azure OpenAI.

---

## Architecture

### Workflow Graph

```
START
  ↓
[Node 1: Fetch Candidates]
  ↓
[Node 2: Grounded Search]
  ↓
[Node 3: Select & Write]
  ↓
END (Newsletter)
```

### State Machine

The workflow maintains state as a `TypedDict` that flows through each node:

```python
class AgentState(TypedDict, total=False):
    subscription: Subscription      # User preferences & configuration
    candidates: List[Candidate]     # Raw content from all sources
    selected: List[SelectedItem]    # Final curated items
    newsletter: Newsletter          # Rendered HTML + text output
    errors: List[str]               # Non-blocking errors encountered
```

**Key Properties:**
- `total=False`: All fields are optional (nodes incrementally populate state)
- **Immutability:** Each node returns a new state dict (functional paradigm)
- **Error Accumulation:** Errors don't stop execution; they're logged to `errors[]`

---

## Core Components

### 1. LLM Configuration

#### `build_llm() -> AzureChatOpenAI`

Constructs the Azure OpenAI client used for summarization.

**Environment Variables Required:**
- `AZURE_OPENAI_ENDPOINT` (required): Azure OpenAI service endpoint
- `AZURE_OPENAI_API_KEY` (required): API key for authentication
- `AZURE_OPENAI_API_VERSION` (optional): Defaults to `"2024-10-21"`
- `AZURE_OPENAI_DEPLOYMENT` (optional): Defaults to `"gpt-4o-mini"`

**Configuration:**
```python
{
    "temperature": 0.2,      # Low variance for consistency
    "timeout": 45,           # 45-second max per LLM call
}
```

**Design Decision:** Temperature of 0.2 balances creativity with determinism. Higher values could produce less consistent summaries; lower values might be too repetitive.

---

### 2. Node Functions

All nodes follow the same signature:
```python
async def node_*(state: AgentState) -> AgentState:
    # Process state
    # Return updated state dict
```

---

#### **Node 1: `node_fetch_candidates`**

**Purpose:** Gather raw content from multiple sources in parallel

**Inputs:**
- `state["subscription"]`: User configuration

**Outputs:**
- `state["candidates"]`: List of `Candidate` objects
- `state["errors"]`: Any source-specific failures

**Process:**

1. **RSS Feeds** (synchronous)
   - Iterates through `subscription.sources` where `kind == "rss"`
   - Calls `fetch_rss(url, topic_hint)` for each feed
   - Topic hint helps filter/tag RSS items
   - **Error handling:** Appends `"rss:{url}:{error}"` to errors

2. **New York Times API** (async, optional)
   - **Preconditions:** 
     - `NYT_API_KEY` environment variable exists
     - `subscription.topics` is non-empty
   - **Query:** Boolean OR of first 3 topics (e.g., `"AI agents OR LangGraph OR Azure"`)
   - **Limit:** 20 articles
   - **Error handling:** Appends `"nyt:{error}"` to errors

3. **X/Twitter API** (async, optional)
   - **Preconditions:**
     - `X_BEARER_TOKEN` environment variable exists
     - `subscription.topics` is non-empty
   - **Query:** Boolean OR of first 3 topics
   - **Limit:** 20 tweets
   - **Error handling:** Appends `"x:{error}"` to errors

**Error Philosophy:** Best-effort aggregation. If RSS fails but NYT succeeds, the newsletter still generates with NYT content.

**Example State Output:**
```python
{
    "subscription": {...},
    "candidates": [
        Candidate(title="...", url="...", source="TechCrunch RSS", ...),
        Candidate(title="...", url="...", source="NYT", ...),
        # ... 23 total candidates
    ],
    "errors": ["rss:https://broken.feed:ConnectionTimeout"]
}
```

---

#### **Node 2: `node_grounded_search`**

**Purpose:** Augment candidates with fresh web results using Azure AI Foundry

**Inputs:**
- `state["subscription"]`: For topic extraction
- `state["candidates"]`: Existing candidates (may be empty)

**Outputs:**
- `state["candidates"]`: Original + web search results
- `state["errors"]`: Any Foundry-related failures

**Process:**

1. **Early Exit:** If `subscription.topics` is empty, return state unchanged

2. **Check Foundry Configuration:**
   - `FOUNDRY_PROJECT_ENDPOINT`: Azure AI Foundry project URL
   - `FOUNDRY_BING_CONNECTION_ID`: Bing Search connection resource ID

3. **Call Grounding Tool:**
   ```python
   grounded_search_via_foundry(
       query=" OR ".join(topics[:3]),
       freshness="7d",   # Last 7 days only
       count=10          # Max 10 results
   )
   ```

4. **Merge Results:** Appends Foundry results to existing candidates (non-destructive)

**Why Foundry?**
- Bing Search API v7 deprecated (August 2025)
- Foundry provides built-in grounding with citations
- Better integration with Azure AI ecosystem

**Error Handling:** If Foundry fails, node gracefully degrades to RSS/NYT/X content only.

**Example State Output:**
```python
{
    "candidates": [
        # ... original 23 candidates from Node 1
        Candidate(title="...", url="...", source="Web Search", ...),
        # ... 10 more from Foundry
    ],  # Total: 33 candidates
    "errors": []
}
```

---

#### **Node 3: `node_select_and_write`**

**Purpose:** Deduplicate, rank, select, and generate newsletter content

**Inputs:**
- `state["subscription"]`: User preferences (item_count, tone)
- `state["candidates"]`: All aggregated content

**Outputs:**
- `state["selected"]`: Final curated items with LLM-generated summaries
- `state["newsletter"]`: Rendered HTML + text newsletter

**Process:**

##### **Step 1: Deduplication**
```python
candidates = dedupe_candidates(state.get("candidates") or [])
```
- Removes duplicate URLs (case-insensitive comparison)
- Uses SHA-256 hash of normalized URL as deduplication key
- **Why needed:** RSS, NYT, and web search often return same articles

##### **Step 2: Ranking**
```python
ranked = simple_rank(candidates)
```
Heuristic-based scoring (see `ranking.py` for details):
- **+1.0 points:** Has a snippet
- **+0.5 points:** Has topic tags
- **+0.2 points:** Each topic tag matches user's topics

**Example Ranking:**
```
Candidate A: snippet ✓, tags=["AI", "LangGraph"] → 1.0 + 0.5 + 0.4 = 1.9
Candidate B: snippet ✓, tags=[] → 1.0
Candidate C: snippet ✗, tags=["AI"] → 0.5 + 0.2 = 0.7
```

##### **Step 3: Selection**
```python
picked = ranked[:sub.item_count]
```
Takes top N items (e.g., top 8 for `item_count=8`)

##### **Step 4: LLM Summarization**

**System Prompt:**
```
You are an expert newsletter editor.
Given a list of headlines+snippets+links, produce crisp newsletter entries.
Do NOT invent facts. If you lack context, say so briefly.
Always keep the URL exactly as given.
```

**User Prompt Template:**
```
Tone: {subscription.tone}

Create {N} newsletter items. For each, return:
1) why_it_matters (1 sentence)
2) summary (2-3 sentences)

Use the snippets; do not add unverified claims.

Candidates:
- title: {title}
  source: {source}
  url: {url}
  snippet: {snippet}
  published_at: {published_at}
...
```

**LLM Call:**
```python
resp = await llm.ainvoke([sys, prompt])
```
- **Model:** Azure OpenAI GPT-4o-mini
- **Temperature:** 0.2
- **Timeout:** 45 seconds

##### **Step 5: Response Parsing**

The LLM response is parsed using regex to extract structured fields:

```python
def _extract_field(chunk: str, kind: str) -> str | None:
    if kind == "why":
        # Matches: "Why it matters: ..." or "Why: ..."
        pattern = r"why[^:]*:\s*(.+)"
    if kind == "summary":
        # Matches: "Summary: ..." (multiline)
        pattern = r"summary[^:]*:\s*(.+)"
```

**Fallback Behavior:**
- If regex parsing fails for `why_it_matters`: Uses `"Why it matters: (not provided)"`
- If regex parsing fails for `summary`: Uses first 400 chars of LLM response chunk

**Future Enhancement:** Replace regex parsing with OpenAI's [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) for more reliable field extraction.

##### **Step 6: Newsletter Rendering**

```python
subject = f"Your news digest: {', '.join(sub.topics[:2]) or 'Latest'}"
state["newsletter"] = render_newsletter(subject, selected)
```

- Calls `render.py` to generate HTML from Jinja2 template
- Also generates plain text version for email clients without HTML support

**Example Output:**
```python
Newsletter(
    subject="Your news digest: AI agents, LangGraph",
    html="<html>...</html>",
    text="1. LangGraph 0.2 Released\n...",
    items=[...]
)
```

---

### 3. Graph Construction

#### `build_graph() -> CompiledGraph`

Assembles the LangGraph workflow and compiles it with checkpointing support.

**Graph Definition:**
```python
g = StateGraph(AgentState)

# Add nodes
g.add_node("fetch_candidates", node_fetch_candidates)
g.add_node("grounded_search", node_grounded_search)
g.add_node("select_and_write", node_select_and_write)

# Define edges (sequential pipeline)
g.add_edge(START, "fetch_candidates")
g.add_edge("fetch_candidates", "grounded_search")
g.add_edge("grounded_search", "select_and_write")
g.add_edge("select_and_write", END)
```

**Checkpointing:**
```python
cp = InMemorySaver()  # Development only
return g.compile(checkpointer=cp)
```

**Checkpointer Strategy:**
- **Development:** `InMemorySaver` (data lost on restart)
- **Staging/Production:** Replace with:
  - `RedisSaver` for distributed checkpointing
  - `PostgresSaver` for persistent storage
  - `CosmosDBSaver` (custom implementation)

**Why Checkpointing?**
- Enables workflow pause/resume
- Allows human-in-the-loop interventions
- Provides audit trail of state transitions
- Supports workflow versioning (time-travel debugging)

**Thread IDs:** Each subscription gets a unique thread ID: `f"sub:{subscription.id}"`

---

### 4. Execution Entry Point

#### `run_once(subscription: Subscription) -> Newsletter`

Convenience function for one-shot newsletter generation.

**Usage:**
```python
from newsletter_agent.workflow import run_once
from newsletter_agent.types import Subscription

sub = Subscription(
    id="abc123",
    topics=["AI agents", "LangGraph"],
    sources=[{"kind": "rss", "value": "https://blog.langchain.dev/feed"}],
    item_count=8,
    tone="concise, professional"
)

newsletter = await run_once(sub)
print(newsletter.html)  # Rendered HTML
```

**Process:**
1. Builds fresh graph instance
2. Invokes graph with initial state: `{"subscription": subscription}`
3. Uses thread ID: `f"sub:{subscription.id}"` for checkpointing
4. Returns final `newsletter` object from state

**Return Value:**
```python
Newsletter(
    subject: str,
    html: str,
    text: str,
    items: List[SelectedItem]
)
```

---

## Data Flow Example

### Input Subscription
```python
{
    "id": "sub_001",
    "user_id": "user_456",
    "topics": ["AI agents", "LangGraph", "Azure"],
    "sources": [
        {"kind": "rss", "value": "https://blog.langchain.dev/feed"}
    ],
    "item_count": 5,
    "tone": "concise and technical",
    "frequency": "daily"
}
```

### State Transitions

**After Node 1 (Fetch Candidates):**
```python
{
    "subscription": {...},
    "candidates": [
        Candidate(title="LangGraph 0.2 Released", url="...", source="LangChain Blog"),
        Candidate(title="NYT: AI Regulation Update", url="...", source="NYT"),
        Candidate(title="Tweet: Azure AI News", url="...", source="X/Twitter"),
        # ... 18 more candidates
    ],
    "errors": []
}
```

**After Node 2 (Grounded Search):**
```python
{
    "subscription": {...},
    "candidates": [
        # ... original 21 candidates
        Candidate(title="Microsoft Announces...", url="...", source="Web Search"),
        # ... 9 more from Foundry
    ],  # Total: 30 candidates
    "errors": []
}
```

**After Node 3 (Select & Write):**
```python
{
    "subscription": {...},
    "candidates": [...],  # 30 candidates (deduped to 27 unique)
    "selected": [
        SelectedItem(
            title="LangGraph 0.2 Released",
            url="https://blog.langchain.dev/...",
            source="LangChain Blog",
            published_at="2025-12-08T10:00:00Z",
            why_it_matters="Major performance improvements enable 3x faster agent execution.",
            summary="LangGraph 0.2 introduces streaming support, improved error handling..."
        ),
        # ... 4 more items
    ],
    "newsletter": Newsletter(
        subject="Your news digest: AI agents, LangGraph",
        html="<html>...</html>",
        text="1. LangGraph 0.2 Released...",
        items=[...]
    ),
    "errors": []
}
```

---

## Configuration

### Required Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI service URL | `https://myopenai.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | API authentication key | `abc123...` |

### Optional Environment Variables

| Variable | Purpose | Default | Impact if Missing |
|----------|---------|---------|-------------------|
| `AZURE_OPENAI_API_VERSION` | OpenAI API version | `2024-10-21` | Uses default |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name | `gpt-4o-mini` | Uses default |
| `NYT_API_KEY` | NYT article search | N/A | Skips NYT source |
| `X_BEARER_TOKEN` | Twitter API v2 access | N/A | Skips X/Twitter source |
| `FOUNDRY_PROJECT_ENDPOINT` | Azure AI Foundry project | N/A | Skips grounded search |
| `FOUNDRY_BING_CONNECTION_ID` | Bing grounding connection | N/A | Skips grounded search |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Foundry agent model | `gpt-4o-mini` | Uses default |

---

## Error Handling

### Error Accumulation Strategy

**Philosophy:** Non-blocking, best-effort execution

```python
try:
    candidates += fetch_rss(url)
except Exception as e:
    state.setdefault("errors", []).append(f"rss:{url}:{e}")
```

**Benefits:**
- If 1 of 3 RSS feeds fails, 2 still provide content
- Users get newsletters even with partial source failures
- Errors are logged for debugging but don't crash workflow

### Error Format

Errors are stored as strings with structured prefixes:
```
"rss:https://example.com/feed:ConnectionTimeout"
"nyt:Invalid API key"
"foundry:Rate limit exceeded"
```

**Parsing Pattern:**
```python
source, *details = error.split(":", 1)
```

### Monitoring Recommendations

1. **Log all errors** from `state["errors"]` to application insights
2. **Alert on error rate** > 30% for any source
3. **Track source availability** metrics:
   - RSS success rate
   - NYT API quota usage
   - Foundry rate limit proximity

---

## Performance Characteristics

### Latency Breakdown (8-item newsletter)

| Stage | Typical Duration | Max Duration |
|-------|-----------------|--------------|
| Node 1: Fetch Candidates | 5-10s | 20s |
| Node 2: Grounded Search | 3-7s | 15s |
| Node 3: Select & Write | 8-15s | 45s |
| **Total End-to-End** | **16-32s** | **80s** |

### Parallelization Opportunities

**Current:** RSS sources are fetched sequentially  
**Future Optimization:** Use `asyncio.gather()` to fetch RSS in parallel

```python
# Current (sequential)
for s in sub.sources:
    candidates += fetch_rss(s.value)

# Optimized (parallel)
tasks = [fetch_rss(s.value) for s in sub.sources if s.kind == "rss"]
results = await asyncio.gather(*tasks, return_exceptions=True)
```

**Expected Speedup:** 40-60% reduction in Node 1 latency for users with 3+ RSS feeds

### Token Usage (GPT-4o-mini)

**Prompt Tokens (per run):**
- System message: ~50 tokens
- User prompt template: ~100 tokens
- Candidates (8 items × 150 tokens): ~1,200 tokens
- **Total Input:** ~1,350 tokens

**Completion Tokens:**
- Per item (why + summary): ~80 tokens
- 8 items: ~640 tokens

**Total Cost per Run:**
- ~2,000 tokens × $0.150/1M input = $0.0003
- GPT-4o-mini is 15-20× cheaper than GPT-4

---

## Testing

### Unit Testing Strategies

**Mock LLM Responses:**
```python
from unittest.mock import AsyncMock

async def test_node_select_and_write():
    mock_llm = AsyncMock()
    mock_llm.ainvoke.return_value = MockResponse(
        content="Why it matters: Test reason\nSummary: Test summary"
    )
    # Inject mock into node
```

**Test Fixtures:**
```python
@pytest.fixture
def sample_subscription():
    return Subscription(
        id="test_123",
        topics=["test"],
        sources=[],
        item_count=3,
        tone="neutral"
    )

@pytest.fixture
def sample_candidates():
    return [
        Candidate(title="Test 1", url="https://example.com/1", ...),
        Candidate(title="Test 2", url="https://example.com/2", ...),
    ]
```

### Integration Testing

**Test Full Workflow:**
```python
async def test_run_once_integration():
    sub = Subscription(...)
    newsletter = await run_once(sub)
    
    assert newsletter.subject
    assert newsletter.html
    assert len(newsletter.items) <= sub.item_count
```

**Test Error Resilience:**
```python
async def test_partial_source_failure():
    # Configure broken RSS feed
    sub = Subscription(sources=[
        {"kind": "rss", "value": "https://broken.feed"},
        {"kind": "rss", "value": "https://working.feed"}
    ])
    
    newsletter = await run_once(sub)
    assert len(newsletter.items) > 0  # Should still generate content
```

---

## Debugging

### Enable LangGraph Tracing

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your_langsmith_key"
```

**LangSmith Dashboard:** https://smith.langchain.com

### Inspect Intermediate State

```python
graph = build_graph()

# Stream state updates
async for event in graph.astream({"subscription": sub}):
    print(f"Node: {event['node']}")
    print(f"State: {event['state']}")
```

### Print LLM Prompts

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("langchain").setLevel(logging.DEBUG)
```

---

## Future Enhancements

### Short-term (Next Sprint)

1. **Structured LLM Outputs**
   - Replace regex parsing with OpenAI function calling
   - Guarantees valid JSON responses
   ```python
   from langchain.output_parsers import PydanticOutputParser
   parser = PydanticOutputParser(pydantic_object=SelectedItem)
   ```

2. **Parallel RSS Fetching**
   - Use `asyncio.gather()` for concurrent RSS downloads
   - Expected 40-60% speedup for multi-feed subscriptions

3. **Better Error Messages**
   - Include retry counts in error strings
   - Differentiate transient vs. permanent failures

### Medium-term (Next Quarter)

1. **Adaptive Ranking**
   - Learn from user feedback (clicks, engagement)
   - Train lightweight ranking model (scikit-learn)

2. **Persistent Checkpointing**
   - Replace `InMemorySaver` with Redis/Cosmos
   - Enable multi-hour workflows (e.g., weekly digests)

3. **Content Diversity**
   - Ensure selected items span multiple sources
   - Prevent single-source dominance

### Long-term (6+ Months)

1. **Multi-language Support**
   - Translate summaries to user's preferred language
   - Use Azure Translator API

2. **Visual Content**
   - Extract hero images from articles
   - Generate thumbnails in HTML newsletter

3. **Conditional Branching**
   - Add decision nodes (e.g., if candidates < 5, expand search)
   - Use LangGraph's `conditional_edges`

---

## Related Modules

- **`types.py`**: Data model definitions (Subscription, Candidate, Newsletter)
- **`ranking.py`**: Deduplication and ranking algorithms
- **`render.py`**: Jinja2 template rendering
- **`tools/`**: Source-specific fetch functions
  - `rss.py`: RSS/Atom feed parser
  - `nyt.py`: New York Times API client
  - `x_twitter.py`: Twitter API v2 client
  - `foundry_grounding.py`: Azure AI Foundry grounding

---

## References

- **LangGraph Documentation:** https://langchain-ai.github.io/langgraph/
- **Azure OpenAI Service:** https://learn.microsoft.com/azure/ai-services/openai/
- **Azure AI Foundry:** https://learn.microsoft.com/azure/ai-studio/
- **Grounding with Bing Search:** https://learn.microsoft.com/azure/ai-services/agents/grounding-bing-search

---

**Module Maintainer:** Newsletter Agent Team  
**Code Location:** `packages/agent/src/newsletter_agent/workflow.py`  
**Last Reviewed:** December 9, 2025
