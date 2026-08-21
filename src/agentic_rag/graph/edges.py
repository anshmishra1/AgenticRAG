"""Conditional edge functions controlling the feedback loops:
- retrieval assessment -> skip grader if strong evidence
- relevance grading -> rewrite -> re-retrieve
- hallucination check -> regenerate

Each routing decision is logged so the trace shows not just what was graded, but
what the graph chose to do about it."""

from agentic_rag.config import settings
from agentic_rag.graph.state import RAGState
from agentic_rag.observability.trace import log_stage


def route_after_retrieval_assessment(state: RAGState) -> str:
    """Route on the three-way decision from assess_retrieval:
    generate (strong) | grade_documents (ambiguous) | rewrite_query (weak)."""
    decision_val = state.get("retrieval_decision")

    print("\n" + "=" * 70)
    print("GRAPH ROUTER: AFTER RETRIEVAL ASSESSMENT")
    print("=" * 70)
    print(f"Retrieval decision: {decision_val}")

    if decision_val == "generate":
        decision = "generate"
    elif decision_val == "rewrite_query":
        decision = "rewrite_query"
    else:
        decision = "grade_documents"

    print(f"ROUTE -> {decision}")
    log_stage("route_after_retrieval_assessment", retrieval_decision=decision_val, decision=decision)
    return decision


def route_after_grading(state: RAGState) -> str:
    grade = state.get("relevance_grade")
    retry_count = state.get("retry_count", 0)

    print("\n" + "=" * 70)
    print("GRAPH ROUTER: AFTER DOCUMENT GRADING")
    print("=" * 70)

    print(f"Relevance grade: {grade}")
    print(f"Retry count: {retry_count}")
    print(f"Maximum retries: {settings.max_retries}")

    if grade == "relevant":
        decision = "generate"
        print(f"ROUTE -> {decision}")
        log_stage("route_after_grading", relevance_grade=grade, retry_count=retry_count, decision=decision)
        return decision

    if retry_count >= settings.max_retries:
        decision = "generate"
        print(f"ROUTE -> {decision}")
        print("Reason: maximum retrieval retries reached.")
        log_stage("route_after_grading", relevance_grade=grade, retry_count=retry_count, decision=decision)
        return decision

    decision = "rewrite_query"
    print(f"ROUTE -> {decision}")
    log_stage("route_after_grading", relevance_grade=grade, retry_count=retry_count, decision=decision)
    return decision

def route_after_contextualization(state: RAGState) -> str:
    """
    Route control messages directly to record_turn.
    All other queries continue to retrieval.
    """

    if state.get("query_is_control", False):
        decision = "record_turn"
    else:
        decision = "retrieve"

    print("\n" + "=" * 70)
    print("GRAPH ROUTER: AFTER CONTEXTUALIZATION")
    print("=" * 70)
    print(f"Query intent: {state.get('query_intent')}")
    print(f"ROUTE -> {decision}")

    log_stage(
        "route_after_contextualization",
        query_intent=state.get("query_intent"),
        decision=decision,
    )

    return decision

def route_after_hallucination_check(state: RAGState) -> str:
    diagnosis = state.get("grounding_diagnosis", state.get("hallucination_grade"))
    correction_attempted = state.get("correction_attempted", False)
    retry_count = state.get("retry_count", 0)

    print("\n" + "=" * 70)
    print("GRAPH ROUTER: AFTER HALLUCINATION CHECK")
    print("=" * 70)
    print(f"Grounding diagnosis: {diagnosis}")
    print(f"Correction already attempted: {correction_attempted}")
    print(f"Retrieval retry count: {retry_count} / {settings.max_retries}")

    if diagnosis == "grounded":
        decision = "end"
        print("ROUTE -> record_turn")
        log_stage("route_after_hallucination_check", grounding_diagnosis=diagnosis, correction_attempted=correction_attempted, decision=decision)
        return decision

    if correction_attempted:
        # One correction already spent - do not loop again regardless of
        # diagnosis. record_turn's disclaimer covers a still-unverified answer.
        decision = "end"
        print("ROUTE -> record_turn")
        print("Reason: single correction budget already spent.")
        log_stage("route_after_hallucination_check", grounding_diagnosis=diagnosis, correction_attempted=correction_attempted, decision=decision)
        return decision

    if diagnosis == "insufficient_evidence" and retry_count < settings.max_retries:
        decision = "rewrite_query"
        print(f"ROUTE -> {decision}")
        print("Reason: evidence is thin, not a generation error - retrieve again.")
        log_stage("route_after_hallucination_check", grounding_diagnosis=diagnosis, correction_attempted=correction_attempted, decision=decision)
        return decision

    # unsupported, or insufficient_evidence with retrieval retries exhausted
    decision = "correct_generation"
    print(f"ROUTE -> {decision}")
    if diagnosis == "insufficient_evidence":
        print("Reason: insufficient evidence but retrieval retries exhausted - falling back to constrained regeneration.")
    log_stage("route_after_hallucination_check", grounding_diagnosis=diagnosis, correction_attempted=correction_attempted, decision=decision)
    return decision