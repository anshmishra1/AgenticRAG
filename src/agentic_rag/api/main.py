"""FastAPI entrypoint. Keeps graph logic behind a stable REST interface so the
Streamlit UI (or anything else) never touches LangGraph internals directly.

The Postgres checkpointer connection opens once at app startup and closes once
at shutdown, via FastAPI's lifespan - same context-manager pattern as
PostgresSaver.from_conn_string(...), just held open for the app's lifetime
instead of a single script block."""

import logging
import shutil
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from langgraph.checkpoint.postgres import PostgresSaver
from pydantic import BaseModel

from agentic_rag.config import settings
from agentic_rag.graph.builder import build_graph
from agentic_rag.ingestion.pipeline import _document_id, ingest_file
from agentic_rag.ingestion.registry import list_documents
from agentic_rag.observability.trace import configure_logging
from agentic_rag.retrieval.reranker import warmup_cross_encoder

configure_logging(settings.debug)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("huggingface_hub").setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with PostgresSaver.from_conn_string(settings.postgres_url) as checkpointer:
        checkpointer.setup()  # Creates checkpoint tables if they don't exist yet; idempotent
        warmup_cross_encoder()
        app.state.rag_graph = build_graph(checkpointer)
        yield
    # Connection closes automatically here on shutdown


app = FastAPI(title="Agentic RAG API", lifespan=lifespan)


class QueryRequest(BaseModel):
    question: str
    session_id: str = "default"
    document_id: str | None = None


class QueryResponse(BaseModel):
    answer: str
    grounded: bool


class IngestResult(BaseModel):
    filename: str
    document_id: str
    chunks_indexed: int


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest, http_request: Request) -> QueryResponse:
    config = {"configurable": {"thread_id": request.session_id}}

    result = http_request.app.state.rag_graph.invoke(
        {
            "question": request.question,
            "document_id": request.document_id,
            "retry_count": 0,
            "hallucination_retry_count": 0,
        },
        config=config,
    )

    return QueryResponse(
        answer=result["generation"],
        grounded=result.get("hallucination_grade") == "grounded",
    )


@app.post("/ingest", response_model=list[IngestResult])
async def ingest(files: list[UploadFile] = File(...)) -> list[IngestResult]:
    """Accepts one or more files, writes each to a temp path, and runs it through
    the ingestion pipeline (load -> chunk -> upsert into Pinecone)."""
    results = []
    for upload in files:
        suffix = Path(upload.filename or "").suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload.file, tmp)
            tmp_path = tmp.name

        try:
            # NOTE: document_id is still computed here AND again inside
            # ingest_file() - flagged, not yet fixed pending pipeline.py.
            document_id = _document_id(Path(tmp_path))
            chunk_count = ingest_file(
                tmp_path,
                display_name=upload.filename,
            )

            results.append(
                IngestResult(
                    filename=upload.filename or "unknown",
                    document_id=document_id,
                    chunks_indexed=chunk_count,
                )
            )
        except (ValueError, NotImplementedError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    return results


@app.get("/documents")
def documents() -> list[dict]:
    """Returns what's actually been ingested - a direct metadata answer, not a
    question routed through the RAG graph."""
    return list_documents()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}