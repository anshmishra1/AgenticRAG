"""Retrieval confidence utilities.

This module intentionally contains no LLM calls.

The initial version only records retrieval characteristics.
Thresholds will be calibrated from real query/grade data before
being used for routing.
"""

from __future__ import annotations


def classify_retrieval_confidence(
    scores: list[float],
) -> str:
    """Classify retrieval confidence.

    IMPORTANT:
    This is intentionally conservative until thresholds are
    calibrated against the project's actual corpus.

    Current behavior:
        no scores -> low
        otherwise -> unknown

    The function exists now so that the graph/state interface
    is ready for calibrated routing later.
    """

    if not scores:
        return "low"

    return "uncalibrated"