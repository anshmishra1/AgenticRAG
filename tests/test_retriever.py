"""
Focused integration test for the retrieval layer.

Tests:
1. Overview retrieval
2. Content retrieval
3. Similarity scores
4. Combined ranking
5. Retrieval metrics
6. Retrieval confidence
7. Retrieval trace
"""

from agentic_rag.graph.nodes import retrieve


def main():
    print("=" * 70)
    print("RETRIEVAL LAYER TEST")
    print("=" * 70)

    question = "What is a large language model?"

    state = {
        "question": question,
        "retrieval_query": question,
        "retry_count": 0,
        "messages": [],
    }

    print(f"\nQuestion:")
    print(question)

    print("\nRunning retrieve()...\n")

    result = retrieve(state)

    print("\n" + "=" * 70)
    print("RETRIEVAL RESULT")
    print("=" * 70)

    documents = result.get("documents", [])
    scores = result.get("retrieval_scores", [])

    print(f"\nDocuments retrieved : {len(documents)}")
    print(f"Scores returned     : {len(scores)}")
    print(f"Top score           : {result.get('retrieval_top_score')}")
    print(f"Confidence          : {result.get('retrieval_confidence')}")

    print("\nScores:")
    for i, score in enumerate(scores, start=1):
        print(f"  {i}. {score:.6f}")

    print("\nDocument metadata:")

    for i, doc in enumerate(documents, start=1):
        print(f"\n--- Document {i} ---")
        print(f"Score    : {scores[i - 1]:.6f}")
        print(f"Metadata : {doc.metadata}")
        print(f"Preview  : {doc.page_content[:200].replace(chr(10), ' ')}...")

    print("\n" + "=" * 70)
    print("TRACE")
    print("=" * 70)

    for item in result.get("trace", []):
        print(item)

    print("\n" + "=" * 70)
    print("BASIC VALIDATION")
    print("=" * 70)

    assert "documents" in result, "Missing 'documents'"
    assert "retrieval_scores" in result, "Missing 'retrieval_scores'"
    assert "retrieval_top_score" in result, "Missing 'retrieval_top_score'"
    assert "retrieval_confidence" in result, "Missing 'retrieval_confidence'"
    assert "trace" in result, "Missing 'trace'"

    assert len(documents) == len(scores), (
        f"Document/score mismatch: "
        f"{len(documents)} documents vs {len(scores)} scores"
    )

    assert len(documents) > 0, "No documents were retrieved"

    assert all(isinstance(score, float) for score in scores), (
        "Not all retrieval scores are floats"
    )

    assert scores == sorted(scores, reverse=True), (
        "Documents are not sorted by descending similarity score"
    )

    assert result["retrieval_top_score"] == max(scores), (
        "Top score does not match the maximum retrieval score"
    )

    assert result["retrieval_confidence"] in {
        "low",
        "uncalibrated",
    }, (
        f"Unexpected confidence value: "
        f"{result['retrieval_confidence']}"
    )

    print("\n✅ All retrieval assertions passed.")

    print("\n" + "=" * 70)
    print("RETRIEVAL TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()