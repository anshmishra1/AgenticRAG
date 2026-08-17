# Agentic RAG — Project Reference & Handoff

## 1. Purpose

This document is the current project handoff for the Agentic RAG application.

It describes **what is implemented now**, why the current architecture exists, the problems discovered during optimization, and the next retrieval-optimization direction.

> **Rule:** current source code is authoritative. Historical notes are context only.

---

# 2. Current Project Position

The project is currently an **advanced/corrective RAG foundation**, not yet a full tool-using agent.

The current stack is:

```text
Streamlit
    ↓
FastAPI
    ↓
LangGraph
    ↓
Conversation Policy
    ↓
Dense Retrieval / Pinecone
    ↓
Retrieval Policy
    ↓
Relevance Grading / Query Rewrite
    ↓
Generation
    ↓
Hallucination Check
    ↓
PostgreSQL Checkpointing
```

The immediate engineering goal is **retrieval-quality optimization**, before moving to the later agent/tool phase.

---

# 3. Current End-to-End Architecture

## 3.1 Ingestion path

Ingestion is separate from the query graph.

```text
User uploads PDF
       ↓
FastAPI /ingest
       ↓
Temporary file
       ↓
loaders.py
       ↓
PDF text extraction
       ↓
chunking.py
       ↓
content chunks
       ↓
whole-document overview
       ↓
┌───────────────────────────────┐
│ Pinecone                      │
│ embeddings + chunks + overview│
└───────────────────────────────┘
       ↓
registry.py
       ↓
PostgreSQL document metadata
```

For the current optimization phase, **PDF is the primary supported/validated modality**. Image/audio support exists in the codebase but is intentionally not the current optimization target.

The document registry answers metadata questions such as "what did I upload?" and should not be confused with semantic document retrieval.

---

# 4. Current Query Architecture

```text
                         USER QUESTION
                              │
                              ▼
                    contextualize_question
                              │
                 ┌────────────┴────────────┐
                 │                         │
          first/new question         follow-up
                 │                         │
                 └────────────┬────────────┘
                              ▼
                      retrieval_query
                              │
                              ▼
                         retrieve
                              │
                              ▼
                    assess_retrieval
                              │
                ┌─────────────┼─────────────┐
                │             │             │
               LOW       AMBIGUOUS        HIGH
                │             │             │
                ▼             ▼             ▼
             rewrite       grade         generate
                │             │             │
                │       ┌─────┴─────┐       │
                │       │           │       │
                │    relevant   irrelevant  │
                │       │           │       │
                │       ▼           ▼       │
                │    generate    rewrite    │
                │       │           │       │
                └───────┴───────────┘       │
                                            ▼
                                       generation
                                            │
                                            ▼
                                    refusal detection
                                            │
                                  ┌─────────┴─────────┐
                                  │                   │
                               refusal           factual answer
                                  │                   │
                                  ▼                   ▼
                               record        hallucination check
                                                      │
                                            ┌─────────┴─────────┐
                                            │                   │
                                         grounded          hallucinated
                                            │                   │
                                            ▼                   ▼
                                         record              retry
```

### Important state separation

```text
question
```

is the original user request and must remain intact.

```text
retrieval_query
```

is the search-oriented query produced by contextualization/rewrite.

This prevents retrieval optimization from destroying user instructions such as:

```text
"Explain this in detail and give examples."
```

---

# 5. Current Policy Architecture

The policy layer was introduced to prevent routing logic from being scattered across `nodes.py`.

```text
policies/
├── conversation.py
├── retrieval.py
└── generation.py
```

## `conversation.py`

Responsible for deterministic conversation-level decisions such as:

- control/termination messages;
- likely follow-up detection;
- query-intent classification.

The actual contextualization LLM call remains in the graph node.

## `retrieval.py`

Currently contains the three-way retrieval evidence gate:

```text
LOW
AMBIGUOUS
HIGH
```

The earlier approach relied heavily on Pinecone/bi-encoder score thresholds and relative score shape.

That approach is now considered a temporary foundation rather than the final retrieval architecture.

