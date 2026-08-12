# Agentic RAG application

LangGraph-orchestrated corrective RAG pipeline with relevance grading, query
rewriting, hallucination checking, and a RAGAS evaluation harness.

## Architecture

```
Ingest & parse (docs, images, audio)
        v
Chunk, embed, index (Pinecone hybrid search)
        v
Corrective retrieval (grade -> rewrite -> re-retrieve loop)
        v
Generate & verify (LLM answer -> hallucination check -> regenerate loop)
        v
Output & evaluate (answer + RAGAS metrics)
```

LLM calls go through a provider chain: **Groq -> Cerebras -> AWS Bedrock**,
falling back automatically on rate limits or errors. All three serve the same
open-weight model family, so a fallback doesn't change answer quality.

## Project layout

```
src/agentic_rag/
  config.py          settings (env vars / .env)
  llm/provider.py     provider fallback chain
  ingestion/          PDF, image, audio loaders + chunking
  retrieval/          Pinecone vector store
  graph/              LangGraph state, nodes, edges, builder
  api/main.py         FastAPI backend
  evaluation/         RAGAS harness
app/streamlit_app.py  thin UI, calls the FastAPI backend
tests/                pytest unit tests
```

## Setup

```bash
cp .env.example .env   # fill in your keys
pip install -r requirements.txt
pip install -e .
```

## Run locally

```bash
uvicorn agentic_rag.api.main:app --reload          # backend on :8000
streamlit run app/streamlit_app.py                  # frontend on :8501
```

Or with Docker:

```bash
docker compose up --build
```

## Test

```bash
pytest tests/ -v
```

## Notes

- Image ingestion (`ingestion/loaders.py::load_image`) is stubbed — wire up
  EasyOCR or a vision-capable model.
- `evaluation/ragas_eval.py::run_eval` expects question/answer/context triples
  collected from real graph runs; not wired into the API yet by design (eval
  runs offline, not per-request).
