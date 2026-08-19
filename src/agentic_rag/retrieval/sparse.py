"""Sparse (BM25) encoding for Pinecone hybrid search.

BM25 is fit PER DOCUMENT rather than globally across the whole corpus. This
matches the existing document_id-scoped retrieval design - queries are always
scoped to one document, so a document-local IDF distribution is actually more
relevant than a global one, and it sidesteps the bootstrapping problem of
needing a representative corpus before the first document is ever ingested.
pinecone-text's BM25Encoder is documented as "single fit to a corpus, no
continuous updates" - a per-document fit is exactly the intended usage, not
a workaround.

The fitted encoder's parameters are persisted in the document registry
(Postgres), keyed by document_id, so the exact same IDF statistics used at
ingestion time are reused at query time - a BM25 sparse vector is only
meaningful when the query is encoded with the same fitted state as the
documents were.

BM25Encoder.dump()/.load() are file-path based (not dict in/out), so this
module round-trips through a temp file rather than a native serialization -
that's a property of the pinecone-text library, not a design choice here.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from pinecone_text.sparse import BM25Encoder


def fit_bm25(texts: list[str]) -> BM25Encoder:
    encoder = BM25Encoder()
    encoder.fit(texts)
    return encoder


def dump_bm25_json(encoder: BM25Encoder) -> str:
    """Serializes the fitted encoder to a JSON string for storage in Postgres."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        encoder.dump(tmp_path)
        return Path(tmp_path).read_text()
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def load_bm25_json(params_json: str) -> BM25Encoder:
    """Reconstructs a fitted encoder from a JSON string previously produced
    by dump_bm25_json()."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp.write(params_json)
        tmp_path = tmp.name
    try:
        return BM25Encoder().load(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)