## `generation.py`

Owns generation-related policies such as:

- refusal detection;
- context limits;
- history limits.

A refusal should not be sent through the hallucination checker as though it were a factual answer.

---

# 6. What We Learned From Runtime Traces

The timing/trace instrumentation exposed several important behaviors.

### 6.1 Dense retrieval is the major latency contributor

Repeated Pinecone retrieval calls were commonly around 2–3+ seconds during development, and corrective retries multiplied this cost.

Therefore the optimization target is not simply "make the LLM faster".

### 6.2 Bi-encoder similarity has thin margins

Dense retrieval embeds query and documents independently. Similarity scores can be close even when one candidate is meaningfully better than another.

This produced cases where:

```text
high absolute similarity
+
small candidate separation
```

was difficult to classify reliably.

### 6.3 Relative thresholds became a tuning exercise

The previous policy used combinations of:

```text
absolute top-score floor
+
top/mean ratio
+
score-gap ratio
+
overview margin
```

This helped expose retrieval behavior but did not provide a robust long-term relevance signal.

The project therefore moves away from continuously tuning those values.

### 6.4 Relevance grading produced false negatives

Some retrieved passages were semantically relevant but were classified as `irrelevant` by the LLM grader.

This caused unnecessary:

```text
rewrite → retrieve → grade → retrieve ...
```

loops.

### 6.5 Query rewriting can produce malformed search queries

Runtime traces showed malformed rewrites such as concatenated technical terms.

Therefore query rewriting needs validation, not blind reinsertion into retrieval.

### 6.6 Grounded does not mean answered

An answer such as:

```text
I don't know.
```

can be correctly classified as grounded because it introduces no unsupported factual claim.

Therefore:

```text
grounded ≠ successful answer
```

The system must distinguish answer faithfulness from answerability/retrieval success.

---

# 7. Why We Are Changing Retrieval Architecture

The previous dense-only architecture was:

```text
Query
  ↓
Embedding
  ↓
Pinecone
  ↓
Cosine similarity
  ↓
Threshold policy
```

The next architecture is deliberately multi-stage:

```text
Query
  ↓
Dense retrieval ───────────┐
                           │
Sparse BM25 retrieval ─────┤
                           ▼
                     RRF fusion
                           │
                           ▼
                 Cross-encoder reranker
                           │
                           ▼
                    final evidence
                           │
                    retrieval policy
```

Each component has a distinct responsibility.

| Component | Responsibility |
|---|---|
| Pinecone dense retrieval | Semantic recall |
| BM25 | Lexical/keyword recall |
| RRF | Combine independent ranking signals without mixing incompatible score scales |
| Cross-encoder | Precise query–passage relevance modelling |
| LLM grader | Expensive semantic tie-breaker for genuinely ambiguous evidence |
| Query rewrite | Correct failed retrieval attempts |

---

# 8. Planned Hybrid Retrieval Architecture

## 8.1 Dense retrieval

Pinecone remains the cloud vector store.

It continues to provide semantic candidate retrieval and document scoping through `document_id`.

## 8.2 BM25

BM25 will be a **local sparse retrieval index**, not a PostgreSQL search service.

The corpus will be derived from the ingested PDF chunks.

Conceptually:

```text
PDF chunks
   ↓
local persistent corpus/index
   ↓
BM25
```

PostgreSQL remains responsible for application/checkpoint/document-registry concerns rather than being forced into the BM25 retrieval path.

## 8.3 Reciprocal Rank Fusion

Dense and BM25 scores exist on different scales and therefore should not simply be added.

RRF will combine their **rank positions** instead.

Conceptually:

```text
Dense ranking ─────┐
                   ├── RRF ──> fused candidates
BM25 ranking ──────┘
```

This avoids another arbitrary weighted-score calibration exercise.

## 8.4 Cross-encoder reranking

The fused candidate set will be reranked with a local cross-encoder such as:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Unlike the dense bi-encoder, a cross-encoder receives:

```text
(query, candidate passage)
```

as a pair and directly models their interaction.

