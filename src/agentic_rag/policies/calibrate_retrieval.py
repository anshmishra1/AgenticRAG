"""Calibrates retrieval_min_top_score / retrieval_strong_top_score against
real, labeled query/document pairs - not a guess, not RAGAS (which measures
generation quality, not retrieval score separation).

IMPORTANT: after the hybrid search + cross-encoder reranking change, the
score this script measures is a cross-encoder relevance score (sigmoid-
activated), NOT raw Pinecone cosine similarity. Re-run this against your
labeled set before trusting the config.py defaults - the old cosine-based
numbers (and even the previous calibration run's numbers) no longer apply,
since the score source itself changed.

Usage:
    1. Ingest the documents you want to calibrate against, as usual (through
       the hybrid-capable index - see scripts/create_hybrid_index.py).
    2. Fill in LABELED_QUERIES below with real questions, the document_id
       each is scoped to, and whether that pairing SHOULD match (True) or
       is a deliberate mismatch (False).
    3. Run: python -m agentic_rag.policies.calibrate_retrieval
    4. It prints the top-score distribution for "should match" vs "should
       not match" pairs, and suggests where the two thresholds should sit
       given the actual gap between the two clusters.

Add more rows over time as you find new failure cases - this script becomes
more trustworthy the more real examples it has, the same way any eval set does.
"""
from __future__ import annotations

from agentic_rag.graph.nodes import calculate_retrieval_metrics
from agentic_rag.ingestion.registry import get_bm25_params
from agentic_rag.retrieval.reranker import rerank
from agentic_rag.retrieval.sparse import load_bm25_json
from agentic_rag.retrieval.vectorstore import retrieve_hybrid_with_scores
from agentic_rag.config import settings

# Fill these in with real (query, document_id, should_match) rows from your
# own ingested documents. document_id comes from GET /documents.
LABELED_QUERIES: list[tuple[str, str, bool]] = [
    # True matches (Strong retrieval score distribution & grounded answer generated)
    ("What problems does the RAG solve", "8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2", True),
    ("How are LLM's built", "8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2", True),
    ("What are the issues with traditional Fine Tuning", "8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2", True),
    ("Why do we still need context engineering if we already have RAG to solve these problems?", "8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2", True),

    # False matches (Failed semantic document grading / graded as irrelevant for this document)
    ("How to generate the dataset that will be used for fine tuning", "8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2", False),
    ("How to create a dataset for fine-tuningmodeloos", "8354069b86193aa9d4c6f88b576443523f00ad68b9637711ad9f801869ffa1b2", False),
]


def _top_score(query: str, document_id: str) -> float:
    content_filter = {"$and": [{"document_id": {"$eq": document_id}}, {"type": {"$eq": "content"}}]}

    bm25_params = get_bm25_params(document_id)
    bm25_encoder = load_bm25_json(bm25_params) if bm25_params else None

    candidates = retrieve_hybrid_with_scores(
        query=query,
        bm25_encoder=bm25_encoder,
        k=settings.hybrid_candidate_k,
        filter=content_filter,
    )
    reranked = rerank(query, candidates, top_k=settings.rerank_top_k_content)
    scores = [score for _, score in reranked]
    return calculate_retrieval_metrics(scores)["top_score"]


def main() -> None:
    if not LABELED_QUERIES:
        print("LABELED_QUERIES is empty. Add real (query, document_id, should_match)")
        print("rows at the top of this script before running.")
        return

    matches, mismatches = [], []
    for query, document_id, should_match in LABELED_QUERIES:
        score = _top_score(query, document_id)
        (matches if should_match else mismatches).append(score)
        print(f"{'MATCH   ' if should_match else 'MISMATCH'} top_score={score:.4f}  {query!r}")

    print()
    if matches:
        print(f"Match scores:    min={min(matches):.4f}  max={max(matches):.4f}  mean={sum(matches)/len(matches):.4f}")
    if mismatches:
        print(f"Mismatch scores: min={min(mismatches):.4f}  max={max(mismatches):.4f}  mean={sum(mismatches)/len(mismatches):.4f}")

    if matches and mismatches:
        floor = (max(mismatches) + min(matches)) / 2
        print(f"\nSuggested retrieval_min_top_score: ~{floor:.2f} (midpoint between the two clusters)")
        print(f"Suggested retrieval_strong_top_score: ~{min(matches):.2f} (lowest observed genuine match)")
    else:
        print("\nNeed at least one match AND one mismatch example to suggest thresholds.")


if __name__ == "__main__":
    main()