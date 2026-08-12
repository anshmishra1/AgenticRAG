"""End-to-end ingestion: load a file by extension, chunk it, and upsert into Pinecone."""
from pathlib import Path

from langchain_core.documents import Document

from agentic_rag.core.timing import PerformanceTracker
from agentic_rag.ingestion.chunking import chunk_documents
from agentic_rag.ingestion.loaders import load_audio, load_image, load_pdf
from agentic_rag.llm.provider import provider_chain
from agentic_rag.retrieval.vectorstore import get_vectorstore


_LOADERS = {
    ".pdf": load_pdf,
    ".png": load_image,
    ".jpg": load_image,
    ".jpeg": load_image,
    ".mp3": load_audio,
    ".wav": load_audio,
    ".m4a": load_audio,
}


def _build_overview(docs: list[Document], filename: str) -> Document:
    tracker = PerformanceTracker()

    with tracker.measure("overview generation"):
        """Generates a short summary of the whole document, stored as its own
        dedicated chunk (metadata type='overview'). No single content chunk can
        answer 'what does this document cover' - that's a whole-document question,
        so it needs a whole-document answer generated once, not assembled from
        fragments at query time."""
        sample = "\n\n".join(d.page_content for d in docs[:15])[:12000]
        prompt = (
            "Summarize what this document covers: its main subject, structure, and "
            "scope. Be specific about named topics, chapters, or "
            "sections if visible in the excerpt.\n\n"
            f"Document excerpt:\n{sample}"
        )
        summary = provider_chain.invoke(prompt).content
        return Document(page_content=summary, metadata={"source": filename, "type": "overview"})


def ingest_file(path: str | Path, display_name: str | None = None) -> int:
    tracker = PerformanceTracker()

    with tracker.measure("file ingesion"):
        """Loads, chunks, and indexes a single file, plus a generated whole-document
        overview. Returns the number of content chunks written (overview not counted)."""
        path = Path(path)
        loader = _LOADERS.get(path.suffix.lower())
        if loader is None:
            raise ValueError(f"Unsupported file type: {path.suffix}")

        docs = loader(path)
        chunks = chunk_documents(docs)
        overview = _build_overview(docs, display_name or path.name)

        get_vectorstore().add_documents(chunks + [overview])

        from agentic_rag.ingestion.registry import record_ingestion
        record_ingestion(display_name or path.name, len(chunks))

        # Print the full timing summary across measured pipeline nodes
        tracker.summary()

        return len(chunks)