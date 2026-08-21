# Agentic RAG — Project Reference & Handoff

**Last updated:** 2026-08-21

> Current source code is authoritative if it conflicts with historical notes.
> This document records the latest stable architecture, completed optimization work, current problems, and next implementation plan.

---

## 1. Project Position

The project is currently a **Corrective / Advanced RAG system**, not yet a true tool-using agent.

Development progression:

```text
Basic RAG
    ↓
Production-style RAG
    ↓
Corrective / Advanced RAG        ← CURRENT
    ↓
Tool-enabled Agentic RAG
    ↓
Advanced Agentic System
```

The future agentic layer will use the existing RAG capability as a tool rather than replacing it.

---

## 2. Current Architecture

```text
User
  ↓
Streamlit
  ↓
FastAPI
  ↓
PostgreSQL checkpoint
  ↓
LangGraph
  ↓
contextualize_question
  ↓
retrieve
  │
  ├── Dense retrieval
  └── BM25 / sparse retrieval
          ↓
        RRF
          ↓
  logical candidate deduplication
          ↓
  cross-encoder reranking
          ↓
  retrieval assessment
      │       │       │
    strong  unsure   weak
      │       │       │
      ▼       ▼       ▼
   generate grade   rewrite
              │       │
              │       └──→ retrieve
              ▼
          generation
              ↓
     hallucination check
              ↓
       final / correction
```

The final generation-correction branch is currently the next major optimization.

---

## 3. Stable Retrieval Baseline

The retrieval architecture now uses:

```text
Dense + BM25
     ↓
RRF
     ↓
logical candidate deduplication
     ↓
cross-encoder reranking
     ↓
retrieval assessment
```

### Document scoping

Every document receives a deterministic SHA-256 `document_id`.

The ID is propagated through:

- ingestion metadata;
- Pinecone metadata;
- LangGraph state;
- `/ingest`;
- `/query`;
- Streamlit active-document state.

This prevents unrelated uploaded documents from entering the active document's retrieval space.

### RRF

Dense and BM25 results are fused with Reciprocal Rank Fusion because their raw score scales are not directly comparable.

Diagnostics preserve:

```text
dense rank / score
BM25 rank / score
RRF score
```

### Cross-encoder

Current model:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

The reranker receives `(query, passage)` pairs and preserves:

```text
_retrieval_rrf_score
_cross_encoder_logit
_cross_encoder_score
_reranker_previous_rank
```

---

## 4. Retrieval Efficiency Optimization — COMPLETED

The first retrieval optimization pass has been implemented and validated.

### Previous execution

```text
query
 ├── overview retrieval → embed query
 └── content retrieval  → embed query AGAIN

overview → reranker
content  → reranker
```

### Current execution

```text
query
  ↓
build query representation ONCE
  ├── dense vector
  └── sparse/BM25 vector
  ↓
parallel overview + content retrieval
  ↓
deduplication
  ↓
ONE batched cross-encoder inference
  ↓
final ranking
```

Also implemented:

- GPU-aware cross-encoder execution;
- cross-encoder startup warm-up;
- preserved RRF/cross-encoder diagnostics;
- no changes to Streamlit for retrieval optimization.

The retrieval path is now the **baseline**. Do not keep redesigning it without evidence.

---

## 5. Latest Performance Finding

The latest application run showed approximately:

```text
retrieve                7.82 sec
grade_documents         1.74 sec
generate               14.83 sec
check_hallucination     2.60 sec
TOTAL                  ~27.00 sec
```

Therefore:

> **Generation/correction orchestration is now the primary optimization target.**

The retrieval optimization should be considered successful enough to freeze temporarily.

---

## 6. Retrieval Assessment

The current assessment uses a three-way decision:

```text
strong evidence
    → generate

ambiguous evidence
    → LLM relevance grading

weak evidence
    → rewrite / re-retrieve
```

This is intended to avoid expensive relevance grading when retrieval evidence is already strong.

### Important rule

Do not keep adding arbitrary score thresholds.

Cross-encoder scores are different from the old vector-similarity scale, so any future calibration must be based on the current retrieval path and an evaluation dataset.

The long-term direction is **calibrated/adaptive routing**, not endless manual threshold tuning.

---

## 7. Current Generation / Hallucination Problem

The current hallucination routing effectively behaves like:

```text
generate
   ↓
hallucination check
   ↓
grounded → END

hallucinated
   ↓
generate AGAIN
   ↓
hallucination check AGAIN
```

