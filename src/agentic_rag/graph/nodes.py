"""Node functions for the corrective RAG pipeline.

Every node prints diagnostic information as it runs, appends a small entry to state["trace"],
and measures execution time using PerformanceTracker.
"""
import json
import logging

from langchain_core.messages import AIMessage, HumanMessage

from agentic_rag.graph.state import RAGState
from agentic_rag.llm.provider import provider_chain, fast_provider_chain
from agentic_rag.retrieval.vectorstore import get_overview_retriever, get_retriever, retrieve_with_scores
from agentic_rag.graph.query_utils import is_likely_follow_up
from agentic_rag.retrieval.confidence import classify_retrieval_confidence
from agentic_rag.core.timing import PerformanceTracker

logger = logging.getLogger(__name__)
tracker = PerformanceTracker()


# =============================================================
# Debug helpers
# =============================================================

def _separator(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def _preview(text: str, length: int = 500) -> str:
    text = text.replace("\n", " ")
    return text[:length]


# =============================================================
# Contextualize Question
# =============================================================

def contextualize_question(state: RAGState) -> dict:
    """Contextualize only high-confidence follow-up questions."""
    tracker = PerformanceTracker()
    with tracker.measure("contextualize_question"):
        history = state.get("messages", [])[-6:]
        question = state["question"]

        if not history or not is_likely_follow_up(question, history):
            return {
                "retrieval_query": question,
            }

        history_text = "\n".join(
            f"{m.type}: {m.content}"
            for m in history
        )

        prompt = (
            "Given this conversation history and a follow-up input, "
            "rewrite the follow-up into a standalone search query about "
            "the document's content. "
            "Return only the rewritten query, nothing else.\n\n"
            f"History:\n{history_text}\n\n"
            f"Follow-up: {question}"
        )

        result = provider_chain.invoke(prompt)

        return {
            "retrieval_query": result.content.strip(),
            "trace": [{
                "stage": "contextualize_question",
                "question": question,
                "history_turns": len(history),
            }],
        }


# =============================================================
# Retrieval
# =============================================================

def calculate_retrieval_metrics(scores: list[float]) -> dict:
    if not scores:
        return {
            "top_score": 0.0,
            "second_score": 0.0,
            "score_gap": 0.0,
            "mean_score": 0.0,
        }

    ordered = sorted(scores, reverse=True)
    top_score = ordered[0]
    second_score = ordered[1] if len(ordered) > 1 else ordered[0]

    return {
        "top_score": top_score,
        "second_score": second_score,
        "score_gap": top_score - second_score,
        "mean_score": sum(scores) / len(scores),
    }


def retrieve(state: RAGState) -> dict:
    tracker = PerformanceTracker()
    with tracker.measure("retrieve"):
        _separator("2. RETRIEVAL")

        query = state.get("retrieval_query") or state["question"]
        print(f"Query sent to retriever:\n{query}")

        overview_results = retrieve_with_scores(
            query=query,
            k=2,
            filter={"type": {"$eq": "overview"}},
        )

        content_results = retrieve_with_scores(
            query=query,
            k=5,
        )

        results = overview_results + content_results
        results.sort(key=lambda item: float(item[1]), reverse=True)

        docs = [doc for doc, _ in results]
        scores = [float(score) for _, score in results]

        overview_docs_count = len(overview_results)
        content_docs_count = len(content_results)
        top_score = max(scores) if scores else 0.0
        confidence = classify_retrieval_confidence(scores)

        print(f"\nOverview chunks retrieved: {overview_docs_count}")
        print(f"Content chunks retrieved: {content_docs_count}")

        if not docs:
            print("WARNING: No documents were retrieved.")

        for i, doc in enumerate(docs, start=1):
            print("\n" + "-" * 60)
            print(f"DOCUMENT {i}")
            print(f"Similarity score: {scores[i - 1]}")
            print(f"Metadata: {doc.metadata}")
            print(f"\nContent preview:\n{_preview(doc.page_content)}")

        metrics = calculate_retrieval_metrics(scores)

        logger.info(
            "RETRIEVAL | query=%r | scores=%s | top=%.4f | second=%.4f | gap=%.4f | mean=%.4f",
            query,
            [round(score, 4) for score in scores],
            metrics["top_score"],
            metrics["second_score"],
            metrics["score_gap"],
            metrics["mean_score"],
        )

        return {
            "documents": docs,
            "retrieval_scores": scores,
            "retrieval_top_score": top_score,
            "retrieval_confidence": confidence,
            "trace": [
                {
                    "stage": "retrieve",
                    "retrieval_query": query,
                    "overview_docs": overview_docs_count,
                    "content_docs": content_docs_count,
                    "sources": [d.metadata.get("source") for d in docs],
                    "scores": scores,
                    "top_score": top_score,
                    "retrieval_confidence": confidence,
                }
            ],
        }


# =============================================================
# Document Grading
# =============================================================

def grade_documents(state: RAGState) -> dict:
    tracker = PerformanceTracker()
    with tracker.measure("grade_documents"):
        _separator("3. DOCUMENT RELEVANCE GRADING")

        documents = state.get("documents", [])
        query = state.get("retrieval_query") or state["question"]

        print(f"Question/query being graded:\n{query}")
        print(f"Number of retrieved documents: {len(documents)}")

        preview = [d.page_content[:300] for d in documents]

        prompt = (
            "You grade whether retrieved context is relevant to a question. "
            "Answer with exactly one word: 'relevant' or 'irrelevant'.\n\n"
            f"Question: {query}\n"
            f"Context: {preview}"
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
                "raw_grade": raw_grade,
                "normalized_grade": grade,
            }],
        }


