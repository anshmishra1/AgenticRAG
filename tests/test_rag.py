"""Smoke test for the optimized corrective RAG graph."""
import uuid

from langgraph.checkpoint.postgres import PostgresSaver

from agentic_rag.config import settings
from agentic_rag.graph.builder import build_graph


def main() -> None:
    print("=" * 80)
    print("OPTIMIZED AGENTIC RAG GRAPH TEST")
    print("=" * 80)

    with PostgresSaver.from_conn_string(settings.postgres_url) as checkpointer:
        checkpointer.setup()
        graph = build_graph(checkpointer)

        session_id = f"rag-test-{uuid.uuid4().hex[:8]}"

        questions = [
            "What is the main topic of the document?",
            "Explain it in more detail.",
            "What are the key concepts discussed?",
        ]

        for idx, question in enumerate(questions, start=1):
            print("\n" + "=" * 80)
            print(f"QUESTION {idx}: {question}")
            print("=" * 80)

            config = {
                "configurable": {
                    "thread_id": f"{session_id}-q{idx}"
                }
            }

            initial_state = {
                "question": question,
                "document_id": None,
                "retrieval_query": None,
                "documents": [],
                "generation": None,
                "relevance_grade": None,
                "hallucination_grade": None,
                "retry_count": 0,
                "hallucination_retry_count": 0,
                "retrieval_scores": [],
                "trace": [],
            }

            result = graph.invoke(initial_state, config=config)

            print("\nANSWER:")
            print(result.get("generation"))

            print("\nRETRIEVAL DECISION:")
            print(result.get("retrieval_decision"))

            print("\nDECISION REASON:")
            print(result.get("retrieval_decision_reason"))

            print("\nEVIDENCE STRENGTH:")
            print(result.get("retrieval_evidence_strength"))

            print("\nRELEVANCE:")
            print(result.get("relevance_grade"))

            print("\nHALLUCINATION:")
            print(result.get("hallucination_grade"))

            print("\nRETRY COUNT:")
            print(result.get("retry_count"))

    print("\n" + "=" * 80)
    print("OPTIMIZED RAG TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
