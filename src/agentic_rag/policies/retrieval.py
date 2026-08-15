"""Retrieval evidence policies.

The retrieval policy deliberately uses a three-way decision:

    HIGH       -> generate
    AMBIGUOUS  -> LLM relevance grader
    LOW        -> corrective query rewrite

The absolute thresholds are configuration values and are expected to be
calibrated from representative retrieval observations.

RAGAS is intentionally not used here. RAGAS evaluates generation quality;
this module decides how raw retrieval evidence should be routed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RetrievalMetrics:
    """Derived metrics from a ranked retrieval score list."""

    top_score: float
    second_score: float
    score_gap: float
    mean_score: float
    top_to_mean_ratio: float
    gap_ratio: float


def calculate_retrieval_metrics(
    scores: list[float],
) -> RetrievalMetrics:
    """Calculate stable retrieval metrics from similarity scores."""

    if not scores:
        return RetrievalMetrics(
            top_score=0.0,
            second_score=0.0,
            score_gap=0.0,
            mean_score=0.0,
            top_to_mean_ratio=0.0,
            gap_ratio=0.0,
        )

    ordered = sorted(
        (float(score) for score in scores),
        reverse=True,
    )

    top_score = ordered[0]

    second_score = (
        ordered[1]
        if len(ordered) > 1
        else ordered[0]
    )

    mean_score = sum(ordered) / len(ordered)
    score_gap = top_score - second_score

    top_to_mean_ratio = (
        top_score / mean_score
        if mean_score > 0
        else 0.0
    )

    gap_ratio = (
        score_gap / top_score
        if top_score > 0
        else 0.0
    )

    return RetrievalMetrics(
        top_score=top_score,
        second_score=second_score,
        score_gap=score_gap,
        mean_score=mean_score,
        top_to_mean_ratio=top_to_mean_ratio,
        gap_ratio=gap_ratio,
    )


def _cfg_value(
    cfg: Any,
    name: str,
    default: float,
) -> float:
    """Read a numeric setting safely."""

    value = getattr(cfg, name, default)

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def classify_retrieval_confidence(
    metrics: RetrievalMetrics,
    *,
    top_doc_type: str | None = None,
    overview_top_score: float | None = None,
    content_top_score: float | None = None,
    cfg: Any,
) -> tuple[str, str, str]:
    """Return ``(decision, evidence_strength, reason)``.

    Decisions:
        generate
        grade_documents
        rewrite_query

    The low gate is evaluated first because a strong relative score
    distribution must never override an absolutely weak retrieval score.

    The high gate requires the calibrated strong-score boundary plus
    supporting relative evidence, or a clearly dominant overview result.

    Everything else remains ambiguous and is delegated to the LLM grader.
    """

    min_top_score = _cfg_value(
        cfg,
        "retrieval_min_top_score",
        0.35,
    )

    strong_top_score = _cfg_value(
        cfg,
        "retrieval_strong_top_score",
        0.55,
    )

    min_top_to_mean = _cfg_value(
        cfg,
        "retrieval_min_top_to_mean_ratio",
        1.20,
    )

    min_gap_ratio = _cfg_value(
        cfg,
        "retrieval_min_gap_ratio",
        0.05,
    )

    overview_margin = _cfg_value(
        cfg,
        "retrieval_overview_margin",
        0.10,
    )

    # ---------------------------------------------------------
    # 1. No evidence / absolute low floor
    # ---------------------------------------------------------

    if metrics.top_score <= 0:
        return (
            "rewrite_query",
            "low",
            "no_retrieval_evidence",
        )

    if metrics.top_score < min_top_score:
        return (
            "rewrite_query",
            "low",
            "below_absolute_score_floor",
        )

    # ---------------------------------------------------------
    # 2. Strong evidence
    # ---------------------------------------------------------

    overview_dominant = (
        top_doc_type == "overview"
        and overview_top_score is not None
        and content_top_score is not None
        and (
            float(overview_top_score)
            - float(content_top_score)
            >= overview_margin
        )
    )

    relative_strength = (
        metrics.top_to_mean_ratio >= min_top_to_mean
        and metrics.gap_ratio >= min_gap_ratio
    )

    if metrics.top_score >= strong_top_score:
        if overview_dominant:
            return (
                "generate",
                "strong",
                "overview_dominant_with_clear_margin",
            )

        if relative_strength:
            return (
                "generate",
                "strong",
                "strong_absolute_and_relative_evidence",
            )

    # ---------------------------------------------------------
    # 3. Ambiguous region
    # ---------------------------------------------------------

    return (
        "grade_documents",
        "ambiguous",
        "ambiguous_score_distribution",
    )