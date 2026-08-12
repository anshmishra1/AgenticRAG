"""State schema shared across all graph nodes."""
import operator
from typing import Annotated, TypedDict

from langchain_core.documents import Document
from langgraph.graph.message import add_messages


class RAGState(TypedDict, total=False):
    question: str
    retrieval_query: str

    documents: list[Document]

    # Retrieval diagnostics
    retrieval_scores: list[float]
    retrieval_top_score: float
    retrieval_confidence: str

    generation: str

    relevance_grade: str
    hallucination_grade: str

    retry_count: int

    messages: Annotated[list, add_messages]
    trace: Annotated[list[dict], operator.add]   # accumulates one entry per node; printed as a summary at the end