"""Retrieval confidence policy.

Replaces the old binary check (strong -> skip grading / else -> grade) with a
three-way gate:

  1. Below an ABSOLUTE score floor  -> weak.    Skip grading, go straight to
     query rewrite. No point asking an LLM to grade context we're already
     confident is unrelated to the question.
  2. Above the floor AND a confident relative shape -> strong. Skip grading,
     go straight to generation.
  3. Everything in between -> ambiguous. Defer to the LLM grader - this is
     exactly where a cheap heuristic is least reliable, so don't trust it here.

Why an absolute floor was missing before, and why that mattered: the old
check only looked at RELATIVE shape (top-to-mean ratio, gap ratio). Six
uniformly weak, barely-related scores can still produce a "confident-looking"
ratio purely because they're not identical to each other - there's nothing in
a relative-only check that can tell "these are strong matches" apart from
"these are six weak matches where one happens to be less weak than the rest."
A real production trace caught this exactly: a query against the wrong
document returned scores of [0.23, 0.17, 0.15, 0.15, 0.13, -0.06] and was
still classified "strong" by the old logic, because the ratios looked fine.

The absolute thresholds below (retrieval_min_top_score=0.35,
retrieval_strong_top_score=0.55) are calibrated from that trace's real score
clusters: genuine matches scored 0.55-0.63, genuine mismatches scored
0.04-0.23. Treat these as a starting point backed by one real trace, not a
rigorous calibration - see scripts/calibrate_retrieval.py to refine them
against a larger labeled set.
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
    """Returns {"decision": ..., "evidence_strength": ..., "reason": ...}.

    decision is one of "generate" | "grade" | "rewrite_query".
    retry_count guards against the weak-evidence branch looping forever:
    once max_retries is hit, weak evidence falls through to "grade" (the LLM
    gets one last say) instead of rewriting indefinitely.
    """
    top_score = metrics["top_score"]
    top_to_mean = metrics["top_to_mean_ratio"]
    gap_ratio = metrics["gap_ratio"]

    overview_dominant = (
        top_doc_type == "overview"
        and overview_top_score is not None
        and content_top_score is not None
        and overview_top_score >= content_top_score * (1.0 + settings.retrieval_overview_margin)
    )

    # 1. Absolute floor - checked first, regardless of relative shape.
    if top_score < settings.retrieval_min_top_score:
        if retry_count >= settings.max_retries:
            return {
                "decision": "grade",
                "evidence_strength": "weak",
                "reason": "weak_evidence_retries_exhausted",
            }
        return {
            "decision": "rewrite_query",
            "evidence_strength": "weak",
            "reason": "absolute_score_below_floor",
        }

    # 2. Strong evidence requires BOTH a healthy absolute score and a
    # confident relative shape - either signal alone isn't enough.
    strong_by_distribution = (
        top_score >= settings.retrieval_strong_top_score
        and top_to_mean >= settings.retrieval_top_to_mean_ratio
        and gap_ratio >= settings.retrieval_gap_ratio
    )
    strong_by_overview = overview_dominant and gap_ratio >= settings.retrieval_gap_ratio

    if strong_by_distribution or strong_by_overview:
        reason = "overview_dominant_with_clear_margin" if (strong_by_overview and not strong_by_distribution) else "strong_score_distribution"
        return {"decision": "generate", "evidence_strength": "strong", "reason": reason}

    # 3. Ambiguous - defer to the LLM grader.
    if gap_ratio < settings.retrieval_gap_ratio:
        reason = "top_candidates_too_close"
    elif top_to_mean < settings.retrieval_top_to_mean_ratio:
        reason = "weak_top_candidate_separation"
    else:
        reason = "retrieval_requires_semantic_grading"
    return {"decision": "grade", "evidence_strength": "ambiguous", "reason": reason}