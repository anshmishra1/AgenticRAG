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


def get_retriever(k: int = 5):
    """Existing retriever kept for compatibility."""

    return get_vectorstore().as_retriever(
        search_kwargs={"k": k}
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


def get_overview_retriever(k: int = 5):
    """Retrieve only whole-document overview chunks."""

    return get_vectorstore().as_retriever(
        search_kwargs={
            "k": k,
            "filter": {
                "type": {"$eq": "overview"}
            },
        }
    )