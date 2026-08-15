"""Conversation/query-intent policies.

This module contains deterministic classification for:
- conversation-control messages
- standalone questions
- likely follow-up questions

No LLM call is made here.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from langchain_core.messages import BaseMessage


_CONTROL_PATTERNS = (
    r"^\s*that's all[\s.!]*$",
    r"^\s*thats all[\s.!]*$",
    r"^\s*that is all[\s.!]*$",
    r"^\s*i(?:'m| am) done[\s.!]*$",
    r"^\s*done[\s.!]*$",
    r"^\s*no more questions[\s.!]*$",
    r"^\s*i don't have any more questions[\s.!]*$",
    r"^\s*i do not have any more questions[\s.!]*$",
    r"^\s*no further questions[\s.!]*$",
    r"^\s*nothing else[\s.!]*$",
    r"^\s*thank(?:s| you)[\s.!]*$",
    r"^\s*goodbye[\s.!]*$",
    r"^\s*bye[\s.!]*$",
)

_FOLLOW_UP_PATTERNS = (
    r"\bthis\b",
    r"\bthat\b",
    r"\bthese\b",
    r"\bthose\b",
    r"\bit\b",
    r"\bthey\b",
    r"\bthem\b",
    r"\bthe same\b",
    r"\babove\b",
    r"\bprevious\b",
    r"\bearlier\b",
    r"\bmore detail\b",
    r"\bin more detail\b",
    r"\belaborate\b",
    r"\belabor\b",
    r"\bexplain further\b",
    r"\bexpand on\b",
    r"\bgo deeper\b",
    r"\bcontinue\b",
    r"\bwhat about\b",
    r"\bhow about\b",
    r"\bwhy is that\b",
    r"\bhow does that\b",
    r"\bhow do they\b",
)

_FOLLOW_UP_STARTERS = (
    "can you explain",
    "can you elaborate",
    "can you expand",
    "could you explain",
    "could you elaborate",
    "could you expand",
    "explain that",
    "explain this",
    "tell me more",
    "elaborate on that",
    "elaborate further",
    "go deeper",
    "what about that",
    "what about this",
    "why is that",
    "how does that",
    "how do they",
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def is_control_query(question: str) -> bool:
    """Return True for messages that should bypass document retrieval."""
    normalized = _normalize(question)

    if not normalized:
        return True

    return any(
        re.search(pattern, normalized)
        for pattern in _CONTROL_PATTERNS
    )


def is_likely_follow_up(
    question: str,
    history: Sequence[BaseMessage],
) -> bool:
    """Classify whether a question likely depends on prior conversation.

    This is deliberately conservative. A false positive causes an unnecessary
    contextualization LLM call, while a false negative leaves the original
    question untouched and can still be handled by normal retrieval.
    """
    if not history:
        return False

    normalized = _normalize(question)

    if not normalized or is_control_query(normalized):
        return False

    if any(
        normalized.startswith(starter)
        for starter in _FOLLOW_UP_STARTERS
    ):
        return True

    if any(
        re.search(pattern, normalized)
        for pattern in _FOLLOW_UP_PATTERNS
    ):
        return True

    # Very short questions with pronouns are often conversational follow-ups.
    tokens = normalized.split()

    if len(tokens) <= 8:
        pronouns = {
            "it",
            "this",
            "that",
            "these",
            "those",
            "they",
            "them",
        }

        if any(token in pronouns for token in tokens):
            return True

    return False


def classify_query_intent(
    question: str,
    history: Sequence[BaseMessage],
) -> tuple[str, bool]:
    """Return ``(intent, is_control)``.

    Possible intents:
        - control
        - follow_up
        - new_question
    """
    if is_control_query(question):
        return "control", True

    if is_likely_follow_up(question, history):
        return "follow_up", False

    return "new_question", False