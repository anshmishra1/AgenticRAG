"""One-time setup: creates the Pinecone index if it doesn't already exist.
Run this once before the first query: python scripts/create_index.py
"""
from pinecone import Pinecone, ServerlessSpec

from agentic_rag.config import settings

# all-MiniLM-L6-v2 (the embedding model in config.py) outputs 384-dim vectors.
# If you change embedding_model later, this number must change to match.
EMBEDDING_DIMENSION = 384


def main() -> None:
    pc = Pinecone(api_key=settings.pinecone_api_key)
    existing = [idx["name"] for idx in pc.list_indexes()]

    if settings.pinecone_index_name in existing:
        print(f"Index '{settings.pinecone_index_name}' already exists — nothing to do.")
        return

    pc.create_index(
        name=settings.pinecone_index_name,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print(f"Created index '{settings.pinecone_index_name}' with dimension {EMBEDDING_DIMENSION}.")


if __name__ == "__main__":
    main()
