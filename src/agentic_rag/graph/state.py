"""State schema shared across all graph nodes."""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.documents import Document
from langgraph.graph.message import add_messages


class RAGState(TypedDict, total=False):
    # ---------------------------------------------------------
    # User / conversation
    # ---------------------------------------------------------

    question: str
    document_id: str
    retrieval_query: str

    query_intent: str
    query_is_control: bool
    contextualization_used: bool

    # ---------------------------------------------------------
    # Retrieval
    # ---------------------------------------------------------

    documents: list[Document]
    retrieval_scores: list[float]

    retrieval_top_score: float
    retrieval_second_score: float
    retrieval_score_gap: float
    retrieval_mean_score: float
    retrieval_top_to_mean_ratio: float
    retrieval_gap_ratio: float

    retrieval_overview_top_score: float | None
    retrieval_content_top_score: float | None

    retrieval_decision: str
    retrieval_evidence_strength: str
    retrieval_decision_reason: str

    # ---------------------------------------------------------
    # Relevance grading
    # ---------------------------------------------------------

    relevance_grade: str

    # ---------------------------------------------------------
    # Generation
    # ---------------------------------------------------------

    generation: str

    # ---------------------------------------------------------
    # Hallucination verification
    # ---------------------------------------------------------

    hallucination_grade: str
    hallucination_retry_count: int
    grounding_diagnosis: str
    grounding_unsupported_claims: list[str]
    correction_attempted: bool

    # ---------------------------------------------------------
    # Corrective retrieval
    # ---------------------------------------------------------

    retry_count: int

    # ---------------------------------------------------------
    # Observability
    # ---------------------------------------------------------

    trace: Annotated[list[dict], lambda left, right: left + right]

    # ---------------------------------------------------------
    # Persistent conversation memory
    # ---------------------------------------------------------

    messages: Annotated[list, add_messages]