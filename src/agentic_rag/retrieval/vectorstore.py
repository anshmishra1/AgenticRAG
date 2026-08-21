"""Pinecone-backed vector store with explicit Dense + BM25 + RRF retrieval.

Retrieval stages are intentionally observable:
    Dense retrieval + BM25 sparse retrieval -> RRF -> cross-encoder reranking.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

from agentic_rag.config import settings

_embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
_pc: Pinecone | None = None
_index = None


@dataclass(frozen=True)
class QueryRepresentation:
    """Query-time representation computed once and reusable across searches."""

    dense: list[float]
    sparse: dict | None = None


def build_query_representation(query: str, bm25_encoder=None) -> QueryRepresentation:
    """Build dense and sparse query vectors exactly once per request."""
    dense = _embeddings.embed_query(query)
    sparse = bm25_encoder.encode_queries(query) if bm25_encoder is not None else None
    return QueryRepresentation(dense=dense, sparse=sparse)


def get_pinecone_index():
    global _pc, _index
    if _index is None:
        _pc = Pinecone(api_key=settings.pinecone_api_key)
        _index = _pc.Index(settings.pinecone_index_name)
    return _index


def _stable_chunk_id(doc_id: str, chunk_type: str, text: str) -> str:
    """Deterministic vector ID derived from the chunk's own content, not a
    random UUID. Pinecone's upsert() is idempotent by ID - same ID overwrites
    in place, a fresh random ID always creates a new entry. This is the fix
    for duplicate chunks: re-ingesting the same document now overwrites its
    existing vectors instead of piling up copies, since identical chunk text
    always hashes to the same ID.

    This was previously implemented, then dropped when this file was
    rewritten for the explicit Dense+BM25+RRF architecture - restoring it
    here, since random-UUID IDs regressed the duplicate-chunk bug."""
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    return f"{doc_id}-{chunk_type}-{content_hash}"


def upsert_hybrid(chunks: list[Document], bm25_encoder) -> None:
    index = get_pinecone_index()
    texts = [c.page_content for c in chunks]
    dense_vectors = _embeddings.embed_documents(texts)

    vectors = []
    for chunk, dense, text in zip(chunks, dense_vectors, texts):
        sparse = bm25_encoder.encode_documents(text)
        metadata = dict(chunk.metadata)
        metadata["text"] = text
        doc_id = metadata.get("document_id", "doc")
        chunk_type = metadata.get("type", "content")
        vector_id = _stable_chunk_id(doc_id, chunk_type, text)
        vectors.append({
            "id": vector_id,
            "values": dense,
            "sparse_values": sparse,
            "metadata": metadata,
        })

    batch_size = 100
    for start in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[start:start + batch_size])


def _match_to_document(match: Any) -> tuple[str, Document, float]:
    metadata = dict(match["metadata"] or {})
    text = metadata.pop("text", "")
    vector_id = str(match["id"])
    return vector_id, Document(page_content=text, metadata=metadata), float(match["score"])


def _rrf_fuse(dense_matches, sparse_matches, rrf_k: int):
    """Fuse two ranked lists with Reciprocal Rank Fusion.

    With deterministic vector IDs (see _stable_chunk_id above), the same
    chunk hit by both dense and sparse retrieval now correctly shares one
    vector_id and merges into a single fused entry here, as intended - that
    part of the dict-keyed-by-vector_id design was always correct. The
    text-based dedup pass below is a separate concern: a safety net against
    any duplicate vectors already sitting in the index from before this fix
    (old random-UUID uploads), which would still have distinct IDs for
    identical text and would otherwise fuse as separate candidates.
    """
    fused: dict[str, dict] = {}

    for rank, (vector_id, doc, score) in enumerate(dense_matches, start=1):
        fused[vector_id] = {
            "vector_id": vector_id,
            "doc": doc,
            "dense_rank": rank,
            "dense_score": score,
            "bm25_rank": None,
            "bm25_score": None,
        }

    for rank, (vector_id, doc, score) in enumerate(sparse_matches, start=1):
        if vector_id not in fused:
            fused[vector_id] = {
                "vector_id": vector_id,
                "doc": doc,
                "dense_rank": None,
                "dense_score": None,
                "bm25_rank": None,
                "bm25_score": None,
            }
        fused[vector_id]["bm25_rank"] = rank
        fused[vector_id]["bm25_score"] = score

    diagnostics = []
    for item in fused.values():
        rrf_score = 0.0
        if item["dense_rank"] is not None:
            rrf_score += 1.0 / (rrf_k + item["dense_rank"])
        if item["bm25_rank"] is not None:
            rrf_score += 1.0 / (rrf_k + item["bm25_rank"])
        item["rrf_score"] = rrf_score
        diagnostics.append(item)

    diagnostics.sort(key=lambda x: x["rrf_score"], reverse=True)

    # Defense-in-depth dedup by content, in case stale duplicate vectors from
    # before the deterministic-ID fix are still sitting in the index.
    seen_text: set[str] = set()
    deduped_diagnostics = []
    for item in diagnostics:
        text = item["doc"].page_content
        if text in seen_text:
            continue
        seen_text.add(text)
        deduped_diagnostics.append(item)

    results = [(x["doc"], float(x["rrf_score"])) for x in deduped_diagnostics]
    return results, deduped_diagnostics


def _print_retrieval_table(title: str, matches) -> None:
    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)
    if not matches:
        print("No candidates returned.")
        return
    for rank, (vector_id, doc, score) in enumerate(matches, start=1):
        md = doc.metadata
        page = md.get("page_label", md.get("page", "-"))
        print(f"[{rank:02d}] score={score:.6f} | type={md.get('type')} | page={page} | id={vector_id}")


def _print_rrf_table(diagnostics) -> None:
    print("\n" + "-" * 70)
    print("3. RRF FUSION")
    print("-" * 70)
    if not diagnostics:
        print("No candidates available for RRF.")
        return
    for rank, item in enumerate(diagnostics, start=1):
        ds = f"{item['dense_score']:.6f}" if item["dense_score"] is not None else "-"
        bs = f"{item['bm25_score']:.6f}" if item["bm25_score"] is not None else "-"
        md = item["doc"].metadata
        page = md.get("page_label", md.get("page", "-"))
        print(
            f"[{rank:02d}] RRF={item['rrf_score']:.8f} | "
            f"DenseRank={item['dense_rank'] or '-'} | DenseScore={ds} | "
            f"BM25Rank={item['bm25_rank'] or '-'} | BM25Score={bs} | "
            f"type={md.get('type')} | page={page}"
        )


def retrieve_hybrid_with_scores(
    query: str,
    bm25_encoder,
    k: int,
    filter: dict | None = None,
    alpha: float | None = None,
    query_representation: QueryRepresentation | None = None,
):
    """Retrieve Dense + BM25 separately, fuse with RRF, and return diagnostics.

    ``query_representation`` is optional for backwards compatibility. When it
    is supplied, dense and sparse query encodings are reused instead of being
    recomputed for every overview/content search.
    """
    index = get_pinecone_index()
    representation = query_representation or build_query_representation(query, bm25_encoder)
    dense_query = representation.dense

    print("\n" + "=" * 70)
    print("HYBRID RETRIEVAL: DENSE + BM25 + RRF")
    print("=" * 70)
    print(f"Query: {query}")
    print(f"Candidate k per retriever: {k}")
    print(f"RRF k: {settings.rrf_k}")
    print(f"Document filter: {filter}")

    dense_result = index.query(
        vector=dense_query,
        top_k=k,
        filter=filter,
        include_metadata=True,
    )
    dense_matches = [_match_to_document(m) for m in dense_result["matches"]]
    _print_retrieval_table("1. DENSE RETRIEVAL", dense_matches)

    sparse_matches = []
    if bm25_encoder is not None and representation.sparse is not None:
        sparse_query = representation.sparse
        zero_dense = [0.0] * len(dense_query)
        sparse_result = index.query(
            vector=zero_dense,
            sparse_vector=sparse_query,
            top_k=k,
            filter=filter,
            include_metadata=True,
        )
        sparse_matches = [_match_to_document(m) for m in sparse_result["matches"]]
        _print_retrieval_table("2. BM25 / SPARSE RETRIEVAL", sparse_matches)
        print(f"BM25 query terms encoded: {len(sparse_query.get('indices', []))}")
    else:
        print("\n" + "-" * 70)
        print("2. BM25 / SPARSE RETRIEVAL")
        print("-" * 70)
        print("SKIPPED - no document-specific BM25 encoder available.")

    if bm25_encoder is not None and representation.sparse is not None:
        fused_results, rrf_diagnostics = _rrf_fuse(dense_matches, sparse_matches, settings.rrf_k)
    else:
        seen_text: set[str] = set()
        fused_results = []
        rrf_diagnostics = []
        for rank, (vector_id, doc, score) in enumerate(dense_matches, start=1):
            if doc.page_content in seen_text:
                continue
            seen_text.add(doc.page_content)
            rrf_score = 1.0 / (settings.rrf_k + rank)
            fused_results.append((doc, rrf_score))
            rrf_diagnostics.append({
                "vector_id": vector_id,
                "doc": doc,
                "dense_rank": rank,
                "dense_score": score,
                "bm25_rank": None,
                "bm25_score": None,
                "rrf_score": rrf_score,
            })

    _print_rrf_table(rrf_diagnostics)
    fused_results = fused_results[:k]

    print("\n" + "-" * 70)
    print(f"RRF OUTPUT: {len(fused_results)} candidates")
    print("-" * 70)
    for rank, (doc, score) in enumerate(fused_results, start=1):
        md = doc.metadata
        print(f"[{rank:02d}] RRF={score:.8f} | type={md.get('type')} | page={md.get('page_label', md.get('page', '-'))}")

    diagnostics = {
        "query": query,
        "candidate_k": k,
        "rrf_k": settings.rrf_k,
        "hybrid_alpha": alpha if alpha is not None else settings.hybrid_alpha,
        "dense_count": len(dense_matches),
        "bm25_count": len(sparse_matches),
        "rrf_count": len(fused_results),
        "dense": [
            {"rank": r, "vector_id": vid, "score": score,
             "type": doc.metadata.get("type"),
             "page": doc.metadata.get("page_label", doc.metadata.get("page"))}
            for r, (vid, doc, score) in enumerate(dense_matches, start=1)
        ],
        "bm25": [
            {"rank": r, "vector_id": vid, "score": score,
             "type": doc.metadata.get("type"),
             "page": doc.metadata.get("page_label", doc.metadata.get("page"))}
            for r, (vid, doc, score) in enumerate(sparse_matches, start=1)
        ],
        "rrf": [
            {"rank": r, "vector_id": item["vector_id"],
             "rrf_score": item["rrf_score"],
             "dense_rank": item["dense_rank"], "dense_score": item["dense_score"],
             "bm25_rank": item["bm25_rank"], "bm25_score": item["bm25_score"],
             "type": item["doc"].metadata.get("type"),
             "page": item["doc"].metadata.get("page_label", item["doc"].metadata.get("page"))}
            for r, item in enumerate(rrf_diagnostics[:k], start=1)
        ],
    }

    return fused_results, diagnostics