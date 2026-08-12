import uuid
from langgraph.checkpoint.postgres import PostgresSaver

from agentic_rag.config import settings
from agentic_rag.graph.builder import build_graph
# Import tracker instance from your timing/core module
from agentic_rag.core.timing import PerformanceTracker

tracker = PerformanceTracker()

def main() -> None:

    print("=" * 80)
    print("AGENTIC RAG GRAPH TEST")
    print("=" * 80)

    print("\nConnecting to PostgreSQL...")

    with PostgresSaver.from_conn_string(
        settings.postgres_url
    ) as checkpointer:

        print("PostgreSQL connection established.")

        # Create checkpoint tables if they do not already exist.
        checkpointer.setup()

        print("Checkpoint tables verified.")

        # Build the graph
        graph = build_graph(checkpointer)

        print("LangGraph initialized.")

        # Base session prefix for isolation
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

            try:
                initial_state = {
                    "question": question,
                    "retrieval_query": None,
                    "documents": [],
                    "generation": None,
                    "relevance_grade": None,
                    "hallucination_grade": None,
                    "retry_count": 0,
                }

                # Measure the full graph invocation in PerformanceTracker
                with tracker.measure(f"graph_invoke_q{idx}"):
                    result = graph.invoke(initial_state, config=config)

                print("\nANSWER:")
                print(result.get("generation"))

                print("\nRETRIEVAL QUERY:")
                print(result.get("retrieval_query"))

                print("\nRELEVANCE:")
                print(result.get("relevance_grade"))

                print("\nHALLUCINATION:")
                print(result.get("hallucination_grade"))

                print("\nRETRY COUNT:")
                print(result.get("retry_count"))

                documents = result.get("documents", [])

                print("\nRETRIEVED DOCUMENTS:")
                print(len(documents))

            except Exception as exc:

                print("\nERROR:")
                print(type(exc).__name__)
                print(str(exc))

                raise

    # Print the aggregate execution breakdown across all pipeline steps and questions
    tracker.summary()

    print("\n" + "=" * 80)
    print("RAG TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()