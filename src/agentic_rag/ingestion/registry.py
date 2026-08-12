"""Tracks what's been ingested. This is deliberately NOT part of the vector store -
'what documents have I uploaded' is an application-metadata question, not a content
question, and no amount of retrieval tuning can make chunk-similarity search answer
it. This gives a direct, always-correct answer instead."""
from datetime import datetime, timezone

import psycopg

from agentic_rag.config import settings

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS ingested_documents (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    chunk_count INTEGER NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL
);
"""


def _connect():
    return psycopg.connect(settings.postgres_url, autocommit=True)


def record_ingestion(filename: str, chunk_count: int) -> None:
    with _connect() as conn:
        conn.execute(_CREATE_TABLE)
        conn.execute(
            "INSERT INTO ingested_documents (filename, chunk_count, ingested_at) VALUES (%s, %s, %s)",
            (filename, chunk_count, datetime.now(timezone.utc)),
        )


def list_documents() -> list[dict]:
    with _connect() as conn:
        conn.execute(_CREATE_TABLE)
        rows = conn.execute(
            "SELECT filename, chunk_count, ingested_at FROM ingested_documents ORDER BY ingested_at DESC"
        ).fetchall()
    return [{"filename": r[0], "chunk_count": r[1], "ingested_at": r[2].isoformat()} for r in rows]