# =============================================================
# Query Rewrite
# =============================================================

def rewrite_query(state: RAGState) -> dict:
    tracker = PerformanceTracker()
    with tracker.measure("rewrite_query"):
        _separator("4. QUERY REWRITE")

        current = state.get("retrieval_query") or state["question"]
        retry_count = state.get("retry_count", 0)

        prompt = (
            "Rewrite this search query to be clearer and better suited for "
            "semantic search. Return only the rewritten query, nothing else.\n\n"
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
    tracker = PerformanceTracker()
    with tracker.measure("generate"):
        _separator("5. GENERATION")

        documents = state.get("documents", [])
        context = "\n\n".join(d.page_content for d in documents)
        history = state.get("messages", [])[-6:]
        history_text = (
            "\n".join(f"{m.type}: {m.content}" for m in history)
            if history else "None"
        )

        prompt = (
            "Answer the question using only the provided context and prior conversation. "
            "Follow the user's requested level of detail, structure, and style. "
            "If the user asks for a detailed explanation, provide a detailed explanation. "
            "If the user asks for a concise answer, keep it concise. "
            "If the answer isn't supported by the context, say you don't know. "
            "Do not omit important details needed to properly answer the question.\n\n"
            f"Prior conversation:\n{history_text}\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {state['question']}"
        )

        result = provider_chain.invoke(prompt)
        generation = result.content.strip()

        return {
            "generation": generation,
            "trace": [{
                "stage": "generate",
                "question": state["question"],
                "context_chars": len(context),
                "history_turns": len(history),
                "answer": generation,
            }],
        }


# =============================================================
# Hallucination Check
# =============================================================

def check_hallucination(state: RAGState) -> dict:
    tracker = PerformanceTracker()
    with tracker.measure("check_hallucination"):
        _separator("6. HALLUCINATION CHECK")

        documents = state.get("documents", [])
        context = "\n\n".join(d.page_content for d in documents)
        generation = state["generation"]

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

        return {
            "hallucination_grade": grade,
            "trace": [{
                "stage": "check_hallucination",
                "raw_grade": raw_grade,
                "normalized_grade": grade,
            }],
        }


# =============================================================
# Record Turn
# =============================================================

def record_turn(state: RAGState) -> dict:
    _separator("7. RECORD TURN")

    final_entry = {
        "stage": "record_turn",
        "final_route": "end",
        "retry_count": state.get("retry_count", 0),
    }

    full_trace = state.get("trace", []) + [final_entry]

    _separator("STRUCTURED TRACE SUMMARY (full request, end to end)")
    print(json.dumps(full_trace, indent=2, default=str))

    # Print the full timing summary across measured pipeline nodes
    tracker.summary()

    return {
        "messages": [
            HumanMessage(content=state["question"]),
            AIMessage(content=state["generation"]),
        ],
        "trace": [final_entry],
    }