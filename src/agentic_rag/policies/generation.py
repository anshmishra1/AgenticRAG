"""Generation-side policy: what reaches the prompt, and what needs a
hallucination check at all.
"""
from __future__ import annotations

import re

from agentic_rag.config import settings

# A genuine refusal is short and opens with a hedge. A long, substantive
# answer that happens to start with "I'm not sure, but..." before giving real
# content is NOT a refusal - it still needs grounding verification. That's
# why this requires both a pattern match AND a length cap, not pattern alone.
_REFUSAL_PATTERNS = [
    r"^i don'?t know\b",
    r"^i do not know\b",
    r"^i'?m not sure\b",
    r"^i cannot (find|determine|answer)\b",
    r"^the (context|document|provided context) does(n'?t| not) (contain|provide|include|mention)\b",
    r"^no relevant (information|context)\b",
    r"^unable to (find|answer)\b",
]
_MAX_REFUSAL_CHARS = 200


def is_refusal_answer(text: str) -> bool:
    """True only when the answer IS a refusal, not merely contains one.
    Refusals make no factual claim, so running them through the hallucination
    grader is a category error - there's nothing to check for groundedness.
    Skipping the check here removes an LLM call and prevents the failure mode
    where a correct 'I don't know' gets misclassified as hallucinated and
    triggers a pointless regenerate loop against the same unhelpful context."""
    stripped = text.strip()
    if not stripped or len(stripped) > _MAX_REFUSAL_CHARS:
        return False
    lowered = stripped.lower()
    return any(re.match(pattern, lowered) for pattern in _REFUSAL_PATTERNS)


def apply_generation_limits(documents: list, history_messages: list) -> tuple[str, list]:
    """Trims retrieved documents and chat history to the configured budget
    before they reach the prompt. Keeps prompt size - and therefore cost and
    latency - predictable regardless of how many chunks retrieval returns or
    how long the conversation has run."""
    limited_docs = documents[: settings.max_generation_context_documents]

    context = "\n\n".join(d.page_content for d in limited_docs)
    if len(context) > settings.max_generation_context_chars:
        context = context[: settings.max_generation_context_chars] + "\n[...truncated]"

    limited_history = history_messages[-settings.max_history_messages_for_generation:]
    return context, limited_history