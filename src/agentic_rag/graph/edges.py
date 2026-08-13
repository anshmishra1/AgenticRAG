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
    """Skip the LLM relevance grader when retrieval evidence is strong."""
    decision_val = state.get("retrieval_decision")

    print("\n" + "=" * 70)
    print("GRAPH ROUTER: AFTER RETRIEVAL ASSESSMENT")
    print("=" * 70)
    print(f"Retrieval decision: {decision_val}")

    if decision_val == "generate":
        decision = "generate"
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


def route_after_hallucination_check(state: RAGState) -> str:
    grade = state.get("hallucination_grade")
    retry_count = state.get("hallucination_retry_count", 0)

    print("\n" + "=" * 70)
    print("GRAPH ROUTER: AFTER HALLUCINATION CHECK")
    print("=" * 70)

    print(f"Hallucination grade: {grade}")
    print(f"Retry count: {retry_count}")
    print(f"Maximum retries: {settings.max_retries}")

    if grade == "grounded":
        decision = "end"
        print("ROUTE -> record_turn")
        log_stage("route_after_hallucination_check", hallucination_grade=grade, retry_count=retry_count, decision=decision)
        return decision

    if retry_count >= settings.max_retries:
        decision = "end"
        print("ROUTE -> record_turn")
        print("Reason: maximum retries reached.")
        log_stage("route_after_hallucination_check", hallucination_grade=grade, retry_count=retry_count, decision=decision)
        return decision

    decision = "generate"
    print(f"ROUTE -> {decision}")
    log_stage("route_after_hallucination_check", hallucination_grade=grade, retry_count=retry_count, decision=decision)
    return decision