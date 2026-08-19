"""One-time setup: creates a NEW Pinecone index configured for hybrid search
(metric='dotproduct' - required for sparse+dense vectors together; cosine
indexes cannot accept sparse vectors at all).

This does NOT touch or delete the existing index. Hybrid search needs vectors
upserted with sparse components, and anything already in the old index lacks
them - there's no in-place conversion, only a fresh index plus re-ingestion.

Steps:
    1. Run this script.
    2. Update PINECONE_INDEX_NAME in .env to the new index's name.
    3. Restart the app and re-ingest every document through the normal
       upload flow - old data does not carry over automatically.
    4. Once you've confirmed everything works, delete the old index yourself
       from the Pinecone console if you want to reclaim the free-tier slot.

Run: python scripts/create_hybrid_index.py
"""
from pinecone import Pinecone, ServerlessSpec

from agentic_rag.config import settings

EMBEDDING_DIMENSION = 384  # matches all-MiniLM-L6-v2 (settings.embedding_model)


def main() -> None:
    pc = Pinecone(api_key=settings.pinecone_api_key)
    existing = [idx["name"] for idx in pc.list_indexes()]

    target_name = settings.pinecone_index_name

    if target_name in existing:
        print(f"Index '{target_name}' already exists.")
        print("If this is the ORIGINAL index (created with metric='cosine'),")
        print("hybrid search will not work against it - sparse vectors require")
        print("metric='dotproduct'. Set PINECONE_INDEX_NAME in .env to a new,")
        print("not-yet-existing name (e.g. 'agentic-rag-hybrid') and re-run.")
        return

    pc.create_index(
        name=target_name,
        dimension=EMBEDDING_DIMENSION,
        metric="dotproduct",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print(f"Created hybrid-capable index '{target_name}' (metric=dotproduct, dim={EMBEDDING_DIMENSION}).")
    print("Next: re-ingest every document through the app - the old index's")
    print("data does not carry over, since it has no sparse vectors.")


if __name__ == "__main__":
    main()