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
    """Re-rank hybrid candidates with the cross-encoder.

    The incoming score is preserved as RRF metadata.
    The cross-encoder score remains the returned score so the existing
    retrieval/graph contract is not changed in this stage.
    """

    if not candidates:
        print("\n" + "-" * 70)
        print("CROSS-ENCODER RERANKER")
        print("-" * 70)
        print("No candidates to rerank.")
        return []

    print("\n" + "-" * 70)
    print(
        f"CROSS-ENCODER RERANKER | "
        f"candidates={len(candidates)} | top_k={top_k}"
    )
    print("-" * 70)
    print(f"Model: {settings.cross_encoder_model}")

    pairs = [
        (query, doc.page_content)
        for doc, _ in candidates
    ]

    raw_scores = np.asarray(
        _get_cross_encoder().predict(pairs)
    )

    scores = _sigmoid(raw_scores)

    scored_candidates = []

    for original_rank, (
        (doc, rrf_score),
        raw_score,
        ce_score,
    ) in enumerate(
        zip(candidates, raw_scores, scores),
        start=1,
    ):
        # Do not overwrite the existing retrieval score contract.
        # Preserve all retrieval-stage information in metadata.
        doc.metadata["_retrieval_rrf_score"] = float(rrf_score)
        doc.metadata["_cross_encoder_logit"] = float(raw_score)
        doc.metadata["_cross_encoder_score"] = float(ce_score)
        doc.metadata["_reranker_previous_rank"] = original_rank

        scored_candidates.append(
            (
                doc,
                float(ce_score),
                float(rrf_score),
                float(raw_score),
                original_rank,
            )
        )

    scored_candidates.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    for rerank_position, (
        doc,
        ce_score,
        rrf_score,
        raw_score,
        original_rank,
    ) in enumerate(
        scored_candidates,
        start=1,
    ):
        metadata = doc.metadata

        print(
            f"[{rerank_position:02d}] "
            f"CE={ce_score:.6f} | "
            f"logit={raw_score:.6f} | "
            f"RRF={rrf_score:.8f} | "
            f"previous_rank={original_rank} | "
            f"type={metadata.get('type')} | "
            f"page={metadata.get('page_label', metadata.get('page', '-'))}"
        )

    selected = scored_candidates[:top_k]

    print(
        f"Selected top {len(selected)} candidates "
        f"after cross-encoder reranking."
    )
    print("-" * 70)

    return [
        (doc, ce_score)
        for (
            doc,
            ce_score,
            _rrf_score,
            _raw_score,
            _original_rank,
        ) in selected
    ]