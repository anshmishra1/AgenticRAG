"""State schema shared across all graph nodes."""
from typing import Annotated, TypedDict

from langchain_core.documents import Document
from langgraph.graph.message import add_messages


class RAGState(TypedDict, total=False):
    # User/application state
    question: str
    document_id: str

    # Retrieval state
    retrieval_query: str
    documents: list[Document]
    retrieval_scores: list[float]
    retrieval_top_score: float
    retrieval_second_score: float
    retrieval_score_gap: float
    retrieval_mean_score: float
    retrieval_top_to_mean_ratio: float
    retrieval_gap_ratio: float
    retrieval_confidence: str
    retrieval_overview_top_score: float | None
    retrieval_content_top_score: float | None

    # New deterministic retrieval decision layer
    retrieval_decision: str       # "generate" | "grade"
    retrieval_evidence_strength: str  # "strong" | "ambiguous" | "weak"
    retrieval_decision_reason: str

    # Corrective RAG / generation state
    relevance_grade: str
    hallucination_grade: str
    retry_count: int
    hallucination_retry_count: int
    generation: str

    # Conversation / query routing
    query_intent: str
    query_is_control: bool
    contextualization_used: bool

    # Generation diagnostics
    generation_context_chars: int
    generation_history_chars: int
    generation_prompt_chars: int
    generation_output_chars: int

    # Conversation state
    messages: Annotated[list, add_messages]
    trace: list[dict]