The cross-encoder will run locally and can use the user's RTX 3060 GPU.

The GPU is therefore used for a computationally intensive but bounded local task, while LLM generation and cloud vector infrastructure remain provider/API based.

---

# 9. Target Retrieval Flow

```text
                         QUERY
                           │
                           ▼
                   contextualization
                           │
                           ▼
              ┌────────────────────────┐
              │ Candidate generation  │
              └───────────┬────────────┘
                          │
               ┌──────────┴──────────┐
               ▼                     ▼
       Pinecone / Dense           BM25 / Sparse
          top-N candidates          top-N candidates
               │                     │
               └──────────┬──────────┘
                          ▼
                     RRF fusion
                          │
                    fused top-N
                          │
                          ▼
                 Cross-encoder GPU
                          │
                          ▼
                  reranked top-K
                          │
                          ▼
                 retrieval assessment
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
           rewrite       grade      generate
```

The important principle is:

> **First maximize candidate recall, then maximize evidence precision.**

Dense and BM25 search are candidate generators. The cross-encoder is the precision stage.

---

# 10. Why We Are Not Using PostgreSQL for BM25

PostgreSQL already has legitimate responsibilities:

```text
LangGraph checkpoints
Document registry
Application metadata
```

BM25 fundamentally requires an inverted text index.

For the current project scale, a local persistent BM25 index is simpler and avoids introducing a second database responsibility.

The intended architecture is therefore:

```text
Pinecone → dense retrieval / cloud
BM25     → local sparse retrieval
GPU      → local cross-encoder reranking
LLM APIs → generation / grading / rewriting
Postgres → checkpoint + registry
```

---

# 11. GPU Strategy

The development machine has:

```text
NVIDIA GeForce RTX 3060
12 GB VRAM
```

The planned GPU workload is the local cross-encoder reranker.

The design deliberately does **not** move the whole application onto the local GPU.

This preserves scalability:

```text
Cloud/API:
  LLM inference
  Pinecone

Local GPU:
  bounded reranking workload
```

If the application is later deployed to infrastructure without a GPU, the reranker should support CPU fallback.

---

# 12. Expected Code Changes for Retrieval Upgrade

The planned implementation is incremental.

### New retrieval modules

```text
src/agentic_rag/retrieval/
├── vectorstore.py       existing dense retrieval
├── bm25.py              new sparse retrieval
├── fusion.py            new RRF implementation
├── reranker.py          new cross-encoder implementation
└── hybrid.py            new retrieval orchestrator
```

### Existing components expected to change later

```text
config.py
ingestion/pipeline.py
ingestion/registry.py / local corpus storage
retrieval/vectorstore.py
retrieval policy
RAGState
nodes.py
tests
```

The graph topology should remain largely unchanged.

The goal is to replace the **retrieval implementation**, not redesign LangGraph again.

---

# 13. Evaluation Strategy

Evaluation will compare retrieval architectures rather than tuning one score threshold forever.

The intended comparison is:

```text
A. Dense only
B. Dense + BM25
C. Dense + BM25 + RRF
D. Dense + BM25 + RRF + Cross-encoder
```

Metrics should include:

### Retrieval

- recall@K;
- precision@K;
- ranking quality;
- candidate recovery from lexical queries;
- cross-encoder ranking quality.

### RAG answer quality

RAGAS can later evaluate:

- faithfulness;
- answer relevancy;
- context precision;
- context recall.

### System performance

Track:

- dense retrieval latency;
- BM25 latency;
- RRF latency;
- reranker latency;
- LLM latency;
- total request latency;
- number of retrieval retries;
- number of LLM calls.

RAGAS is therefore an **evaluation layer**, not a replacement for retrieval itself.

---

# 14. Current vs Target Architecture

