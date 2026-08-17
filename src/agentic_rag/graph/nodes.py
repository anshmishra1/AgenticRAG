"""Node functions for the optimized corrective RAG pipeline.

Optimization introduced in this version:
- Retrieval now produces an evidence profile from the scores/metadata it already has.
- A deterministic retrieval assessment decides whether an LLM relevance grader is
  actually necessary.
- Strong retrieval results go directly to generation.
- Ambiguous/weak retrieval results keep the existing corrective grading + rewrite loop.
- The LLM grader evaluates the strongest candidates instead of blindly grading every
  retrieved chunk.

The existing document_id-scoped retrieval and provider tiers are preserved.
"""
from __future__ import annotations

import json
import logging

from langchain_core.messages import AIMessage, HumanMessage

from agentic_rag.config import settings
from agentic_rag.graph.state import RAGState
from agentic_rag.llm.provider import provider_chain, fast_provider_chain
from agentic_rag.retrieval.vectorstore import retrieve_with_scores
from agentic_rag.policies.conversation  import classify_query_intent
from agentic_rag.policies.retrieval import assess_retrieval_confidence
from agentic_rag.policies.generation import apply_generation_limits, is_refusal_answer
from agentic_rag.core.timing import PerformanceTracker

logger = logging.getLogger(__name__)
tracker = PerformanceTracker()

MAX_GRADING_CANDIDATES = 4


# =============================================================
# Debug helpers
# =============================================================