The problem is that regeneration often uses essentially the same:

- question;
- evidence;
- generation strategy.

Therefore a failed generation can simply fail again while consuming another expensive LLM call.

This is now the major architecture issue to solve.

---

## 8. Planned Generation-Correction Architecture

We will replace blind regeneration with an **evidence-correction loop**.

Target:

```text
retrieve
   ↓
assess evidence
   ↓
generate
   ↓
grounding assessment
   │
   ├── grounded
   │      ↓
   │     END
   │
   └── not grounded
          ↓
      diagnose failure
          │
      ┌───┴────────────────┐
      │                    │
unsupported claim   insufficient evidence
      │                    │
      ▼                    ▼
targeted             rewrite + re-retrieve
regeneration              │
      │                    │
      └─────────┬──────────┘
                ▼
          final verification
                ↓
               END
```

### Key principle

The grounding checker should answer:

> **What failed?**

not only:

> **Did it fail?**

Potential diagnoses:

```text
grounded
unsupported_claims
insufficient_evidence
contradiction
```

Different diagnoses should cause different graph actions.

---

## 9. Structured Grounding Assessment — NEXT IMPLEMENTATION

The hallucination check should eventually return structured information such as:

```text
verdict
unsupported_claims
explanation
```

Example:

```json
{
  "verdict": "unsupported_claims",
  "unsupported_claims": [
    "The model uses only one loss function."
  ],
  "explanation": "The retrieved context does not support this claim."
}
```

This gives the graph actionable feedback and makes the system more white-box.

---

## 10. Targeted Regeneration

Instead of:

```text
"Try again."
```

the corrective generation should receive the failure diagnosis:

```text
The previous answer contained unsupported claims.

Rewrite the answer using only claims supported by the supplied context.

If the context does not establish an answer, explicitly say so.
```

This means generation attempt #2 is actually different from attempt #1.

---

## 11. Retrieval Failure vs Generation Failure

These must remain separate.

### Retrieval failure

```text
retrieve
  ↓
evidence insufficient
  ↓
rewrite query
  ↓
retrieve again
```

### Generation failure

```text
retrieve
  ↓
good evidence
  ↓
generate
  ↓
unsupported claim
  ↓
targeted regeneration
```

A good retrieval result should not be discarded merely because the generator overclaimed.

---

## 12. Correction Budget

The graph should have a bounded correction budget.

Desired maximum:

```text
Normal:
generation
+
grounding check

Corrective:
generation
+
grounding check
+
one corrective action
+
one final verification
```

Avoid:

```text
generate → check → generate → check → ...
```

This protects:

- latency;
- API cost;
- token usage;
- provider quotas;
- user experience.

---

## 13. Refusal Handling

A genuine refusal such as:

```text
I don't know.
```

should not enter hallucination verification.

The generation policy already uses refusal-pattern matching plus a length cap to distinguish genuine refusals from substantive answers that merely begin with uncertainty.

Important distinction:

```text
grounded refusal
```

means:

> The answer itself did not make unsupported claims.

It does **not** mean:

> The user's question was successfully answered.

---

## 14. Cost / Latency Optimization Principle

Every optimization must aim for:

```text
LLM calls          ↓
Token usage        ↓
Latency            ↓ or unchanged
Retrieval quality  ≥ baseline
Answer quality     ≥ baseline
Groundedness       ≥ baseline
```

Preferred order:

```text
avoid unnecessary work
        ↓
make necessary work cheaper
        ↓
make remaining waiting visible
```

Do not optimize a computation that can first be avoided.

---

## 15. Provider Layer

Current provider abstraction supports:

```text
Groq
Cerebras
NVIDIA
OpenRouter
Bedrock (prepared/optional)
```

Provider order is configuration-driven.

Provider reliability belongs in the provider abstraction:

```text
provider selection
      ↓
timeout
      ↓
retry
      ↓
fallback
      ↓
latency/error diagnostics
```

Do not scatter provider-specific timeout/fallback logic across graph nodes.

---

## 16. Evaluation Strategy

Offline evaluation remains separate from the live query path.

RAGAS can evaluate:

- faithfulness;
- answer relevancy;
- context precision;
- context recall.

Retrieval-specific evaluation should also use:

```text
Recall@K
MRR
nDCG
```

The evaluation set should contain:

- factual questions;
- conceptual questions;
- broad document questions;
- follow-ups;
- weak/out-of-context questions;
- cases where dense and lexical retrieval disagree.

