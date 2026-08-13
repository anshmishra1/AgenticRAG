"""Document chunking with document-level metadata propagation.

The splitter configuration remains unchanged. Every produced chunk can now
carry a stable document_id and user-facing filename so retrieval can later
be scoped to the active document.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agentic_rag.config import settings


def chunk_documents(
    docs: list[Document],
    *,
    document_id: str | None = None,
    filename: str | None = None,
) -> list[Document]:
    """Split documents while preserving and enriching chunk metadata.

    Existing loader metadata such as page numbers is preserved.
    document_id and filename are added to every resulting chunk when supplied.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    chunks = splitter.split_documents(docs)

    for chunk in chunks:
        if document_id is not None:
            chunk.metadata["document_id"] = document_id

        if filename is not None:
            chunk.metadata["filename"] = filename
            chunk.metadata["source"] = filename

        chunk.metadata.setdefault("type", "content")

    return chunks
