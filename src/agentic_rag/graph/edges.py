"""Conditional routing functions for the corrective RAG graph."""

from __future__ import annotations

from agentic_rag.config import settings
from agentic_rag.graph.state import RAGState
from agentic_rag.observability.trace import log_stage
from agentic_rag.policies.generation import is_refusal


def route_after_contextualization(
    state: RAGState,
) -> str:
    """Route control messages directly to conversation recording."""

    if state.get("query_is_control", False):
        decision = "record_turn"
    else:
        decision = "retrieve"

    print(
        f"[route_after_contextualization] "
        f"query_intent={state.get('query_intent')!r} "
        f"decision={decision!r}"
    )

    log_stage(
        "route_after_contextualization",
        query_intent=state.get("query_intent"),
        decision=decision,
    )

    return decision


def route_after_retrieval_assessment(
    state: RAGState,
) -> str:
    """Route the three-way retrieval policy."""

    retrieval_decision = state.get(
        "retrieval_decision",
        "grade_documents",
    )

    retry_count = state.get("retry_count", 0)

    if retrieval_decision == "generate":
        decision = "generate"

    elif retrieval_decision == "rewrite_query":
        # Low evidence should normally trigger corrective retrieval.
        #
        # Once the retrieval retry budget is exhausted, defer to the
        # semantic grader rather than repeatedly rewriting the query.
        if retry_count >= settings.max_retries:
            decision = "grade_documents"
        else:
            decision = "rewrite_query"

    else:
        decision = "grade_documents"

    print(
        "[route_after_retrieval_assessment] "
        f"retrieval_decision={retrieval_decision!r} "
        f"retry_count={retry_count} "
        f"decision={decision!r}"
    )

    log_stage(
        "route_after_retrieval_assessment",
        retrieval_decision=retrieval_decision,
        retry_count=retry_count,
        decision=decision,
    )

    return decision


def route_after_grading(
    state: RAGState,
) -> str:
    """Route the semantic relevance grader."""

    grade = state.get("relevance_grade")
    retry_count = state.get("retry_count", 0)

    if grade == "relevant":
        decision = "generate"

    elif retry_count >= settings.max_retries:
        # Best-effort generation is retained for compatibility with
        # the existing graph behavior. The generation prompt itself
        # will abstain if evidence is insufficient.
        decision = "generate"

    else:
        decision = "rewrite_query"

    print(
        "[route_after_grading] "
        f"grade={grade!r} "
        f"retry_count={retry_count} "
        f"decision={decision!r}"
    )

    log_stage(
        "route_after_grading",
        relevance_grade=grade,
        retry_count=retry_count,
        decision=decision,
    )

    return decision


def route_after_generate(
    state: RAGState,
) -> str:
    """Skip hallucination verification for explicit refusals."""

    generation = state.get("generation", "")

    if is_refusal(generation):
        decision = "record_turn"
    else:
        decision = "check_hallucination"

    print(
        "[route_after_generate] "
        f"refusal={is_refusal(generation)} "
        f"decision={decision!r}"
    )

    log_stage(
        "route_after_generate",
        refusal=is_refusal(generation),
        decision=decision,
    )

    return decision


def route_after_hallucination_check(
    state: RAGState,
) -> str:
    """Bound the hallucination correction loop."""

    grade = state.get("hallucination_grade")
    retry_count = state.get("hallucination_retry_count", 0)

    if grade == "grounded":
        decision = "end"

    elif retry_count >= settings.max_retries:
        decision = "end"

    else:
        decision = "generate"

    print(
        "[route_after_hallucination_check] "
        f"grade={grade!r} "
        f"retry_count={retry_count} "
        f"decision={decision!r}"
    )

    log_stage(
        "route_after_hallucination_check",
        hallucination_grade=grade,
        hallucination_retry_count=retry_count,
        decision=decision,
    )

    return decision