The evaluation dataset should become the basis for future routing calibration.

---

## 17. Current Optimization Roadmap

```text
COMPLETED
│
├── document-scoped retrieval                 ✅
├── Dense + BM25                              ✅
├── RRF                                       ✅
├── cross-encoder reranking                   ✅
├── query representation reuse                ✅
├── parallel retrieval                       ✅
├── batched cross-encoder inference           ✅
├── GPU-aware reranker                        ✅
└── reranker warm-up                          ✅
│
▼
CURRENT
│
├── structured grounding diagnosis            🔧
├── targeted regeneration                     🔧
├── insufficient-evidence recovery            🔧
├── bounded correction budget                 🔧
└── generation latency/cost optimization     🔧
│
▼
NEXT
│
├── RAGAS regression evaluation               🔧
├── retrieval metric calibration              🔧
├── adaptive retrieval decisions              🔧
├── provider timeout/fallback hardening       🔧
├── fast-vs-quality model separation          🔧
├── caching                                   🔧
└── adaptive retrieval depth                  🔧
│
▼
AFTER STABLE RAG
│
├── RAG as a tool
├── calculator
├── web search
├── LLM tool selection
├── tool execution loop
└── tool-result reasoning
│
▼
LATER
│
├── multi-step planning
├── stronger memory
├── agent evaluation
├── agent tracing
└── MCP
```

---

## 18. What We Are NOT Doing Right Now

Do not:

- redesign ingestion;
- modify PDF chunking without evidence;
- change stored Pinecone vectors to solve generation problems;
- redesign hybrid retrieval again;
- add more arbitrary thresholds;
- add multiple LLM judges without measurement;
- create uncontrolled regeneration loops;
- add tools before the RAG baseline is stable;
- add MCP merely for complexity;
- modify multiple unrelated pipeline layers in one debugging pass.

---

## 19. Development Rules

1. Current source code is authoritative.
2. Preserve the working ingestion pipeline.
3. Preserve the optimized retrieval baseline.
4. Measure before changing retrieval parameters.
5. Keep expensive LLM operations conditional.
6. Keep correction loops bounded.
7. Preserve structured diagnostics.
8. Treat refusal and groundedness as different concepts.
9. A grounded answer is not automatically a correct answer.
10. Ask for permission before directly modifying repository files.
11. Prefer complete updated files when an implementation change is approved.
12. Do not rebuild what already works.

---

## 20. Interview-Level Project Description

> This is a cost-aware corrective RAG system built with LangGraph. It uses document-scoped hybrid dense and BM25 retrieval, RRF fusion, logical candidate deduplication, and local cross-encoder reranking. Retrieval evidence is assessed before expensive LLM grading, allowing strong evidence to bypass unnecessary grading and weak evidence to trigger corrective retrieval. The system maintains persistent conversation state through PostgreSQL and exposes the workflow through FastAPI with a Streamlit conversational frontend. The current optimization focus is replacing blind hallucination-driven regeneration with structured grounding diagnosis and targeted corrective actions. Once the RAG baseline is stable and evaluated, the retrieval capability will become a tool inside a larger Agentic RAG workflow.

---

## 21. Latest Handoff — 2026-08-21

### Stable

```text
FastAPI                         ✅
Streamlit                       ✅
PostgreSQL checkpointing        ✅
Document registry               ✅
Document-scoped retrieval       ✅
Dense retrieval                 ✅
BM25 retrieval                  ✅
RRF                             ✅
Candidate deduplication         ✅
Cross-encoder reranking         ✅
Query embedding reuse           ✅
Parallel retrieval              ✅
Batched reranking               ✅
GPU-aware reranking             ✅
Reranker warm-up                ✅
Retrieval assessment            ✅
Conditional relevance grading   ✅
Query rewriting                 ✅
Grounded generation             ✅
Hallucination checking         ✅
```

### Current work

```text
Generation correction loop
Structured grounding diagnosis
Targeted regeneration
Insufficient-evidence recovery
Bounded correction budget
Generation latency optimization
```

### Future

```text
Evaluation/calibration
Provider reliability
Caching
Adaptive retrieval
RAG as tool
Calculator
Web search
Tool selection
Tool execution
MCP
Advanced agentic behavior
```

---

# Golden Rule

> **Do not rebuild what already works.**

The current RAG subsystem is the foundation of the future agent.

The next question is:

> **How do we make the existing RAG reliable, measurable, cost-effective, and useful enough to serve as a capability inside an agent?**
