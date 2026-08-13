"""Application registry for ingested documents.

The registry is separate from the vector store. It answers application-level
questions such as which documents have been ingested and provides the same
document_id used by Pinecone retrieval.
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

_MIGRATE_TABLE = """
ALTER TABLE ingested_documents
ADD COLUMN IF NOT EXISTS document_id TEXT;
"""


def _connect():
    return psycopg.connect(settings.postgres_url, autocommit=True)


def _ensure_table(conn) -> None:
    conn.execute(_CREATE_TABLE)
    conn.execute(_MIGRATE_TABLE)


def record_ingestion(
    filename: str,
    chunk_count: int,
    document_id: str | None = None,
) -> None:
    with _connect() as conn:
        _ensure_table(conn)
        conn.execute(
            """
            INSERT INTO ingested_documents
                (document_id, filename, chunk_count, ingested_at)
            VALUES (%s, %s, %s, %s)
            """,
            (
                document_id,
                filename,
                chunk_count,
                datetime.now(timezone.utc),
            ),
        )


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
