"""Generation policies.

Centralizes:
- context size limits
- conversation-history limits
- refusal detection
- corrective-generation instructions
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage


_DEFAULT_MAX_DOCUMENTS = 5
_DEFAULT_MAX_CONTEXT_CHARS = 12000
_DEFAULT_MAX_HISTORY_MESSAGES = 2

_REFUSAL_PATTERNS = (
    r"^\s*i\s+(?:do\s+not|don't)\s+know[\s.!]*$",
    r"^\s*i\s+(?:do\s+not|don't)\s+have\s+enough\s+information[\s.!]*$",
    r"^\s*i\s+(?:cannot|can't)\s+answer[\s.!]*$",
    r"^\s*i\s+(?:cannot|can't)\s+find\s+that\s+information[\s.!]*$",
    r"^\s*the\s+(?:provided\s+)?context\s+does\s+not\s+contain[\s\S]*",
    r"^\s*the\s+provided\s+documents?\s+do\s+not\s+contain[\s\S]*",
    r"^\s*there\s+is\s+not\s+enough\s+information[\s\S]*",
)


def _int_setting(
    settings: Any,
    name: str,
    default: int,
) -> int:
    value = getattr(settings, name, default)

    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


def truncate_context(
    documents: Sequence[Document],
    settings: Any,
) -> list[Document]:
    """Apply both document-count and character-budget limits.

    Documents are already ranked by the retrieval node, so truncation keeps
    the strongest evidence first.
    """

    max_documents = _int_setting(
        settings,
        "max_generation_context_documents",
        _DEFAULT_MAX_DOCUMENTS,
    )

    max_chars = _int_setting(
        settings,
        "max_generation_context_chars",
        _DEFAULT_MAX_CONTEXT_CHARS,
    )

    if max_documents == 0 or max_chars == 0:
        return []

    selected: list[Document] = []
    used_chars = 0

    for document in documents[:max_documents]:
        content = document.page_content or ""

        if not content:
            continue

        remaining = max_chars - used_chars

        if remaining <= 0:
            break

        if len(content) > remaining:
            content = content[:remaining]

        selected.append(
            Document(
                page_content=content,
                metadata=document.metadata,
            )
        )

        used_chars += len(content)

    return selected


def build_history_text(
    messages: Sequence[BaseMessage],
    settings: Any,
) -> tuple[str, list[BaseMessage]]:
    """Build a bounded representation of conversation history."""

    max_messages = _int_setting(
        settings,
        "max_history_messages_for_generation",
        _DEFAULT_MAX_HISTORY_MESSAGES,
    )

    if max_messages == 0:
        return "None", []

    history = list(messages[-max_messages:])

    if not history:
        return "None", []

    history_text = "\n".join(
        f"{message.type}: {message.content}"
        for message in history
    )

    return history_text, history


def is_refusal(text: str | None) -> bool:
    """Return True when the generated answer is an explicit abstention.

    This is deliberately conservative. We do not classify an answer as a
    refusal merely because it contains words such as "don't know" somewhere
    in a longer factual answer.
    """

    if not text:
        return True

    normalized = re.sub(
        r"\s+",
        " ",
        text.strip().lower(),
    )

    return any(
        re.search(pattern, normalized)
        for pattern in _REFUSAL_PATTERNS
    )


def corrective_generation_instruction(
    hallucination_retry_count: int,
) -> str:
    """Return stricter generation instructions after a failed grounding check."""

    if hallucination_retry_count <= 0:
        return (
            "Use only information supported by the supplied context. "
            "If the context does not support the answer, say you don't know."
        )

    return (
        "The previous answer failed the grounding check. "
        "Generate a new, more conservative answer. "
        "Use only claims explicitly supported by the supplied context. "
        "Do not infer missing facts, fill gaps from general knowledge, "
        "or introduce unsupported examples. "
        "If the context is insufficient, say you don't know instead of "
        "trying to complete the answer from memory."
    )