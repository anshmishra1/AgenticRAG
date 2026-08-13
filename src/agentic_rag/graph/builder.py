"""Assembles the corrective RAG StateGraph.

Flow:

contextualize -> retrieve -> grade
                           ├── relevant -> generate -> hallucination check
                           │                              ├── grounded -> record -> END
                           │                              └── hallucinated -> generate
                           │
                           └── irrelevant -> rewrite -> retrieve
"""

from langgraph import graph
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph

from agentic_rag.graph.edges import (
    route_after_grading,
    route_after_hallucination_check,
    route_after_retrieval_assessment,
)
from agentic_rag.graph.nodes import (
    assess_retrieval,
    contextualize_question,
    check_hallucination,
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
    graph.add_node("assess_retrieval", assess_retrieval)
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
    # Retrieve -> AssessRetrieval
    # ---------------------------------------------------------
    graph.add_edge("contextualize_question", "retrieve")
    graph.add_edge("retrieve", "assess_retrieval")
    # graph.add_edge("retrieve", "grade_documents")

    graph.add_conditional_edges(
        "assess_retrieval",
        route_after_retrieval_assessment,
        {
            "generate": "generate",
            "grade_documents": "grade_documents",
        },
    )

    # ---------------------------------------------------------
    # Retrieval -> Relevance Grading
    # ---------------------------------------------------------

    # graph.add_edge(
    #     "retrieve",
    #     "grade_documents",
    # )

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