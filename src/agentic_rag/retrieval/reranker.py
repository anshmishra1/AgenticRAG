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

import time
import numpy as np
import torch
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from agentic_rag.config import settings

_cross_encoder: CrossEncoder | None = None


def _resolve_device() -> str:
    configured = getattr(settings, "cross_encoder_device", "auto")
    if configured != "auto":
        return configured
    return "cuda" if torch.cuda.is_available() else "cpu"


def _get_cross_encoder() -> CrossEncoder:
    global _cross_encoder
    if _cross_encoder is None:
        device = _resolve_device()
        print(f"CROSS-ENCODER DEVICE: {device}")
        _cross_encoder = CrossEncoder(
            settings.cross_encoder_model,
            device=device,
        )
    return _cross_encoder


def warmup_cross_encoder() -> None:
    """Load and warm the local reranker during application startup."""
    start = time.perf_counter()
    model = _get_cross_encoder()
    model.predict(
        [("warmup query", "warmup passage")],
        batch_size=1,
        show_progress_bar=False,
    )
    elapsed = time.perf_counter() - start
    print("\n" + "=" * 70)
    print("CROSS-ENCODER WARM-UP")
    print("=" * 70)
    print(f"Model: {settings.cross_encoder_model}")
    print(f"Device: {_resolve_device()}")
    print(f"Warm-up time: {elapsed:.2f} sec")
    print("Status: READY")


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def rerank_many(
    query: str,
    candidate_groups: dict[str, list[tuple[Document, float]]],
    top_k_by_group: dict[str, int],
) -> dict[str, list[tuple[Document, float]]]:
    """Rerank multiple candidate groups in one cross-encoder inference batch."""
    non_empty = {name: candidates for name, candidates in candidate_groups.items() if candidates}
    if not non_empty:
        return {name: [] for name in candidate_groups}

    print("\n" + "-" * 70)
    print("CROSS-ENCODER RERANKER | BATCHED GROUPS")
    print("-" * 70)
    print(f"Model: {settings.cross_encoder_model}")
    print(f"Device: {_resolve_device()}")
    print(f"Groups: {', '.join(non_empty)}")
    print(f"Total candidates: {sum(len(v) for v in non_empty.values())}")

    flattened: list[tuple[str, int, Document, float]] = []
    pairs = []
    for group_name, candidates in non_empty.items():
        for original_rank, (doc, incoming_rrf) in enumerate(candidates, start=1):
            flattened.append((group_name, original_rank, doc, incoming_rrf))
            pairs.append((query, doc.page_content))

    start_time = time.perf_counter()
    raw_scores = np.asarray(
        _get_cross_encoder().predict(
            pairs,
            batch_size=getattr(settings, "cross_encoder_batch_size", 32),
            show_progress_bar=False,
        )
    )
    elapsed = time.perf_counter() - start_time
    scores = _sigmoid(raw_scores)

    grouped: dict[str, list[dict]] = {name: [] for name in candidate_groups}
    for (group_name, original_rank, doc, incoming_rrf), raw_score, score in zip(
        flattened, raw_scores, scores
    ):
        item = {
            "original_rank": original_rank,
            "incoming_rrf": float(incoming_rrf),
            "raw_logit": float(raw_score),
            "cross_encoder_score": float(score),
            "doc": doc,
        }
        grouped[group_name].append(item)

        # Preserve the diagnostics in document metadata for downstream tracing.
        doc.metadata["_retrieval_rrf_score"] = float(incoming_rrf)
        doc.metadata["_cross_encoder_logit"] = float(raw_score)
        doc.metadata["_cross_encoder_score"] = float(score)

    print(f"Inference time: {elapsed:.3f} sec")
    print(f"Batch size: {getattr(settings, 'cross_encoder_batch_size', 32)}")

    results: dict[str, list[tuple[Document, float]]] = {}
    for group_name, items in grouped.items():
        items.sort(key=lambda item: item["cross_encoder_score"], reverse=True)
        print(f"\n[{group_name.upper()}]")
        for rank, item in enumerate(items, start=1):
            md = item["doc"].metadata
            print(
                f"[{rank:02d}] CE={item['cross_encoder_score']:.6f} | "
                f"logit={item['raw_logit']:.6f} | "
                f"RRF={item['incoming_rrf']:.8f} | "
                f"previous_rank={item['original_rank']} | "
                f"type={md.get('type')} | "
                f"page={md.get('page_label', md.get('page', '-'))}"
            )

        top_k = top_k_by_group.get(group_name, len(items))
        selected = items[:top_k]
        results[group_name] = [
            (item["doc"], item["cross_encoder_score"]) for item in selected
        ]
        print(f"Selected top {len(selected)} {group_name} candidates.")

    print("-" * 70)
    return results


def rerank(
    query: str,
    candidates: list[tuple[Document, float]],
    top_k: int,
) -> list[tuple[Document, float]]:
    """Backward-compatible single-group reranking wrapper."""
    return rerank_many(
        query,
        {"candidates": candidates},
        {"candidates": top_k},
    )["candidates"]

