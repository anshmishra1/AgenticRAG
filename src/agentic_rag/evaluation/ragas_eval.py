"""Runs a small question set through the LIVE graph and scores the results
with RAGAS (faithfulness, answer relevancy, context precision).

This answers a different question than calibrate_retrieval.py: not "what
threshold should the retrieval floor be" (that's arithmetic on scores you
already have), but "after changing the retrieval/generation policy, did
answer quality actually hold up, or did we just trade one failure mode for
another". This is the regression-test role RAGAS is actually built for.

Run this after any change to policies/retrieval.py or policies/generation.py,
before merging - not on every request (it's slow and costs LLM judge calls,
which is exactly why it isn't wired into the live /query path).

Requires: a running Postgres checkpointer connection (same POSTGRES_URL as
the app) and at least one already-ingested document.

Usage:
    Fill in EVAL_SET below (same document_id source as calibrate_retrieval.py),
    then: python scripts/run_ragas_eval.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from langgraph.checkpoint.postgres import PostgresSaver

from agentic_rag.config import settings
from agentic_rag.evaluation.ragas_eval import run_eval
from agentic_rag.graph.builder import build_graph

# (document_id, question, expected_ground_truth_or_None)
EVAL_SET = [
    (
        "8b8f659beda18f55ab82191bde2d0d8090ae73925b2c7ea3e8d9171857cc506a",
        "What are the scaling laws in large language models?",
        None,
    ),
    (
        "92f92d40c9b94deefa0d98d0c384a0402755d69cf7485641513fc8bbeb968d21",
        "What are the different types of LLM?",
        None,  # expected to correctly refuse - this is the regression case
    ),
]


def main() -> None:
    if len(EVAL_SET) < 2:
        print("EVAL_SET is empty or too small. Fill it in before running.")
        return

    with PostgresSaver.from_conn_string(settings.postgres_url) as checkpointer:
        checkpointer.setup()
        rag_graph = build_graph(checkpointer)

        questions, answers, contexts, ground_truths = [], [], [], []
        has_ground_truth = all(gt is not None for _, _, gt in EVAL_SET)

        for i, (document_id, question, ground_truth) in enumerate(EVAL_SET):
            config = {"configurable": {"thread_id": f"ragas-eval-{i}"}}
            result = rag_graph.invoke(
                {"question": question, "document_id": document_id, "retry_count": 0},
                config=config,
            )
            questions.append(question)
            answers.append(result.get("generation", ""))
            contexts.append([d.page_content for d in result.get("documents", [])])
            if ground_truth is not None:
                ground_truths.append(ground_truth)

            print(f"[{i + 1}/{len(EVAL_SET)}] {question}")
            print(f"  -> {result.get('generation', '')[:150]}")

        print("\n" + "=" * 70)
        print("RUNNING RAGAS EVALUATION")
        print("=" * 70)

        scores = run_eval(
            questions=questions,
            answers=answers,
            contexts=contexts,
            ground_truths=ground_truths if has_ground_truth else None,
        )

        for row in scores:
            print(row)


if __name__ == "__main__":
    main()