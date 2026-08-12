from langchain_core.documents import Document

from agentic_rag.ingestion.chunking import chunk_documents


def test_chunk_documents_splits_long_text():
    long_text = "word " * 2000
    docs = [Document(page_content=long_text)]
    chunks = chunk_documents(docs)
    assert len(chunks) > 1
    assert all(len(c.page_content) <= 1500 + 300 for c in chunks)
