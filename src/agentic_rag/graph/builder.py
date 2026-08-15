"""Assemble the corrective Agentic RAG StateGraph."""

from __future__ import annotations

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph

from agentic_rag.graph.edges import (
    route_after_contextualization,
    route_after_generate,
    route_after_grading,
    route_after_hallucination_check,
    route_after_retrieval_assessment,
)
from agentic_rag.graph.nodes import (
    assess_retrieval,
    check_hallucination,
    contextualize_question,
    generate,
    grade_documents,
    record_turn,
    retrieve,
    rewrite_query,
)
from agentic_rag.graph.state import RAGState


def build_graph(
    checkpointer: BaseCheckpointSaver,
):
    """Build and compile the corrective RAG graph."""

    graph = StateGraph(RAGState)

    # ---------------------------------------------------------
    # Nodes
    # ---------------------------------------------------------

    graph.add_node(
        "contextualize_question",
        contextualize_question,
    )

    graph.add_node(
        "retrieve",
        retrieve,
    )

    graph.add_node(
        "assess_retrieval",
        assess_retrieval,
    )

    graph.add_node(
        "grade_documents",
        grade_documents,
    )

    graph.add_node(
        "rewrite_query",
        rewrite_query,
    )

    graph.add_node(
        "generate",
        generate,
    )

    graph.add_node(
        "check_hallucination",
        check_hallucination,
    )

    graph.add_node(
        "record_turn",
        record_turn,
    )

    # ---------------------------------------------------------
    # Entry
    # ---------------------------------------------------------

    graph.set_entry_point("contextualize_question")

    # ---------------------------------------------------------
    # Contextualization
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "contextualize_question",
        route_after_contextualization,
        {
            "retrieve": "retrieve",
            "record_turn": "record_turn",
        },
    )

    # ---------------------------------------------------------
    # Retrieval
    # ---------------------------------------------------------

    graph.add_edge(
        "retrieve",
        "assess_retrieval",
    )

    # ---------------------------------------------------------
    # Three-way evidence gate
    #
    # HIGH       -> generate
    # AMBIGUOUS  -> grade_documents
    # LOW        -> rewrite_query
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "assess_retrieval",
        route_after_retrieval_assessment,
        {
            "generate": "generate",
            "grade_documents": "grade_documents",
            "rewrite_query": "rewrite_query",
        },
    )

    # ---------------------------------------------------------
    # Semantic relevance grading
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "grade_documents",
        route_after_grading,
        {
            "generate": "generate",
            "rewrite_query": "rewrite_query",
        },
    )

    # ---------------------------------------------------------
    # Corrective retrieval
    # ---------------------------------------------------------

    graph.add_edge(
        "rewrite_query",
        "retrieve",
    )

    # ---------------------------------------------------------
    # Generation
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "generate",
        route_after_generate,
        {
            "check_hallucination": "check_hallucination",
            "record_turn": "record_turn",
        },
    )

    # ---------------------------------------------------------
    # Hallucination verification
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "check_hallucination",
        route_after_hallucination_check,
        {
            "generate": "generate",
            "end": "record_turn",
        },
    )

    # ---------------------------------------------------------
    # Conversation persistence
    # ---------------------------------------------------------

    graph.add_edge(
        "record_turn",
        END,
    )

    return graph.compile(
        checkpointer=checkpointer,
    )