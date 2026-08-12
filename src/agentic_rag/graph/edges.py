"""Conditional edge functions controlling the two feedback loops:
relevance grading -> rewrite -> re-retrieve, and hallucination check -> regenerate.
Each routing decision is logged so the trace shows not just what was graded, but
what the graph chose to do about it."""

from agentic_rag.config import settings
from agentic_rag.graph.state import RAGState
from agentic_rag.observability.trace import log_stage


def route_after_grading(state: RAGState) -> str:
    grade = state["relevance_grade"]
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
    grade = state["hallucination_grade"]
    retry_count = state.get("retry_count", 0)

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