"""Pinecone-backed vector store."""

from __future__ import annotations

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from agentic_rag.config import settings


_embeddings = HuggingFaceEmbeddings(
    model_name=settings.embedding_model
)


def get_vectorstore() -> PineconeVectorStore:
    return PineconeVectorStore(
        index_name=settings.pinecone_index_name,
        embedding=_embeddings,
        pinecone_api_key=settings.pinecone_api_key,
    )


def retrieve_with_scores(
    query: str,
    k: int = 5,
    filter: dict | None = None,
) -> list[tuple]:
    """Retrieve documents together with similarity scores."""

    vectorstore = get_vectorstore()

    return vectorstore.similarity_search_with_score(
        query,
        k=k,
        filter=filter,
    )
