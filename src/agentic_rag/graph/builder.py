"""Assembles the corrective RAG StateGraph.

Flow:

contextualize -> retrieve -> grade
                           ├── relevant -> generate -> hallucination check
                           │                              ├── grounded -> record -> END
                           │                              └── hallucinated -> generate
                           │
                           └── irrelevant -> rewrite -> retrieve
"""

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph

from agentic_rag.graph.edges import (
    route_after_grading,
    route_after_hallucination_check,
)
from agentic_rag.graph.nodes import (
    check_hallucination,
    contextualize_question,
    generate,
    grade_documents,
    record_turn,
    retrieve,
    rewrite_query,
)
from agentic_rag.graph.state import RAGState


def build_graph(checkpointer: BaseCheckpointSaver):

    graph = StateGraph(RAGState)

    # ---------------------------------------------------------
    # Nodes
    # ---------------------------------------------------------

    graph.add_node("contextualize_question", contextualize_question)
    graph.add_node("retrieve", retrieve)
    graph.add_node("grade_documents", grade_documents)
    graph.add_node("rewrite_query", rewrite_query)
    graph.add_node("generate", generate)
    graph.add_node("check_hallucination", check_hallucination)
    graph.add_node("record_turn", record_turn)

    # ---------------------------------------------------------
    # Entry point
    # ---------------------------------------------------------

    graph.set_entry_point("contextualize_question")

    # ---------------------------------------------------------
    # Contextualization -> Retrieval
    # ---------------------------------------------------------

    graph.add_edge(
        "contextualize_question",
        "retrieve",
    )

    # ---------------------------------------------------------
    # Retrieval -> Relevance Grading
    # ---------------------------------------------------------

    graph.add_edge(
        "retrieve",
        "grade_documents",
    )

    # ---------------------------------------------------------
    # Relevance routing
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "grade_documents",
        route_after_grading,
        {
            "rewrite_query": "rewrite_query",
            "generate": "generate",
        },
    )

    # ---------------------------------------------------------
    # Corrective retrieval loop
    # ---------------------------------------------------------

    graph.add_edge(
        "rewrite_query",
        "retrieve",
    )

    # ---------------------------------------------------------
    # Generation -> Hallucination Check
    # ---------------------------------------------------------

    graph.add_edge(
        "generate",
        "check_hallucination",
    )

    # ---------------------------------------------------------
    # Hallucination routing
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
    # Record conversation
    # ---------------------------------------------------------

    graph.add_edge(
        "record_turn",
        END,
    )

    return graph.compile(checkpointer=checkpointer)