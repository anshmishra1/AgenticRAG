"""Lightweight query classification utilities.

These functions intentionally avoid LLM calls.
They are used to decide whether an expensive contextualization
step is actually necessary.
"""

from __future__ import annotations

import re


# High-confidence conversational references.
#
# We deliberately keep this conservative.
# A false negative costs one contextualization call.
# A false positive can corrupt retrieval for an independent question.
FOLLOW_UP_PATTERNS = (
    r"\bit\b",
    r"\bthis\b",
    r"\bthat\b",
    r"\bthese\b",
    r"\bthose\b",
    r"\bthey\b",
    r"\bthem\b",
    r"\bthe same\b",
    r"\bthe above\b",
    r"\bthe previous\b",
    r"\bwhat about\b",
    r"\bhow about\b",
    r"\bcan you elaborate\b",
    r"\bexplain (it|that|this)\b",
    r"\bexpand (on|upon) (it|that|this)\b",
    r"\bgo deeper\b",
    r"\bmore detail\b",
    r"\bin more detail\b",
    r"\bmore about (it|that|this)\b",
    r"\bwhy is (it|that|this)\b",
    r"\bhow does (it|that|this)\b",
)


def is_likely_follow_up(
    question: str,
    history: list | None,
) -> bool:
    """Return True only when a query strongly looks like a follow-up.

    This is intentionally conservative.

    Examples that should return True:
        "Explain it in more detail."
        "What about its limitations?"
        "Can you elaborate on that?"
        "Why is that important?"

    Examples that should return False:
        "What is Docker?"
        "Explain transformers."
        "How does RAG work?"
        "What are the limitations of vector databases?"
    """

    if not history:
        return False

    text = " ".join(question.lower().strip().split())

    if not text:
        return False

    # Very short conversational questions are strong follow-up candidates.
    words = text.split()

    if len(words) <= 7:
        if any(re.search(pattern, text) for pattern in FOLLOW_UP_PATTERNS):
            return True

    # Explicit conversational references.
    if any(re.search(pattern, text) for pattern in FOLLOW_UP_PATTERNS):
        return True

    return False