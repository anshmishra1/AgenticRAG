"""Pinecone-backed vector store, with native hybrid (dense + sparse) support.

This bypasses langchain_pinecone's PineconeVectorStore for hybrid operations,
since that wrapper doesn't support sparse vectors - upsert and query here go
through the raw Pinecone SDK client instead. The index itself must be created
with metric="dotproduct" (see scripts/create_hybrid_index.py); cosine-metric
indexes cannot accept sparse vectors at all.
"""
from __future__ import annotations

import uuid

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

from agentic_rag.config import settings

_embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)

_pc: Pinecone | None = None
_index = None


def get_pinecone_index():
    """Raw Pinecone Index client (not the LangChain wrapper) - required for
    sparse_values support on upsert/query."""
    global _pc, _index
    if _index is None:
        _pc = Pinecone(api_key=settings.pinecone_api_key)
        _index = _pc.Index(settings.pinecone_index_name)
    return _index


def hybrid_scale(dense: list[float], sparse: dict, alpha: float) -> tuple[list[float], dict]:
    """Convex combination scaling for hybrid queries: alpha=1.0 is pure dense,
    alpha=0.0 is pure sparse. This is Pinecone's documented pattern for
    combining two differently-scaled score types into one query."""
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be between 0 and 1")
    scaled_sparse = {
        "indices": sparse["indices"],
        "values": [v * (1.0 - alpha) for v in sparse["values"]],
    }
    scaled_dense = [v * alpha for v in dense]
    return scaled_dense, scaled_sparse


def upsert_hybrid(chunks: list[Document], bm25_encoder) -> None:
    """Embeds each chunk's text with both the dense model and the fitted
    per-document BM25 encoder, then upserts both vector types together.
    Chunk text is duplicated into metadata["text"] since Pinecone matches
    only return metadata, not the original page_content."""
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
        vector_id = f"{doc_id}-{chunk_type}-{uuid.uuid4().hex[:12]}"

        vectors.append({
            "id": vector_id,
            "values": dense,
            "sparse_values": sparse,
            "metadata": metadata,
        })

    batch_size = 100
    for start in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[start:start + batch_size])


def retrieve_hybrid_with_scores(
    query: str,
    bm25_encoder,
    k: int,
    filter: dict | None = None,
    alpha: float | None = None,
) -> list[tuple[Document, float]]:
    """Hybrid dense+sparse retrieval when bm25_encoder is provided (normal,
    document-scoped case). Falls back to dense-only when bm25_encoder is None
    (the global/unscoped fallback path, where no single document's BM25 fit
    applies) - a dotproduct index accepts dense-only queries fine, sparse is
    optional per query even though the index supports it."""
    index = get_pinecone_index()
    dense_query = _embeddings.embed_query(query)

    if bm25_encoder is not None:
        alpha = settings.hybrid_alpha if alpha is None else alpha
        sparse_query = bm25_encoder.encode_queries(query)
        vector, sparse_vector = hybrid_scale(dense_query, sparse_query, alpha)
        result = index.query(
            vector=vector,
            sparse_vector=sparse_vector,
            top_k=k,
            filter=filter,
            include_metadata=True,
        )
    else:
        result = index.query(
            vector=dense_query,
            top_k=k,
            filter=filter,
            include_metadata=True,
        )

    pairs: list[tuple[Document, float]] = []
    for match in result["matches"]:
        metadata = dict(match["metadata"])
        text = metadata.pop("text", "")
        doc = Document(page_content=text, metadata=metadata)
        pairs.append((doc, float(match["score"])))
    return pairs