"""Structured request tracing for the RAG pipeline. Lets a single bad answer be
diagnosed as a retrieval failure, a grading failure, a generation failure, or a
hallucination-grader failure - instead of debugging the graph as a black box.

Every stage logs one readable line: [stage] key=value | key=value ...
Long values (document content, generated answers) are truncated so the log
stays scannable rather than flooded with full chunk text.
"""
import logging

logger = logging.getLogger("agentic_rag.trace")


def log_stage(stage: str, **fields) -> None:
    parts = []
    for key, value in fields.items():
        text = str(value)
        if len(text) > 200:
            text = text[:200] + "...[truncated]"
        parts.append(f"{key}={text!r}")
    logger.info("[%s] %s", stage, " | ".join(parts))


def configure_logging(debug: bool) -> None:
    """Called once at app startup. The trace logger is always visible at INFO -
    it's the whole point of this module. debug=True additionally turns up
    everything else (library internals); debug=False keeps noisy third-party
    libraries quiet so the trace isn't buried."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(name)s: %(message)s")
    logging.getLogger("agentic_rag.trace").setLevel(logging.INFO)
    if not debug:
        for noisy in ("httpx", "httpcore", "urllib3", "pinecone", "langchain", "langchain_core"):
            logging.getLogger(noisy).setLevel(logging.WARNING)