| Area | Current | Target |
|---|---|---|
| Semantic retrieval | Pinecone dense | Pinecone dense |
| Sparse retrieval | Not implemented | Local BM25 |
| Candidate fusion | Dense ranking only | RRF |
| Reranking | None | Cross-encoder |
| Reranker execution | N/A | RTX 3060 GPU with CPU fallback |
| Relevance policy | Bi-encoder score heuristics | Reranked evidence + policy |
| LLM grader | Used for ambiguous cases | Retained as expensive tie-breaker |
| Query rewrite | Corrective loop | Corrective loop + validation |
| Conversation policy | Implemented | Retain/refine |
| Generation policy | Implemented | Retain/refine |
| Hallucination check | Implemented | Retain/refine |
| Evaluation | RAGAS harness exists | Retrieval + RAGAS evaluation |
| PostgreSQL | Checkpoint + registry | Same responsibilities |

---

# 15. Important Architectural Rules Going Forward

1. **Do not redesign the LangGraph topology unless a concrete failure requires it.**
2. **Do not keep tuning Pinecone similarity thresholds as the primary retrieval solution.**
3. **Do not mix dense and BM25 scores directly. Use rank fusion.**
4. **Do not make BM25 depend on PostgreSQL unless scale later requires it.**
5. **Do not call the cross-encoder once per entire document corpus. Rerank only a bounded candidate set.**
6. **Do not load the cross-encoder for every request. Load it once and reuse it.**
7. **Do not send every query to the expensive LLM grader. Use reranking to narrow the ambiguity.**
8. **Do not allow malformed rewritten queries directly back into retrieval.**
9. **Do not treat `grounded` as equivalent to `answered`.**
10. **Do not modify multiple major retrieval components at once without an isolated test.**

---

# 16. Immediate Development Order

```text
CURRENT BASELINE
      │
      ▼
1. Build local BM25 corpus/index
      │
      ▼
2. Test BM25 independently
      │
      ▼
3. Keep Pinecone unchanged
      │
      ▼
4. Implement RRF
      │
      ▼
5. Test dense vs BM25 vs RRF
      │
      ▼
6. Add cross-encoder
      │
      ▼
7. Test CPU/GPU reranking + latency
      │
      ▼
8. Integrate hybrid retrieval into retrieve()
      │
      ▼
9. Update RAGState / trace
      │
      ▼
10. Replace old bi-encoder confidence policy
      │
      ▼
11. Re-evaluate grading + rewriting
      │
      ▼
12. Run retrieval evaluation + RAGAS
      │
      ▼
13. Optimize remaining bottlenecks
```

No BM25, RRF, or cross-encoder implementation should be considered complete until its isolated tests pass.

---

# 17. Later Agentic Phase

Once retrieval quality is stable, the project can continue toward true Agentic RAG:

```text
User
  ↓
Agent
  ├── RAG tool
  ├── Web search
  ├── Calculator
  ├── Document metadata
  └── Future MCP tools
```

The agent should select tools conditionally and inspect tool results before answering.

MCP should be introduced after ordinary tool calling is understood and stable.

---

# 18. Development Commands

### FastAPI

```powershell
uvicorn agentic_rag.api.main:app --reload
```

### Streamlit

```powershell
streamlit run app/streamlit_app.py
```

### Health

```text
http://127.0.0.1:8000/health
```

---

# 19. Handoff Summary

**The project currently has a stable corrective-RAG foundation built around FastAPI, Streamlit, LangGraph, Pinecone, provider-based LLM inference, PostgreSQL checkpointing, document registry, conversation policies, retrieval policies, generation policies, relevance grading, query rewriting, grounded generation, hallucination checking, and performance tracing. The major retrieval weakness is the reliance on dense bi-encoder similarity as both retrieval and relevance signal. Rather than continuing to tune thresholds, the next optimization is a true multi-stage retrieval architecture: Pinecone dense retrieval + local BM25 sparse retrieval → RRF fusion → local GPU cross-encoder reranking → retrieval assessment. PostgreSQL remains for checkpointing/registry, while cloud APIs remain responsible for LLM inference. The LangGraph topology should remain stable while the retrieval subsystem is upgraded incrementally and evaluated at every stage.**

---

# 20. Golden Rule

> **Do not rebuild what already works. Improve one layer at a time, measure it, and preserve the working graph architecture.**
