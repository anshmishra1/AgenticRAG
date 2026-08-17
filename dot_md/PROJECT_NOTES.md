# Agentic RAG — Current Architecture Notes

This is the concise architecture/reference companion to `PROJECT.md`.

## Current request flow

```text
User question
    ↓
contextualize_question
    ↓
retrieval_query
    ↓
retrieve
    ↓
retrieval policy
    ├── low       → rewrite_query → retrieve
    ├── ambiguous → grade_documents
    │                  ├── relevant   → generate
    │                  └── irrelevant → rewrite_query
    └── high      → generate
    ↓
generation policy / refusal detection
    ↓
check_hallucination
    ├── grounded       → record_turn
    └── hallucinated   → corrective generation/retry
    ↓
END
```

The current graph is deliberately retained. The upcoming retrieval work changes the retrieval subsystem, not the overall LangGraph topology.

## Ingestion flow

```text
Upload
  ↓
load PDF
  ↓
recursive chunking
  ↓
whole-document overview
  ↓
Pinecone
  ├── embeddings
  ├── content chunks
  └── overview
  ↓
PostgreSQL document registry
```

PDF is the immediate optimization target. Image/audio support is intentionally deferred.

## Policy layer

```text
policies/
├── conversation.py
├── retrieval.py
└── generation.py
```

### Conversation policy

Handles deterministic conversation decisions such as control messages, likely follow-ups, and query intent. The contextualization LLM call remains in the graph node.

### Retrieval policy

Currently provides a three-way evidence decision:

```text
LOW → rewrite
AMBIGUOUS → LLM grade
HIGH → generate
```

This was introduced to avoid blindly trusting dense retrieval scores. It is now considered a transitional policy because the next retrieval architecture will provide a stronger relevance signal.

### Generation policy

Owns refusal detection and generation context/history limits. A refusal should not be sent through the hallucination checker as if it were a factual answer.

## Current retrieval

Current validated retrieval is dense Pinecone retrieval with document scoping and overview/content handling. MMR/diversity behavior may exist depending on the exact current `vectorstore.py`; source code remains authoritative.

The previous confidence approach relied on combinations of dense similarity thresholds and relative score-shape heuristics. Runtime traces showed that these scores can have thin margins and are not a robust final relevance signal.

## Retrieval problems established from runtime evidence

1. Dense bi-encoder scores can be close for candidates with different actual relevance.
2. Broad/document-level queries can underuse the overview evidence.
3. The LLM relevance grader has produced false-negative relevance decisions.
4. Query rewriting can produce malformed search strings and therefore needs validation.
5. Corrective retrieval retries add repeated retrieval latency.
6. `grounded` only establishes answer faithfulness to supplied context; it does not prove that the retrieved context was the best context for the question.

## Next retrieval architecture

The project is moving to a true multi-stage retrieval system:

```text
Query
  │
  ├──────────────→ Pinecone dense retrieval
  │
  └──────────────→ local BM25 sparse retrieval
                         │
                         ▼
                   RRF rank fusion
                         │
                         ▼
                bounded candidate set
                         │
                         ▼
             Cross-encoder reranking
                 (RTX 3060 GPU)
                         │
                         ▼
                   final evidence
                         │
                         ▼
                 retrieval policy
```

### Responsibilities

| Component | Responsibility |
|---|---|
| Pinecone | Semantic candidate recall |
| BM25 | Lexical candidate recall |
| RRF | Rank fusion without incompatible score arithmetic |
| Cross-encoder | Query–passage relevance precision |
| LLM grader | Expensive tie-breaker for remaining ambiguity |
| Query rewrite | Corrective retrieval |

## BM25 storage decision

BM25 will **not** be implemented as a PostgreSQL search service.

PostgreSQL remains responsible for:

- LangGraph checkpoints;
- document registry/application metadata.

The sparse retrieval corpus/index will be local and persistent, with document scoping. This avoids introducing another database responsibility for the current project scale.

## GPU decision

Development hardware:

```text
NVIDIA GeForce RTX 3060
12 GB VRAM
```

The local GPU will be used primarily for cross-encoder reranking. LLM inference and Pinecone remain API/cloud based, preserving scalability and avoiding dependence on the development machine for generation.

The reranker should support CPU fallback for deployment environments without a GPU.

## Planned retrieval modules

```text
src/agentic_rag/retrieval/
├── vectorstore.py
├── bm25.py
├── fusion.py
├── reranker.py
└── hybrid.py
```

These modules should be implemented incrementally and tested independently before graph integration.

## Planned evaluation

Compare:

```text
A. Dense only
B. Dense + BM25
C. Dense + BM25 + RRF
D. Dense + BM25 + RRF + Cross-encoder
```

Measure:

- retrieval recall/precision;
- ranking quality;
- retrieval latency;
- reranking latency;
- total request latency;
- LLM calls/retries;
- RAGAS faithfulness/relevancy/context precision/context recall.

RAGAS is an evaluation layer, not the retrieval mechanism.

## Immediate implementation order

```text
1. Local persistent BM25 corpus/index
2. Independent BM25 tests
3. RRF implementation
4. Dense vs BM25 vs RRF evaluation
5. Cross-encoder implementation
6. GPU/CPU reranker test
7. Hybrid retrieval integration
8. State + trace updates
9. Replace old dense-score confidence policy
10. Re-evaluate grader and rewrite behavior
11. Retrieval + RAGAS evaluation
12. Remaining performance optimization
```

## Architectural rules

- Do not redesign the LangGraph topology without evidence.
- Do not keep tuning dense-only thresholds as the primary retrieval solution.
- Do not directly add dense and BM25 scores; use rank fusion.
- Do not use PostgreSQL as the BM25 index unless future scale requires it.
- Do not rerank the entire corpus; rerank a bounded candidate set.
- Load the cross-encoder once and reuse it.
- Keep expensive LLM grading for genuinely ambiguous cases.
- Validate rewritten queries before sending them back to retrieval.
- Treat `grounded` and `answered` as separate concepts.
- Implement and test one retrieval layer at a time.
