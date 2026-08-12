"""RAGAS-based evaluation harness: faithfulness, answer relevancy, context precision/recall."""
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy, context_precision, context_recall, faithfulness


def run_eval(
    questions: list[str],
    answers: list[str],
    contexts: list[list[str]],
    ground_truths: list[str] | None = None,
) -> list[dict]:
    data = {"question": questions, "answer": answers, "contexts": contexts}
    metrics = [faithfulness, answer_relevancy, context_precision]

    if ground_truths:
        data["ground_truth"] = ground_truths
        metrics.append(context_recall)

    dataset = Dataset.from_dict(data)
    result = evaluate(dataset, metrics=metrics)
    return result.to_pandas().to_dict(orient="records")
