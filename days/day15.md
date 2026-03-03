# Day 15 — Building Your First RAG System (From Scratch)

_Timebox: ~1.5 hours_

## Knowledge goals

- Understand what **RAG (Retrieval-Augmented Generation)** is and why it solves the "LLM doesn't know my data" problem.
- Learn the core components of a RAG pipeline: **loading → chunking → embedding → vector storage → retrieval → generation**.
- Understand key concepts: **embeddings**, **cosine similarity**, **chunking strategies**, and **prompt construction** for grounded answers.
- Explore advanced retrieval techniques: **hybrid search** (BM25 + vector), **reranking**, and **agentic RAG** (ReAct pattern).
- Learn how to **evaluate** RAG quality using retrieval precision, answer faithfulness, and answer relevance.

## Learning materials (≈ 25–30 minutes)

- Read: **RAG From Scratch README** — end-to-end overview of a RAG system built with zero frameworks (no LangChain, no vector DB libraries, no OpenAI SDK). [GitHub](https://github.com/jessieffff/rag-from-scratch)
- Read: **Core Concepts Guide** — beginner-friendly explanations of RAG, embeddings, cosine similarity, chunking, BM25, reranking, and evaluation. [concepts.md](https://github.com/jessieffff/rag-from-scratch/blob/master/docs/concepts.md)
- Read: **How It Works — Codebase Walkthrough** — file-by-file guided tour of the codebase with data flow diagrams. [how_it_works.md](https://github.com/jessieffff/rag-from-scratch/blob/master/docs/how_it_works.md)
- Read: **Agentic RAG Guide** — the ReAct pattern for iterative, self-correcting retrieval. [agentic_rag.md](https://github.com/jessieffff/rag-from-scratch/blob/master/docs/agentic_rag.md)
- Optional: **"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"** — the original RAG paper by Lewis et al. [arXiv](https://arxiv.org/abs/2005.11401)
- Optional: **"ReAct: Synergizing Reasoning and Acting in Language Models"** — the ReAct paper that underpins the agentic retrieval loop. [arXiv](https://arxiv.org/abs/2210.03629)

## Activities (about 50–60 minutes)

### 1) Set up and run the RAG system end-to-end

Clone the repo & run your first query against your own documents:

```bash
# 1. Clone the repo
git clone https://github.com/jessieffff/rag-from-scratch.git
cd rag-from-scratch

# 2. Install dependencies (just 4 packages!)
pip install -r requirements.txt

# 3. Log in to Azure (for Azure AI Foundry embeddings + chat)
az login

# 4. Add your own documents
mkdir sample_data
# Copy some .md, .txt, or .pdf files into sample_data/

# 5. Ask a question — auto-ingests on first run
python cli.py query "What is this about?" --verbose
```

Deliverable: a screenshot or log showing retrieved chunks, similarity scores, and the generated answer.

### 2) Trace the RAG pipeline — understand every step

Walk through the codebase and map each stage to what it does. Fill in this table:

| Stage        | File                  | What it does                                              | Key design decision                                                    |
| ------------ | --------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Load**     | `rag/loader.py`       | Reads PDF / Markdown / web pages → plain text             | "Normalize early" — all downstream code receives the same format       |
| **Chunk**    | `rag/chunker.py`      | Splits text into overlapping pieces                       | Overlap prevents splitting sentences across chunk boundaries           |
| **Embed**    | `rag/embedder.py`     | Converts chunks → 3072-d vectors via Azure AI Foundry API | No SDK — raw HTTP requests so you see every API call                   |
| **Store**    | `rag/vector_store.py` | Stores vectors + metadata; cosine similarity search       | Hand-written math (no numpy); brute-force O(n×d) search                |
| **Retrieve** | `rag/retriever.py`    | Embeds the query, finds top-k similar chunks              | Query MUST use same embedding model as documents                       |
| **Generate** | `rag/generator.py`    | Builds prompt with context + question → streams answer    | System prompt says "answer ONLY from context" to prevent hallucination |

Deliverable: your completed table with any observations (e.g., "I noticed the chunker has 3 strategies and I'd pick sentence-based because…").

### 3) Experiment with search modes and compare results

Run the same question against all three search modes and compare:

```bash
# Semantic search only (default)
python cli.py query "What is the return policy?" --search-mode vector --verbose

# BM25 keyword search only
python cli.py query "What is the return policy?" --search-mode keyword --verbose

# Hybrid search (vector + BM25 + Reciprocal Rank Fusion)
python cli.py query "What is the return policy?" --search-mode hybrid --verbose

# Hybrid + LLM-based reranking (most precise)
python cli.py query "What is the return policy?" --search-mode hybrid --rerank --verbose
```

For each mode, note:

- Which chunks were retrieved (and their scores)
- Whether the answer was accurate and grounded
- How long it took (reranking adds ~20 LLM calls)

Deliverable: a comparison table showing retrieved chunks and answer quality across the 4 modes.

### 4) Run the evaluation framework and interpret results

Use the built-in evaluation to measure RAG quality objectively:

```bash
# Run eval with default vector search
python cli.py eval --verbose

# Compare search modes
python cli.py eval --search-mode hybrid
python cli.py eval --search-mode hybrid --rerank
```

Understand the three metrics:

- **Retrieval Precision** — Did we find the right chunks? (fix: tune chunk_size, overlap, threshold)
- **Answer Faithfulness** — Is the answer grounded in context, not hallucinated? (fix: strengthen system prompt)
- **Answer Relevance** — Does the answer address the question? (fix: improve retrieval + prompt)

Deliverable: a summary of your eval results across modes with one concrete insight (e.g., "Hybrid+Rerank improved faithfulness from 0.71 → 0.82 but is 10× slower").

### 5) Try agentic RAG for a complex question

Use the ReAct agent to see how iterative retrieval handles harder queries:

```bash
# Agentic query — agent iteratively retrieves and reasons
python cli.py agentic-query "What are the side effects of ingredient X?" --verbose

# See the full Thought/Action/Observation trace
python cli.py agentic-query "Compare product A vs B" --verbose
```

Observe the agent's reasoning loop:

1. **Thought** — the agent reasons about what it knows and what's missing
2. **Action** — it chooses `RequestMoreContext`, `ReformulateQuery`, or `Answer`
3. **Observation** — it sees the retrieved chunks and decides whether to iterate

Deliverable: a copy of the agent's reasoning trace for one question, annotated with your observations on when/why it decided to reformulate vs. answer.

## Knowledge check

- **RAG fundamentals:**
  - In your own words, explain why RAG is better than stuffing an entire document into the LLM prompt.
  - What are **embeddings** and why do texts with similar meanings produce similar vectors?
  - Why do we use **cosine similarity** instead of Euclidean distance for comparing embeddings?

- **Pipeline design:**
  - Name the 6 stages of the RAG pipeline in order and explain what each stage does in one sentence.
  - Why is **chunking with overlap** important? What happens if you chunk without overlap?
  - Why must the query be embedded with the **same model** used for documents?

- **Search modes:**
  - Give one example where **vector search** beats keyword search, and one example where **BM25 keyword search** beats vector search.
  - What is **Reciprocal Rank Fusion (RRF)** and why can't you simply add vector scores and BM25 scores?
  - What does the **reranker** do that first-stage retrieval cannot?

- **Evaluation:**
  - Explain the difference between **retrieval precision**, **answer faithfulness**, and **answer relevance**. Which metric catches hallucination?
  - If your system has high precision but low faithfulness, what should you fix?

- **Agentic RAG:**
  - What is the **ReAct pattern** and how does it differ from standard single-pass RAG?
  - Name the 3 actions the agent can take and when each is appropriate.

- **Scenario questions:**
  1. You built a RAG system but the LLM keeps making up facts that aren't in your documents. Which metric is low and what's the fix?
  2. A user asks a complex question requiring info scattered across 3 different documents. Should you use standard RAG or agentic RAG? Why?
  3. Your RAG retrieves the right chunks but the BM25 keyword search keeps missing results. What's likely happening and how does hybrid search help?
