"""Retrieval confidence policy.

The retrieval pipeline now uses:

    Dense + BM25
        ↓
       RRF
        ↓
Cross-encoder reranking
        ↓
retrieval assessment

The cross-encoder sigmoid score is NOT treated as a calibrated probability.
It is primarily used for ranking.

Confidence therefore combines:
    1. top-vs-second separation
    2. top-vs-mean separation
    3. minimum ranking evidence
    4. retry state
    5. overview/content evidence where available

The policy deliberately avoids treating the old Pinecone cosine-score
thresholds as valid for the new cross-encoder score distribution.
"""

from __future__ import annotations

from agentic_rag.config import settings


def assess_retrieval_confidence(
    metrics: dict,
    top_doc_type: str | None,
    overview_top_score: float | None,
    content_top_score: float | None,
    retry_count: int = 0,
) -> dict:
    """Classify retrieved evidence as strong, ambiguous, or weak.

    Returns:
        {
            "decision": "generate" | "grade" | "rewrite_query",
            "evidence_strength": "strong" | "ambiguous" | "weak",
            "reason": str,
        }

    Important:
        Cross-encoder sigmoid scores are ranking signals, not calibrated
        probabilities. Therefore absolute CE thresholds are deliberately
        not used as the primary decision mechanism.
    """

    top_score = float(metrics.get("top_score", 0.0))
    second_score = float(metrics.get("second_score", 0.0))
    mean_score = float(metrics.get("mean_score", 0.0))

    top_to_mean = float(
        metrics.get("top_to_mean_ratio", 0.0)
    )
    gap_ratio = float(
        metrics.get("gap_ratio", 0.0)
    )

    score_gap = top_score - second_score

    # ---------------------------------------------------------
    # 1. No usable retrieval evidence
    # ---------------------------------------------------------
    if top_score <= 0.0 or not metrics:
        if retry_count >= settings.max_retries:
            return {
                "decision": "grade",
                "evidence_strength": "weak",
                "reason": "no_usable_retrieval_evidence_retries_exhausted",
            }

        return {
            "decision": "rewrite_query",
            "evidence_strength": "weak",
            "reason": "no_usable_retrieval_evidence",
        }

    # ---------------------------------------------------------
    # 2. Very weak distribution
    #
    # The top result is not sufficiently separated from the
    # remaining candidates.
    # ---------------------------------------------------------
    weak_distribution = (
        top_to_mean < settings.retrieval_top_to_mean_ratio
        and gap_ratio < settings.retrieval_gap_ratio
    )

    if weak_distribution:
        if retry_count >= settings.max_retries:
            return {
                "decision": "grade",
                "evidence_strength": "weak",
                "reason": "weak_distribution_retries_exhausted",
            }

        return {
            "decision": "rewrite_query",
            "evidence_strength": "weak",
            "reason": "weak_candidate_separation",
        }

    # ---------------------------------------------------------
    # 3. Strong evidence
    #
    # We require BOTH:
    #
    #   - meaningful top-vs-mean separation
    #   - meaningful top-vs-second separation
    #
    # This prevents one tiny numerical difference from being
    # interpreted as strong evidence.
    # ---------------------------------------------------------
    strong_distribution = (
        top_to_mean >= settings.retrieval_top_to_mean_ratio
        and gap_ratio >= settings.retrieval_gap_ratio
    )

    if strong_distribution:
        return {
            "decision": "generate",
            "evidence_strength": "strong",
            "reason": "strong_cross_encoder_score_distribution",
        }

    # ---------------------------------------------------------
    # 4. Overview evidence
    #
    # An overview chunk can legitimately answer broad document-level
    # questions even if individual content chunks have weaker scores.
    # ---------------------------------------------------------
    overview_dominant = (
        top_doc_type == "overview"
        and overview_top_score is not None
        and content_top_score is not None
        and overview_top_score
        >= content_top_score
        * (1.0 + settings.retrieval_overview_margin)
    )

    if overview_dominant and gap_ratio >= settings.retrieval_gap_ratio:
        return {
            "decision": "generate",
            "evidence_strength": "strong",
            "reason": "overview_dominant_with_clear_margin",
        }

    # ---------------------------------------------------------
    # 5. Ambiguous evidence
    #
    # The retrieval has signal, but not enough confidence to
    # bypass semantic grading.
    # ---------------------------------------------------------
    if gap_ratio < settings.retrieval_gap_ratio:
        reason = "top_candidates_too_close"
    elif top_to_mean < settings.retrieval_top_to_mean_ratio:
        reason = "weak_top_candidate_separation"
    else:
        reason = "retrieval_requires_semantic_grading"

    return {
        "decision": "grade",
        "evidence_strength": "ambiguous",
        "reason": reason,
    }