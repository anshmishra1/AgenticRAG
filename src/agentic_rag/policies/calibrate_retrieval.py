"""Calibrates retrieval_min_top_score / retrieval_strong_top_score against
real observed similarity scores, instead of guessing.

Why this script and NOT RAGAS: RAGAS metrics (faithfulness, answer relevancy,
context precision/recall) use an LLM judge to score GENERATION quality - they
answer "was this answer good", not "what raw cosine-similarity number should
the retrieval floor be". Picking a numeric threshold is a statistics problem
on scores you already have, not a generation-quality problem. Using RAGAS for
this would mean paying for LLM judge calls to answer a question plain
arithmetic already answers for free. RAGAS's real job is the *separate*
regression-test script (scripts/run_ragas_eval.py) that checks whether a
policy change like this one accidentally hurt answer quality - a genuinely
different question.

Usage:
    Fill in EVAL_SET below with real (document_id, question, is_answerable)
    triples from your own ingested documents - a mix of questions you know
    the document CAN answer and questions you know it CANNOT (e.g. asking
    an Explainable-AI book about LLM scaling laws, as production traffic did).

    python scripts/calibrate_retrieval.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from agentic_rag.policies.retrieval import calculate_retrieval_metrics
from agentic_rag.retrieval.vectorstore import retrieve_with_scores

# ---------------------------------------------------------------------------
# Fill this in with real document_ids from your registry (GET /documents)
# and questions you already know the answer to, one way or the other.
# The two example rows below are taken directly from the production trace
# that surfaced this problem - keep them, they're a real regression case.
# ---------------------------------------------------------------------------
EVAL_SET = [
    # (document_id, question, is_answerable)
    (
        "8b8f659beda18f55ab82191bde2d0d8090ae73925b2c7ea3e8d9171857cc506a",  # Foundation_of_LLMS_TongXiao.pdf
        "What are the scaling laws in large language models?",
        True,
    ),
    (
        "92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21",  # Explainable-AI-for-Practitioners.pdf
        "What are the different types of LLM?",
        False,  # this book doesn't cover LLMs - the actual production failure case
    ),
    # Add more rows here as you find edge cases. Aim for at least 5-10 of
    # each label before trusting the recommended thresholds below.
]


def retrieve_production_candidates(
    document_id: str,
    question: str,
):
    overview_filter = {
        "$and": [
            {"document_id": {"$eq": document_id}},
            {"type": {"$eq": "overview"}},
        ]
    }

    content_filter = {
        "$and": [
            {"document_id": {"$eq": document_id}},
            {"type": {"$eq": "content"}},
        ]
    }

    overview_results = retrieve_with_scores(
        query=question,
        k=2,
        filter=overview_filter,
    )

    content_results = retrieve_with_scores(
        query=question,
        k=5,
        filter=content_filter,
    )

    results = overview_results + content_results

    results.sort(
        key=lambda item: float(item[1]),
        reverse=True,
    )

    return results

def evaluate_candidate_threshold(
    scores: list[tuple[float, bool]],
    threshold: float,
) -> dict:
    tp = fp = tn = fn = 0

    for score, is_answerable in scores:
        predicted = score >= threshold

        if predicted and is_answerable:
            tp += 1
        elif predicted and not is_answerable:
            fp += 1
        elif not predicted and not is_answerable:
            tn += 1
        else:
            fn += 1

    precision = (
        tp / (tp + fp)
        if tp + fp
        else 0.0
    )

    recall = (
        tp / (tp + fn)
        if tp + fn
        else 0.0
    )

    fpr = (
        fp / (fp + tn)
        if fp + tn
        else 0.0
    )

    return {
        "threshold": threshold,
        "precision": precision,
        "recall": recall,
        "false_positive_rate": fpr,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
    }
    
def main() -> None:
    if len(EVAL_SET) < 2:
        print("EVAL_SET is empty or too small. Fill it in with real "
              "(document_id, question, is_answerable) rows before running.")
        return

    answerable_scores: list[float] = []
    unanswerable_scores: list[float] = []

    print("=" * 70)
    print("RETRIEVAL CALIBRATION")
    print("=" * 70)

    for document_id, question, is_answerable in EVAL_SET:
        content_filter = {
            "$and": [
                {"document_id": {"$eq": document_id}},
                {"type": {"$eq": "content"}},
            ]
        }

        results = retrieve_production_candidates(
            document_id,
            question,
        )

        scores = [
            float(score)
            for _, score in results
        ]

        metrics = calculate_retrieval_metrics(scores)

        label = "ANSWERABLE  " if is_answerable else "UNANSWERABLE"
        print(f"\n[{label}] {question}")
        print(f"  top_score={metrics.top_score:.4f}  top_to_mean={metrics.top_to_mean_ratio:.4f}  gap_ratio={metrics.gap_ratio:.4f}")

        (answerable_scores if is_answerable else unanswerable_scores).append(metrics.top_score)

    print("\n" + "=" * 70)
    print("SCORE SEPARATION")
    print("=" * 70)

    if answerable_scores:
        print(f"Answerable   top_score range: {min(answerable_scores):.4f} - {max(answerable_scores):.4f}")
    if unanswerable_scores:
        print(f"Unanswerable top_score range: {min(unanswerable_scores):.4f} - {max(unanswerable_scores):.4f}")

    if answerable_scores and unanswerable_scores:
        floor = max(unanswerable_scores)
        ceiling = min(answerable_scores)
        if floor < ceiling:
            midpoint = (floor + ceiling) / 2
            print(f"\nClean separation. Suggested retrieval_min_top_score: {midpoint:.3f}")
            print(f"(sits between worst answerable {ceiling:.4f} and best unanswerable {floor:.4f})")
        else:
            print(f"\nNo clean separation yet (unanswerable max {floor:.4f} >= "
                  f"answerable min {ceiling:.4f}). Add more eval rows - the "
                  f"current EVAL_SET is too small to calibrate confidently.")
    else:
        print("\nNeed at least one row of each label to suggest a threshold.")


if __name__ == "__main__":
    main()