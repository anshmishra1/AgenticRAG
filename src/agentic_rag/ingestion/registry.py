"""Application registry for ingested documents.

The registry is separate from the vector store. It answers application-level
questions such as which documents have been ingested, provides the same
document_id used by Pinecone retrieval, and - since the hybrid-search change -
stores each document's fitted BM25 parameters so query time can reconstruct
the exact same encoder used at ingestion time.
"""

from datetime import datetime, timezone

import psycopg

from agentic_rag.config import settings


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS ingested_documents (
    id SERIAL PRIMARY KEY,
    document_id TEXT,
    filename TEXT NOT NULL,
    chunk_count INTEGER NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL
);
"""

_MIGRATE_DOCUMENT_ID = """
ALTER TABLE ingested_documents
ADD COLUMN IF NOT EXISTS document_id TEXT;
"""

_MIGRATE_BM25_PARAMS = """
ALTER TABLE ingested_documents
ADD COLUMN IF NOT EXISTS bm25_params TEXT;
"""


def _connect():
    return psycopg.connect(settings.postgres_url, autocommit=True)


def _ensure_table(conn) -> None:
    conn.execute(_CREATE_TABLE)
    conn.execute(_MIGRATE_DOCUMENT_ID)
    conn.execute(_MIGRATE_BM25_PARAMS)


def record_ingestion(
    filename: str,
    chunk_count: int,
    document_id: str | None = None,
    bm25_params: str | None = None,
) -> None:
    with _connect() as conn:
        _ensure_table(conn)
        conn.execute(
            """
            INSERT INTO ingested_documents
                (document_id, filename, chunk_count, ingested_at, bm25_params)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                document_id,
                filename,
                chunk_count,
                datetime.now(timezone.utc),
                bm25_params,
            ),
        )


def get_bm25_params(document_id: str) -> str | None:
    """Returns the JSON-serialized BM25 params for a document_id, or None if
    the document predates the hybrid-search change (ingested before this
    column existed) or wasn't found."""
    with _connect() as conn:
        _ensure_table(conn)
        row = conn.execute(
            """
            SELECT bm25_params
            FROM ingested_documents
            WHERE document_id = %s
            ORDER BY ingested_at DESC
            LIMIT 1
            """,
            (document_id,),
        ).fetchone()
    return row[0] if row and row[0] else None


def list_documents() -> list[dict]:
    with _connect() as conn:
        _ensure_table(conn)
        rows = conn.execute(
            """
            SELECT document_id, filename, chunk_count, ingested_at
            FROM ingested_documents
            ORDER BY ingested_at DESC
            """
        ).fetchall()

    return [
        {
            "document_id": r[0],
            "filename": r[1],
            "chunk_count": r[2],
            "ingested_at": r[3].isoformat(),
        }
        for r in rows
    ]