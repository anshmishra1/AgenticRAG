"""Cross-encoder re-ranking for hybrid retrieval candidates.

Runs entirely locally (CPU), no LLM API calls or quota impact. Re-scores a
shortlist of hybrid-retrieved candidates by feeding (query, passage) pairs
into the model TOGETHER, rather than comparing independently-pooled
embeddings the way bi-encoder cosine similarity does. This is what actually
fixes the thin-margin problem exposed by retrieval calibration - topically
adjacent-but-wrong passages ("how to build a fine-tuning dataset" vs. an
unrelated fine-tuning mention) scored almost as high as genuine matches under
bi-encoder cosine similarity; a cross-encoder that directly models
word-level interaction between query and passage separates them far more
cleanly.

Raw ms-marco cross-encoder output is an unbounded logit, not a 0-1 score.
Sigmoid is applied manually here (numpy, not a library kwarg) since the exact
constructor/predict parameter name for built-in activation varies across
sentence-transformers versions - safer to compute it explicitly.
"""
from __future__ import annotations

import numpy as np
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from agentic_rag.config import settings

_cross_encoder: CrossEncoder | None = None


def _get_cross_encoder() -> CrossEncoder:
    global _cross_encoder
    if _cross_encoder is None:
        _cross_encoder = CrossEncoder(settings.cross_encoder_model)
    return _cross_encoder


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def rerank(
    query: str,
    candidates: list[tuple[Document, float]],
    top_k: int,
) -> list[tuple[Document, float]]:
    """Re-score candidates and print incoming RRF + raw/sigmoid CE scores."""
    if not candidates:
        print("\n" + "-" * 70)
        print("CROSS-ENCODER RERANKER")
        print("-" * 70)
        print("No candidates to rerank.")
        return []

    print("\n" + "-" * 70)
    print(f"CROSS-ENCODER RERANKER | candidates={len(candidates)} | top_k={top_k}")
    print("-" * 70)
    print(f"Model: {settings.cross_encoder_model}")

    pairs = [(query, doc.page_content) for doc, _ in candidates]
    raw_scores = np.asarray(_get_cross_encoder().predict(pairs))
    scores = _sigmoid(raw_scores)

    scored = []
    for original_rank, ((doc, incoming_rrf), raw_score, score) in enumerate(
        zip(candidates, raw_scores, scores), start=1
    ):
        scored.append({
            "original_rank": original_rank,
            "incoming_rrf": float(incoming_rrf),
            "raw_logit": float(raw_score),
            "cross_encoder_score": float(score),
            "doc": doc,
        })

    scored.sort(key=lambda item: item["cross_encoder_score"], reverse=True)

    for rerank_position, item in enumerate(scored, start=1):
        md = item["doc"].metadata
        print(
            f"[{rerank_position:02d}] "
            f"CE={item['cross_encoder_score']:.6f} | "
            f"logit={item['raw_logit']:.6f} | "
            f"RRF={item['incoming_rrf']:.8f} | "
            f"previous_rank={item['original_rank']} | "
            f"type={md.get('type')} | "
            f"page={md.get('page_label', md.get('page', '-'))}"
        )

    selected = scored[:top_k]
    print(f"Selected top {len(selected)} candidates after cross-encoder reranking.")
    print("-" * 70)

    return [(item["doc"], item["cross_encoder_score"]) for item in selected]
