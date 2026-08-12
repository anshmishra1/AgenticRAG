# Agentic RAG — Project Reference

Living reference for the project's current state. Upload this file at the start
of a new session instead of re-explaining the project verbally — it has enough
context for a resumed conversation, and doubles as raw material for the
interview Q&A doc later.

## Architecture (request flow)

```Shell
User question
  -> contextualize_question   (rewrites follow-ups into standalone queries,
                                using chat history; leaves raw question untouched)
  -> retrieve                 (fetches overview chunk(s) + top-k content chunks)
  -> grade_documents           (LLM judges relevance: relevant | irrelevant)
       -> if irrelevant & retries left: rewrite_query -> back to retrieve
  -> generate                  (answers using context + chat history)
  -> check_hallucination        (LLM judges: grounded | hallucinated)
       -> if hallucinated & retries left: back to generate
  -> record_turn                (appends turn to persisted chat history)
  -> end
```

Ingestion is a separate path, not part of the query graph:

```
Upload -> load (pdf/image/audio) -> chunk -> generate whole-doc overview
       -> upsert chunks + overview into Pinecone -> record in document registry
```

## File structure and purpose

```
src/agentic_rag/
  config.py                Typed settings from .env (all provider keys, Pinecone,
                            Postgres URL, chunk size, retry limit)
  llm/
    provider.py             ProviderChain: Groq -> Cerebras -> Bedrock fallback.
                             Same open-weight model family across providers, so
                             a fallback doesn't change answer quality.
    vision.py                Image captioning via llama-4-maverick (Groq).
                             llama-4-scout was deprecated by Groq June 2026.
  ingestion/
    loaders.py                load_pdf / load_image / load_audio.
    chunking.py               RecursiveCharacterTextSplitter, 1500/300.
    whisper_transcribe.py     Audio -> text via Groq's hosted Whisper.
    pipeline.py                ingest_file(): orchestrates load -> chunk ->
                                overview generation -> vector store upsert ->
                                registry record.
    registry.py                Postgres table tracking what's been ingested
                                (filename, chunk count, timestamp). Answers
                                "what did I upload" directly - NOT via the
                                RAG graph, since that's a metadata question,
                                not a content question.
  retrieval/
    vectorstore.py             get_retriever() - MMR search, k=8, excludes
                                overview chunks (metadata filter).
                                get_overview_retriever() - fetches only
                                overview chunks, by metadata filter not
                                similarity, so they're always available.
  graph/
    state.py                   RAGState: question (raw, untouched) vs
                                retrieval_query (rewritten for search) vs
                                documents/generation/grades/retry_count vs
                                messages (persisted via checkpointer).
    nodes.py                    All seven node functions (see flow above).
    edges.py                    route_after_grading, route_after_hallucination_check
                                - the two feedback loops, capped by
                                settings.max_retries.
    builder.py                  Assembles the StateGraph. Takes a checkpointer
                                as a parameter (doesn't own the connection).
  api/
    main.py                    FastAPI app. Lifespan opens PostgresSaver via
                                from_conn_string, builds the graph once, stores
                                it on app.state, closes cleanly on shutdown.
                                Endpoints: /query, /ingest, /documents, /health.
  evaluation/
    ragas_eval.py               Offline eval harness (faithfulness, relevancy,
                                context precision/recall). NOT wired into the
                                live query path on purpose.
app/streamlit_app.py            Thin client: upload UI, document list, chat.
                                No pipeline logic - only HTTP calls to the API.
                                Caches requests.Session via st.cache_resource.
tests/                          Unit tests for chunking + graph routing logic.
                                No real API keys needed (conftest.py stubs one).
```

## Key design decisions and rationale

| Decision                                                  | Why                                                                                                                                                                                              |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| LangChain/FAISS -> LangGraph state machine                | Enables the corrective-retrieval and hallucination-check loops; a linear chain can't branch/retry                                                                                                |
| Chroma -> Pinecone (single vector store, no dual-backend) | Cloud deploy target has no persistent local disk; one backend, less surface area                                                                                                                 |
| Provider fallback chain (Groq -> Cerebras -> Bedrock)     | Groq free tier RPD limits get hit during active dev; same model family across providers keeps output consistent; genuine "why 3 providers" story for interviews                                  |
| MemorySaver -> Postgres checkpointer (Neon)               | MemorySaver is in-process, lost on restart; SQLite writes to ephemeral disk on Streamlit Cloud/Render, also lost on redeploy; Postgres survives both                                             |
| Checkpointer opened via FastAPI lifespan, not a bare pool | Matches proper context-manager resource lifecycle: open once at startup, close once at shutdown                                                                                                  |
| `retrieval_query` separate from `question`            | Follow-ups like "answer in bullet points" need query rewriting for retrieval, but the LLM still needs to see the literal formatting instruction to obey it                                       |
| MMR retrieval instead of plain top-k                      | Plain top-k tends to return near-duplicate chunks from one section; MMR spreads across the document - matters for broad questions                                                                |
| Document overview chunk, generated at ingestion           | No single 1500-char chunk can answer "what does this document cover" - that's a whole-document question needing a whole-document answer, generated once and always retrieved via metadata filter |
| Document registry (Postgres table)                        | "What did I upload" is metadata, not content - no amount of retrieval tuning can make vector search answer it                                                                                    |

## Known gaps / honest TODOs

- **True hybrid search (dense + sparse/BM25) not implemented.** Current retrieval is dense-only via MMR. The "Pinecone hybrid search" line predates this and hasn't been reconciled yet.
- **Image ingestion** uses vision-model captioning (llama-4-maverick), not EasyOCR — a deliberate substitution, not the original plan.
- **RAGAS eval** exists but isn't run automatically anywhere yet — no CI step or scheduled job calls it.
- **Web search fallback tool** (for questions outside the uploaded docs) was discussed, not built.
- **No re-ranking step** after retrieval — MMR is the only diversity mechanism.
- Postgres now backs both the checkpointer (conversation memory) and the document registry — same DB, different tables, not yet consolidated into one connection/pool.

## Deployment target

Backend (FastAPI) + frontend (Streamlit) as separate services, both containerized
via the provided Dockerfile / docker-compose.yml, deployed to Streamlit Cloud
and/or Render. External dependencies: Groq, Cerebras (optional), AWS Bedrock
(optional), Pinecone, Neon Postgres.