def _separator(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def _preview(text: str, length: int = 500) -> str:
    text = text.replace("\n", " ")
    return text[:length]


# =============================================================
# Query Intent
# =============================================================

CONTROL_QUERY_PATTERNS = (
    "no more questions",
    "no further questions",
    "nothing else",
    "that's all",
    "that is all",
    "thanks",
    "thank you",
    "stop",
    "done",
    "end this",
)


def classify_query_intent(
    question: str,
    history: list,
) -> tuple[str, bool]:
    """
    Lightweight deterministic query-intent classification.

    Returns:
        (intent, is_control)

    Intents:
        - new_question
        - follow_up
        - control
    """

    normalized = " ".join(question.lower().split())

    # ---------------------------------------------------------
    # Control / conversation-ending input
    # ---------------------------------------------------------

    if any(pattern in normalized for pattern in CONTROL_QUERY_PATTERNS):
        return "control", True

    # ---------------------------------------------------------
    # No history -> cannot be a follow-up
    # ---------------------------------------------------------

    if not history:
        return "new_question", False

    # ---------------------------------------------------------
    # Strong follow-up indicators
    # ---------------------------------------------------------

    follow_up_indicators = (
        "elaborate",
        "elaborate further",
        "explain further",
        "explain more",
        "tell me more",
        "expand on",
        "expand upon",
        "go deeper",
        "in more detail",
        "more details",
        "why is that",
        "how so",
        "what about that",
        "can you clarify",
        "clarify that",
        "what do you mean",
    )

    if any(indicator in normalized for indicator in follow_up_indicators):
        return "follow_up", False

    # ---------------------------------------------------------
    # Referential follow-ups
    # ---------------------------------------------------------

    referential_terms = (
        "that",
        "this",
        "it",
        "those",
        "these",
        "the above",
        "the previous",
        "mentioned earlier",
    )

    if any(
        normalized.startswith(term + " ")
        or normalized == term
        for term in referential_terms
    ):
        return "follow_up", False

    return "new_question", False
# =============================================================
# Contextualize Question
# =============================================================

def contextualize_question(state: RAGState) -> dict:
    """
    Determine whether the incoming query is new, a follow-up, or a
    conversation-control message.

    Only follow-ups requiring conversational resolution invoke the
    fast LLM contextualizer.
    """

    with tracker.measure("contextualize_question"):

        history = state.get("messages", [])[-6:]
        question = state["question"]

        intent, is_control = classify_query_intent(
            question,
            history,
        )

        print("\n" + "=" * 70)
        print("QUERY INTENT")
        print("=" * 70)
        print(f"Question: {question}")
        print(f"Intent: {intent}")
        print(f"Control query: {is_control}")

        # -----------------------------------------------------
        # Control message
        # -----------------------------------------------------

        if is_control:
            return {
                "query_intent": "control",
                "query_is_control": True,
                "contextualization_used": False,
                "retrieval_query": question,
                "trace": [{
                    "stage": "contextualize_question",
                    "question": question,
                    "intent": "control",
                    "contextualization_used": False,
                }],
            }

        # -----------------------------------------------------
        # New standalone question
        # -----------------------------------------------------

        if intent == "new_question":
            return {
                "query_intent": "new_question",
                "query_is_control": False,
                "contextualization_used": False,
                "retrieval_query": question,
                "trace": [{
                    "stage": "contextualize_question",
                    "question": question,
                    "intent": "new_question",
                    "contextualization_used": False,
                }],
            }

        # -----------------------------------------------------
        # Follow-up
        # -----------------------------------------------------

        history_text = "\n".join(
            f"{m.type}: {m.content}"
            for m in history
        )

        prompt = (
            "Rewrite the user's follow-up as a standalone search query "
            "for the same document.\n\n"
            "Rules:\n"
            "1. Preserve the user's actual information need.\n"
            "2. Use the previous conversation only to resolve references.\n"
            "3. Do not introduce new topics.\n"
            "4. Do not answer the question.\n"
            "5. Return only the standalone search query.\n\n"
            f"Conversation:\n{history_text}\n\n"
            f"Follow-up:\n{question}"
        )

        result = fast_provider_chain.invoke(prompt)

        rewritten = result.content.strip()

        return {
            "query_intent": "follow_up",
            "query_is_control": False,
            "contextualization_used": True,
            "retrieval_query": rewritten,
            "trace": [{
                "stage": "contextualize_question",
                "question": question,
                "intent": "follow_up",
                "contextualization_used": True,
                "rewritten_query": rewritten,
                "history_turns": len(history),
            }],
        }


# =============================================================
# Retrieval metrics
# =============================================================

def calculate_retrieval_metrics(scores: list[float]) -> dict:
    if not scores:
        return {
            "top_score": 0.0,
            "second_score": 0.0,
            "score_gap": 0.0,
            "mean_score": 0.0,
            "top_to_mean_ratio": 0.0,
            "gap_ratio": 0.0,
        }

    ordered = sorted((float(score) for score in scores), reverse=True)
    top_score = ordered[0]
    second_score = ordered[1] if len(ordered) > 1 else ordered[0]
    mean_score = sum(ordered) / len(ordered)
    score_gap = top_score - second_score

    # Scores are assumed to be similarity scores where larger is better, as
    # returned by PineconeVectorStore.similarity_search_with_score().
    top_to_mean_ratio = top_score / mean_score if mean_score > 0 else 0.0
    gap_ratio = score_gap / abs(top_score) if top_score != 0 else 0.0

    return {
        "top_score": top_score,
        "second_score": second_score,
        "score_gap": score_gap,
        "mean_score": mean_score,
        "top_to_mean_ratio": top_to_mean_ratio,
        "gap_ratio": gap_ratio,
    }


def _top_score_for_type(results: list[tuple], chunk_type: str) -> float | None:
    scores = [
        float(score)
        for doc, score in results
        if doc.metadata.get("type") == chunk_type
    ]
    return max(scores) if scores else None


# =============================================================
# Retrieval
# =============================================================

def retrieve(state: RAGState) -> dict:
    with tracker.measure("retrieve"):
        _separator("2. RETRIEVAL")

        query = state.get("retrieval_query") or state["question"]
        print(f"Query sent to retriever:\n{query}")

        document_id = state.get("document_id")

        if document_id:
            overview_filter = {
                "$and": [
                    {"document_id": {"$eq": document_id}},
                    {"type": {"$eq": "overview"}},
                ]
            }
            content_filter = {
                "$and": [
                    {"document_id": {"$eq": document_id}},
                    {"type": {"$eq": "content"}},
                ]
            }
            print(f"Document scope: {document_id}")
        else:
            # Backward-compatible fallback. Normal application queries should
            # provide document_id when the user is asking about one document.
            overview_filter = {"type": {"$eq": "overview"}}
            content_filter = None
            print("Document scope: GLOBAL (no document_id supplied)")

        overview_results = retrieve_with_scores(
            query=query,
            k=2,
            filter=overview_filter,
        )

        content_results = retrieve_with_scores(
            query=query,
            k=5,
            filter=content_filter,
        )

        results = overview_results + content_results
        results.sort(key=lambda item: float(item[1]), reverse=True)

        docs = [doc for doc, _ in results]
        scores = [float(score) for _, score in results]

        overview_docs_count = len(overview_results)
        content_docs_count = len(content_results)
        metrics = calculate_retrieval_metrics(scores)
        top_score = metrics["top_score"]
        overview_top_score = _top_score_for_type(results, "overview")
        content_top_score = _top_score_for_type(results, "content")

        print(f"\nOverview chunks retrieved: {overview_docs_count}")
        print(f"Content chunks retrieved: {content_docs_count}")

        for i, doc in enumerate(docs, start=1):
            print("\n" + "-" * 60)
            print(f"DOCUMENT {i}")
            print(f"Similarity score: {scores[i - 1]}")
            print(f"Metadata: {doc.metadata}")
            print(f"\nContent preview:\n{_preview(doc.page_content)}")

        logger.info(
            "RETRIEVAL | query=%r | scores=%s | top=%.4f | second=%.4f | "
            "gap=%.4f | mean=%.4f | top/mean=%.4f | gap_ratio=%.4f",
            query,
            [round(score, 4) for score in scores],
            metrics["top_score"],
            metrics["second_score"],
            metrics["score_gap"],
            metrics["mean_score"],
            metrics["top_to_mean_ratio"],
            metrics["gap_ratio"],
        )

        return {
            "documents": docs,
            "retrieval_scores": scores,
            "retrieval_top_score": top_score,
            "retrieval_second_score": metrics["second_score"],
            "retrieval_score_gap": metrics["score_gap"],
            "retrieval_mean_score": metrics["mean_score"],
            "retrieval_top_to_mean_ratio": metrics["top_to_mean_ratio"],
            "retrieval_gap_ratio": metrics["gap_ratio"],
            "retrieval_overview_top_score": overview_top_score,
            "retrieval_content_top_score": content_top_score,
            "trace": [{
                "stage": "retrieve",
                "retrieval_query": query,
                "document_id": document_id,
                "overview_docs": overview_docs_count,
                "content_docs": content_docs_count,
                "sources": [d.metadata.get("source") for d in docs],
                "scores": scores,
                "top_score": top_score,
                "second_score": metrics["second_score"],
                "score_gap": metrics["score_gap"],
                "mean_score": metrics["mean_score"],
                "top_to_mean_ratio": metrics["top_to_mean_ratio"],
                "gap_ratio": metrics["gap_ratio"],
                "overview_top_score": overview_top_score,
                "content_top_score": content_top_score,
            }],
        }


# =============================================================
# Retrieval assessment — NEW optimization layer
# =============================================================

def assess_retrieval(state: RAGState) -> dict:
    """Decide whether an LLM relevance grader is necessary - or whether the
    evidence is weak enough that grading is pointless and a query rewrite is
    the better next step. Decision logic itself lives in
    policies.retrieval.assess_retrieval_confidence(); this node's job is I/O
    (printing, tracing) and reading state, not the decision rule.
    """
    with tracker.measure("assess_retrieval"):
        _separator("3. RETRIEVAL ASSESSMENT")

        documents = state.get("documents", [])
        scores = [float(score) for score in state.get("retrieval_scores", [])]

        if not documents or not scores:
            decision = "grade"
            reason = "no_retrieval_candidates"
            evidence_strength = "weak"
        else:
            metrics = calculate_retrieval_metrics(scores)
            top_doc = documents[0]
            top_type = top_doc.metadata.get("type")
            overview_top = state.get("retrieval_overview_top_score")
            content_top = state.get("retrieval_content_top_score")
            retry_count = state.get("retry_count", 0)

            result = assess_retrieval_confidence(
                metrics=metrics,
                top_doc_type=top_type,
                overview_top_score=overview_top,
                content_top_score=content_top,
                retry_count=retry_count,
            )
            decision = result["decision"]
            evidence_strength = result["evidence_strength"]
            reason = result["reason"]

            print(f"Top score: {metrics['top_score']:.4f}")
            print(f"Second score: {metrics['second_score']:.4f}")
            print(f"Top/mean ratio: {metrics['top_to_mean_ratio']:.4f}")
            print(f"Gap ratio: {metrics['gap_ratio']:.4f}")
            print(f"Top document type: {top_type}")

        print(f"Evidence strength: {evidence_strength}")
        print(f"Retrieval decision: {decision}")
        print(f"Decision reason: {reason}")

        return {
            "retrieval_decision": decision,
            "retrieval_evidence_strength": evidence_strength,
            "retrieval_decision_reason": reason,
            "trace": [{
                "stage": "assess_retrieval",
                "decision": decision,
                "evidence_strength": evidence_strength,
                "reason": reason,
                "top_score": state.get("retrieval_top_score", 0.0),
                "second_score": state.get("retrieval_second_score", 0.0),
                "score_gap": state.get("retrieval_score_gap", 0.0),
                "mean_score": state.get("retrieval_mean_score", 0.0),
                "top_to_mean_ratio": state.get("retrieval_top_to_mean_ratio", 0.0),
                "gap_ratio": state.get("retrieval_gap_ratio", 0.0),
            }],
        }


# =============================================================
# Document Grading
# =============================================================

def grade_documents(state: RAGState) -> dict:
    """Use the fast LLM only for ambiguous retrieval results."""
    with tracker.measure("grade_documents"):
        _separator("4. DOCUMENT RELEVANCE GRADING")

        documents = state.get("documents", [])
        scores = state.get("retrieval_scores", [])
        query = state.get("retrieval_query") or state["question"]

        # Retrieval already sorted candidates by score. Keep the grader prompt
        # bounded and focused on the strongest evidence instead of all chunks.
        candidates = list(zip(documents, scores))[:MAX_GRADING_CANDIDATES]
        preview = [
            {
                "rank": idx,
                "score": round(float(score), 4),
                "type": doc.metadata.get("type"),
                "source": doc.metadata.get("source"),
                "content": doc.page_content[:500],
            }
            for idx, (doc, score) in enumerate(candidates, start=1)
        ]

        print(f"Question/query being graded:\n{query}")
        print(f"Candidates sent to grader: {len(preview)}")

        prompt = (
            "You are a retrieval relevance grader. Determine whether the retrieved "
            "evidence contains enough information to answer the user's query. "
            "Consider the candidate type metadata: an 'overview' chunk represents "
            "whole-document evidence, while a 'content' chunk represents specific "
            "document content. Return exactly one word: 'relevant' or 'irrelevant'.\n\n"
            f"Question: {query}\n\n"
            f"Retrieved candidates:\n{json.dumps(preview, ensure_ascii=False, default=str)}"
        )

        result = fast_provider_chain.invoke(prompt)
        raw_grade = result.content.strip().lower()
        grade = (
            "relevant"
            if "relevant" in raw_grade and "irrelevant" not in raw_grade
            else "irrelevant"
        )

        print(f"\nRaw LLM grading response: {raw_grade}")
        print(f"\nNormalized relevance grade: {grade}")

        return {
            "relevance_grade": grade,
            "trace": [{
                "stage": "grade_documents",
                "query": query,
                "doc_count": len(documents),
                "graded_candidates": len(preview),
                "raw_grade": raw_grade,
                "normalized_grade": grade,
            }],
        }


# =============================================================
# Query Rewrite
# =============================================================

def rewrite_query(state: RAGState) -> dict:
    with tracker.measure("rewrite_query"):
        _separator("5. QUERY REWRITE")

        current = state.get("retrieval_query") or state["question"]
        retry_count = state.get("retry_count", 0)

        prompt = (
            "Rewrite this search query to be clearer and better suited for "
            "semantic search. Preserve the user's actual information need. "
            "Return only the rewritten query, nothing else.\n\n"
            f"Query: {current}"
        )

        result = fast_provider_chain.invoke(prompt)
        rewritten_query = result.content.strip()
        new_retry_count = retry_count + 1

        return {
            "retrieval_query": rewritten_query,
            "retry_count": new_retry_count,
            "trace": [{
                "stage": "rewrite_query",
                "old_query": current,
                "new_query": rewritten_query,
                "retry_count": new_retry_count,
            }],
        }


# =============================================================
# Generation
# =============================================================

def generate(state: RAGState) -> dict:
    with tracker.measure("generate"):
        _separator("6. GENERATION")

        documents = state.get("documents", [])
        history = state.get("messages", [])

        context, history = apply_generation_limits(documents, history)

        history_text = (
            "\n".join(
                f"{m.type}: {m.content}"
                for m in history
            )
            if history
            else "None"
        )

        prompt = (
            "Answer the question using only the provided context and "
            "prior conversation. "
            "Follow the user's requested level of detail, structure, "
            "and style. "
            "If the user asks for a detailed explanation, provide a "
            "detailed explanation. "
            "If the user asks for a concise answer, keep it concise. "
            "If the answer isn't supported by the context, say you "
            "don't know. "
            "Do not omit important details needed to properly answer "
            "the question.\n\n"
            f"Prior conversation:\n{history_text}\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {state['question']}"
        )

        # ---------------------------------------------------------
        # Generation diagnostics
        # ---------------------------------------------------------

        context_chars = len(context)
        history_chars = len(history_text)
        prompt_chars = len(prompt)

        print(f"Context characters : {context_chars}")
        print(f"History characters : {history_chars}")
        print(f"Prompt characters  : {prompt_chars}")
        print(f"Documents supplied : {len(documents)}")
        print(f"History turns      : {len(history)}")

        # ---------------------------------------------------------
        # LLM generation
        # ---------------------------------------------------------

        result = provider_chain.invoke(prompt)

        generation = result.content.strip()

        output_chars = len(generation)

        print(f"Output characters  : {output_chars}")

        return {
            "generation": generation,
            "trace": [{
                "stage": "generate",
                "question": state["question"],
                "context_chars": context_chars,
                "history_chars": history_chars,
                "prompt_chars": prompt_chars,
                "output_chars": output_chars,
                "history_turns": len(history),
                "answer": generation,
            }],
        }

# =============================================================
# Hallucination Check
# =============================================================

def check_hallucination(state: RAGState) -> dict:
    with tracker.measure("check_hallucination"):
        _separator("7. HALLUCINATION CHECK")

        generation = state["generation"]

        if is_refusal_answer(generation):
            print("Answer is a refusal ('I don't know' or similar) - skipping")
            print("the hallucination check entirely. A refusal makes no")
            print("factual claim, so there's nothing to verify as grounded.")
            return {
                "hallucination_grade": "grounded",
                "hallucination_retry_count": state.get("hallucination_retry_count", 0),
                "trace": [{
                    "stage": "check_hallucination",
                    "raw_grade": "skipped_refusal_short_circuit",
                    "normalized_grade": "grounded",
                    "hallucination_retry_count": state.get("hallucination_retry_count", 0),
                }],
            }

        documents = state.get("documents", [])
        context = "\n\n".join(d.page_content for d in documents)

        prompt = (
            "Is the following answer fully supported by the context below? "
            "Answer with exactly one word: 'grounded' or 'hallucinated'.\n\n"
            f"Context:\n{context}\n\n"
            f"Answer:\n{generation}"
        )

        result = fast_provider_chain.invoke(prompt)
        raw_grade = result.content.strip().lower()
        grade = (
            "grounded"
            if "grounded" in raw_grade and "hallucinated" not in raw_grade
            else "hallucinated"
        )

        hallucination_retry_count = state.get("hallucination_retry_count", 0)
        if grade == "hallucinated":
            hallucination_retry_count += 1

        return {
            "hallucination_grade": grade,
            "hallucination_retry_count": hallucination_retry_count,
            "trace": [{
                "stage": "check_hallucination",
                "raw_grade": raw_grade,
                "normalized_grade": grade,
                "hallucination_retry_count": hallucination_retry_count,
            }],
        }


# =============================================================
# Record Turn
# =============================================================

def record_turn(state: RAGState) -> dict:
    _separator("8. RECORD TURN")

    final_entry = {
        "stage": "record_turn",
        "final_route": "end",
        "retry_count": state.get("retry_count", 0),
        "retrieval_decision": state.get("retrieval_decision"),
        "retrieval_evidence_strength": state.get("retrieval_evidence_strength"),
        "retrieval_decision_reason": state.get("retrieval_decision_reason"),
    }

    full_trace = state.get("trace", []) + [final_entry]

    _separator("STRUCTURED TRACE SUMMARY (full request, end to end)")
    print(json.dumps(full_trace, indent=2, default=str))

    tracker.summary()

    return {
        "messages": [
            HumanMessage(content=state["question"]),
            AIMessage(content=state["generation"]),
        ],
        "trace": [final_entry],
    }