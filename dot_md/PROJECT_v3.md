# Agentic RAG — Project Reference & Handoff

## Purpose

This file is the **single-source project handoff document** for the Agentic RAG project.

It is written so that a new chatbot/LLM — including a local Ollama model — can understand the project's history, current architecture, important design decisions, known issues, completed work, and next steps **without requiring the user to re-explain the project**.

### How to use this file

At the beginning of a new development session:

1. Load this file first.
2. Treat the **Current State** section as authoritative for the latest project direction.
3. Treat **Completed Changes** as historical context; do not repeat those investigations unless a regression occurs.
4. Treat **Known Gaps / TODOs** as work that has not yet been completed.
5. Before changing architecture, inspect the relevant current source files because this document is a handoff summary, not a replacement for source code.

---

# 1. Project Goal

Build a production-oriented **Agentic RAG application** that can:

- ingest PDFs, images, and audio;
- transform them into searchable knowledge;
- retrieve relevant document context;
- answer questions grounded in the ingested knowledge;
- maintain conversational state;
- correct poor retrieval through query rewriting;
- verify generated answers for hallucination;
- expose the RAG pipeline through a FastAPI backend;
- provide a conversational Streamlit frontend;
- persist graph/checkpoint state through PostgreSQL;
- eventually evolve into a true **Agentic RAG system with tool access, tool selection, multi-step reasoning, and external capabilities**.

The project is deliberately being developed in stages:

```text
Basic RAG
    ↓
Production-style RAG
    ↓
Corrective / Advanced RAG       ← current RAG capability
    ↓
Agentic RAG                     ← next major phase
    ↓
Advanced Agentic System
```

---

# 2. Current Maturity

## RAG maturity

**Current assessment: ~7/10 — Intermediate/Advanced, corrective RAG.**

The system is no longer a basic:

```text
Query → Embed → Vector DB → Context → LLM
```

pipeline.

It currently contains:

- document ingestion;
- chunking;
- embeddings;
- Pinecone vector retrieval;
- conversational state;
- query contextualization;
- relevance grading;
- corrective query rewriting;
- re-retrieval;
- grounded generation;
- hallucination checking;
- regeneration;
- LangGraph orchestration;
- FastAPI backend;
- Streamlit UI;
- PostgreSQL checkpointing.

## Agentic maturity

**Current assessment: foundation only; true tool-using agency has not yet been implemented.**

The next major milestone is to make the existing RAG capability itself a tool and then add additional tools such as:

- web search;
- calculator;
- potentially SQL/database access;
- document metadata access;
- later MCP-based tools.

The goal is not to add tools for the sake of complexity. The agent must be able to decide **when a tool is necessary, which tool to use, execute it, inspect the result, and continue or answer**.

---

# 3. Architecture — Current Query Flow

The intended current corrective-RAG request flow is:

```text
User question
    ↓
contextualize_question
    ↓
retrieve
    ↓
grade_documents
    │
    ├── relevant
    │      ↓
    │   generate
    │      ↓
    │   check_hallucination
    │      │
    │      ├── grounded → record_turn → END
    │      │
    │      └── hallucinated → generate
    │
    └── irrelevant
           ↓
       rewrite_query
           ↓
        retrieve
```

### Important state separation

The graph intentionally distinguishes:

```text
question
```

from:

```text
retrieval_query
```

`question` is the user's original wording and must remain untouched so that formatting/style instructions survive.

`retrieval_query` is the standalone/search-optimized version used by retrieval.

Example:

```text
User:
"Explain this in detail and use bullet points."

question:
"Explain this in detail and use bullet points."

retrieval_query:
"topic being discussed"
```

This prevents retrieval-oriented rewriting from destroying the user's answer-formatting instructions.

---

# 4. Ingestion Flow

Ingestion is separate from the query graph.

```text
Upload
  ↓
load
  ├── PDF
  ├── image
  └── audio
  ↓
chunk
  ↓
generate whole-document overview
  ↓
upsert chunks + overview into Pinecone
  ↓
record ingestion metadata in PostgreSQL
```

The whole-document overview exists because a single chunk cannot reliably answer questions such as:

> "What does this document cover?"

The overview is generated once during ingestion rather than reconstructed from arbitrary fragments during every query.

---

# 5. Current Project Structure

Expected high-level structure:

```text
agentic-rag/
│
├── src/
│   └── agentic_rag/
│       ├── config.py
│       │
│       ├── llm/
│       │   ├── provider.py
│       │   └── vision.py
│       │
│       ├── ingestion/
│       │   ├── loaders.py
│       │   ├── chunking.py
│       │   ├── whisper_transcribe.py
│       │   ├── pipeline.py
│       │   └── registry.py
│       │
│       ├── retrieval/
│       │   └── vectorstore.py
│       │
│       ├── graph/
│       │   ├── state.py
│       │   ├── nodes.py
│       │   ├── edges.py
│       │   └── builder.py
│       │
│       └── api/
│           └── main.py
│
├── app/
│   └── streamlit_app.py
│
├── evaluation/
│   └── ragas_eval.py
│
└── tests/
```

---

# 6. File Responsibilities

## `src/agentic_rag/config.py`

Central settings loaded through Pydantic Settings and `.env`.

Current settings include:

- Groq API key;
- Cerebras API key;
- AWS Bedrock region;
- Pinecone API key;
- Pinecone index name;
- HuggingFace token;
- PostgreSQL URL;
- embedding model;
- chunk size;
- chunk overlap;
- maximum retries.

Current local PostgreSQL configuration discovered during development:

```text
PostgreSQL: localhost:5432
```

The previous configuration used port `5442`, but local PostgreSQL was found listening on `5432`. Docker was not running.

---

## `src/agentic_rag/llm/provider.py`

Provider abstraction / fallback chain.

The intended provider strategy is:

```text
Groq
  ↓ fallback
Cerebras
  ↓ fallback
AWS Bedrock
```

The goal is to maintain a stable model family/behavior while avoiding dependence on a single provider.

### Important generation behavior

The generation prompt previously contained:

```text
Keep the answer concise.
```

This caused answers to remain around 2–4 sentences even when the user explicitly requested elaboration.

This instruction should be removed/replaced with:

```text
Follow the user's requested level of detail, structure, and style.
If the user asks for a detailed explanation, provide a detailed explanation.
If the user asks for a concise answer, keep it concise.
Do not omit important details needed to properly answer the question.
```

This is a known generation-quality modification.

---

## `src/agentic_rag/llm/vision.py`

Image understanding/captioning component.

The project notes indicate image ingestion uses a vision model rather than the originally considered OCR path.

---

## `src/agentic_rag/ingestion/loaders.py`

Loads supported input types:

```text
.pdf
.png
.jpg
.jpeg
.mp3
.wav
.m4a
```

---

## `src/agentic_rag/ingestion/chunking.py`

Uses recursive text splitting.

Target configuration:

```text
chunk_size = 1500
chunk_overlap = 300
```

---

## `src/agentic_rag/ingestion/whisper_transcribe.py`

Audio → text transcription.

Uses hosted Whisper functionality.

---

## `src/agentic_rag/ingestion/pipeline.py`

Orchestrates:

```text
load → chunk → overview → Pinecone upsert → registry record
```

The function is:

```python
ingest_file(path, display_name=None)
```

Important API-side improvement:

```python
ingest_file(
    tmp_path,
    display_name=upload.filename,
)
```

should be used so the original uploaded filename is retained as metadata rather than the temporary Windows filename.

---

## `src/agentic_rag/ingestion/registry.py`

Tracks ingested documents in PostgreSQL.

Purpose:

```text
"What did I upload?"
```

is a metadata question, not a semantic document-content question.

Therefore it should not be forced through the normal RAG retrieval graph.

---

# 7. Retrieval

## `src/agentic_rag/retrieval/vectorstore.py`

Uses:

```text
HuggingFaceEmbeddings
        ↓
PineconeVectorStore
        ↓
retriever
```

Current embedding model configured through:

```text
settings.embedding_model
```

Default:

```text
all-MiniLM-L6-v2
```

The uploaded source notes describe an MMR-based retriever with k=8 and an overview-specific retriever. The current source code should be treated as authoritative if these values differ.

### Important historical discrepancy

An earlier version of the project used plain:

```text
k = 5
```

retrieval.

Later project notes describe:

```text
MMR
k = 8
overview filtering
```

Do not assume both are simultaneously true. Check the current `vectorstore.py` before modifying retrieval.

---

# 8. Graph State

## `src/agentic_rag/graph/state.py`

The shared `RAGState` contains:

```text
question
retrieval_query
documents
generation
relevance_grade
hallucination_grade
retry_count
messages
```

### Meaning

```text
question
    = raw user input

retrieval_query
    = rewritten/contextualized search query

documents
    = retrieved LangChain Documents

generation
    = final LLM answer

relevance_grade
    = relevant | irrelevant

hallucination_grade
    = grounded | hallucinated

retry_count
    = corrective loop counter

messages
    = persisted conversation history
```

---

# 9. Graph Nodes

## `src/agentic_rag/graph/nodes.py`

The important nodes are:

### `contextualize_question`

Uses conversation history to turn follow-up questions into standalone retrieval queries.

Example:

```text
Previous:
"What is Linux?"

Follow-up:
"Explain its architecture."

Retrieval query:
"Explain the architecture of Linux."
```

For a first question with no history, the original question is used directly.

---

### `retrieve`

Calls the vector retriever using:

```text
retrieval_query
```

or falls back to:

```text
question
```

if no retrieval query exists.

---

### `grade_documents`

Uses the LLM to classify retrieved context:

```text
relevant
```

or:

```text
irrelevant
```

This is a batch-level relevance grade, not an individual per-document relevance score.

---

### `rewrite_query`

Runs when retrieval is considered irrelevant and retry budget remains.

It rewrites the search query for better semantic retrieval.

---

### `generate`

Generates an answer using:

- retrieved context;
- prior conversation;
- original user question.

It must respect the user's requested answer length and style.

It should **not** globally force concise answers.

If the answer cannot be supported by context, the intended behavior is:

```text
I don't know.
```

---

### `check_hallucination`

Checks whether the generated answer is supported by retrieved context:

```text
grounded
```

or:

```text
hallucinated
```

Important interpretation:

```text
"I don't know" + grounded
```

does NOT mean the question was successfully answered.

It only means the answer itself did not introduce unsupported factual claims.

---

### `record_turn`

Adds the user's question and assistant answer to persisted conversation history.

---

# 10. Graph Routing

## `src/agentic_rag/graph/edges.py`

### After relevance grading

```text
relevant
    → generate

irrelevant + retries available
    → rewrite_query

irrelevant + retry limit reached
    → generate best-effort answer
```

### After hallucination check

```text
grounded
    → record_turn

hallucinated + retries available
    → generate again

hallucinated + retry limit reached
    → record_turn / END
```

### Known architectural limitation

The hallucination loop currently regenerates against essentially the same context.

A stronger future design should change something after a hallucination, for example:

```text
hallucinated
    ↓
retrieve additional evidence
or
answer correction / critique
    ↓
generate
```

Simply asking the same generation step to try again is not a strong corrective mechanism.

---

# 11. Graph Builder

## `src/agentic_rag/graph/builder.py`

Builds the LangGraph `StateGraph`.

It receives the checkpointer from the API layer rather than owning the PostgreSQL connection.

The intended query graph is:

```text
contextualize_question
    ↓
retrieve
    ↓
grade_documents
    ├── generate
    └── rewrite_query → retrieve
    ↓
check_hallucination
    ├── record_turn
    └── generate
    ↓
END
```

### Important historical issue

`contextualize_question()` existed in `nodes.py` before it was actually connected to the graph.

This was identified and corrected conceptually by adding:

```text
contextualize_question
```

as the graph entry node.

This is important for follow-up questions.

---

# 12. FastAPI Backend

## `src/agentic_rag/api/main.py`

FastAPI is the stable REST boundary between the UI and LangGraph.

The UI does not directly manipulate LangGraph internals.

### Endpoints

```text
POST /query
POST /ingest
GET  /health
```

Some project notes also mention:

```text
GET /documents
```

If that endpoint is not present in the current source, do not assume it exists.

### `/query`

Receives:

```json
{
  "question": "...",
  "session_id": "..."
}
```

and invokes LangGraph using:

```text
thread_id = session_id
```

This connects the conversation to PostgreSQL checkpoint state.

### `/ingest`

Accepts multiple files, writes temporary files, runs `ingest_file()`, and deletes temporary files afterwards.

Important current improvement:

```python
ingest_file(tmp_path, display_name=upload.filename)
```

to preserve the original document name.

### `/health`

Returns:

```json
{
  "status": "ok"
}
```

---

# 13. PostgreSQL / LangGraph Checkpointing

PostgreSQL is used for persistent graph/checkpoint state.

The FastAPI lifespan owns the checkpointer lifecycle:

```text
Application startup
    ↓
PostgresSaver.from_conn_string(...)
    ↓
checkpointer.setup()
    ↓
build graph
    ↓
serve requests
    ↓
Application shutdown
    ↓
connection closes
```

This is preferred over creating/closing a database connection for every request.

### Local development finding

Local PostgreSQL was confirmed to be listening on:

```text
localhost:5432
```

not:

```text
localhost:5442
```

Docker was not running during diagnosis.

---

# 14. Streamlit Frontend

## `app/streamlit_app.py`

The Streamlit application is intentionally thin.

It should contain UI and HTTP logic only.

### Current UI behavior

The UI now supports:

- document upload;
- ingestion;
- persistent visible chat history;
- multiple questions in the same session;
- follow-up questions;
- entirely new questions;
- assistant responses;
- grounding status;
- reusable HTTP session.

The chat UI uses Streamlit's conversational primitives rather than a single ephemeral text input.

Conceptually:

```text
User message
    ↓
display in chat
    ↓
POST /query
    ↓
FastAPI
    ↓
LangGraph
    ↓
response
    ↓
display assistant message
    ↓
store in Streamlit chat history
```

The same `session_id` is sent for each query, so the backend can maintain the conversation state.

### Important follow-up behavior

The UI supports both:

```text
follow-up:
"Explain that in more detail."
```

and:

```text
new question:
"What is Docker?"
```

However, the graph's contextualization logic must distinguish between genuine follow-ups and independent new questions. This is an area for future improvement.

---

# 15. Debugging / Observability

A major development decision was made to stop debugging the RAG pipeline as a black box.

The desired debug trace is:

```text
QUESTION
    ↓
RETRIEVAL QUERY
    ↓
RETRIEVED DOCUMENTS
    ↓
RELEVANCE GRADE
    ↓
QUERY REWRITE (if needed)
    ↓
GENERATION
    ↓
HALLUCINATION GRADE
    ↓
FINAL ROUTE
```

For each request, development-mode logging should expose:

- original question;
- contextualized retrieval query;
- number of retrieved documents;
- document metadata;
- document previews;
- relevance grader raw output;
- normalized relevance grade;
- retry count;
- rewritten query;
- generation context preview;
- generated answer;
- hallucination grader raw output;
- final route.

### Purpose

This allows us to distinguish:

```text
Retrieval failure
vs
Relevance grader failure
vs
Generation failure
vs
Hallucination grader failure
```

Do not randomly modify multiple layers before inspecting this trace.

---

# 16. Important Debugging Lesson: "I Don't Know"

A test such as:

```text
What is Linux?
```

may correctly produce:

```text
I don't know.
```

if Linux is not present in the uploaded documents.

This is expected behavior for a document-grounded RAG system.

Also:

```text
I don't know.
Grounded in context
```

is not contradictory.

It means:

```text
The answer did not hallucinate.
```

It does NOT mean:

```text
The question was successfully answered.
```

A better UI should eventually distinguish:

```text
Answer supported by context
```

from:

```text
No answer found in context
```

---

# 17. Generation Length Problem

A specific generation-quality issue was identified.

The generation prompt contained:

```text
Keep the answer concise.
```

This was causing answers to remain short even when the user explicitly asked for detail.

### Desired behavior

```text
User asks for definition
    → concise

User asks for detailed explanation
    → detailed

User asks for examples
    → include examples

User asks for advantages + limitations
    → structured detailed answer

User asks for one line
    → one line
```

The user's instruction should determine answer length rather than a hard-coded global brevity rule.

---

# 18. Why This Is Already More Than Basic RAG

Current capabilities include:

```text
Document ingestion
        ↓
Chunking
        ↓
Embeddings
        ↓
Pinecone
        ↓
Contextual retrieval
        ↓
Relevance grading
        ↓
Corrective query rewriting
        ↓
Re-retrieval
        ↓
Grounded generation
        ↓
Hallucination verification
        ↓
Regeneration
        ↓
Persistent conversation state
```

This is best described as:

> **Corrective / Advanced RAG**

It is not yet a full tool-using agent.

---

# 19. Agentic Phase — NEXT MAJOR DEVELOPMENT

The next phase is to transform the current RAG subsystem into a tool available to an agent.

The target architecture is:

```text
                         ┌── RAG / Document Search
                         │
User → Agent/Router ─────┼── Web Search
                         │
                         ├── Calculator
                         │
                         ├── Document Metadata
                         │
                         └── Future Tools
```

The agent should be able to:

1. understand the user request;
2. decide whether a tool is required;
3. select the appropriate tool;
4. execute it;
5. inspect the result;
6. decide whether another tool call is required;
7. produce the final answer.

---

# 20. Agentic RAG Roadmap

## Agentic RAG v1

Implement:

1. Existing RAG as `search_documents` tool.
2. Calculator tool.
3. Web search tool.
4. LLM tool selection.
5. Tool execution loop.
6. Conditional routing.
7. Persistent conversation state.

Target flow:

```text
User
 ↓
Agent
 ↓
Decide tool
 ├── RAG
 ├── Web
 └── Calculator
 ↓
Tool result
 ↓
Observe
 ↓
Need another tool?
 ├── YES → tool
 └── NO → answer
```

---

## Agentic RAG v2

Then add:

- multi-step tool use;
- tool-result evaluation;
- planning;
- better failure handling;
- source-aware answers;
- agent tracing;
- tool-call success/failure metrics;
- stronger memory separation;
- RAG + agent evaluation.

---

## MCP phase

MCP should be introduced **after basic tool calling is understood and working**.

Desired progression:

```text
LLM
 ↓
Native application tool
 ↓
Tool result
 ↓
LLM
```

then:

```text
LLM / Agent
 ↓
MCP client
 ↓
MCP server
 ├── Search
 ├── SQL
 ├── Files
 └── Other external capabilities
```

Do not introduce MCP merely for complexity. First establish the underlying tool-calling loop.

---

# 21. Evaluation

## `evaluation/ragas_eval.py`

An offline RAGAS evaluation harness exists / is planned for:

- faithfulness;
- relevancy;
- context precision;
- context recall.

It should remain separate from the live query path.

### Future evaluation expansion

Agentic evaluation should include:

- retrieval relevance;
- answer faithfulness;
- context utilization;
- tool selection accuracy;
- tool-call success rate;
- number of tool calls;
- number of iterations;
- latency;
- hallucination rate;
- final answer quality.

---

# 22. Important Design Decisions

| Decision | Reason |
|---|---|
| LangGraph instead of a linear chain | Enables conditional routing, corrective retrieval, and verification loops |
| Pinecone instead of local-only vector storage | Supports persistent/deployable retrieval |
| PostgreSQL checkpointer | Conversation state survives process restarts/redeployments |
| FastAPI between UI and graph | Keeps LangGraph internals out of the frontend |
| Streamlit as thin client | Presentation layer remains separate from RAG logic |
| `question` separate from `retrieval_query` | Retrieval rewriting must not destroy user formatting/style instructions |
| Whole-document overview | Broad document-level questions need document-level information |
| Document registry separate from semantic retrieval | Upload metadata is not the same as document content |
| Corrective retrieval | Poor retrieval can trigger query rewriting and another retrieval attempt |
| Hallucination check | Prevents unsupported answers from being accepted silently |
| Tool layer comes after stable RAG | Existing RAG should become a reliable capability rather than being rebuilt unnecessarily |

---

# 23. Known Gaps / Honest TODOs

The following are **not yet complete** unless the current source code explicitly shows otherwise:

- True dense + sparse/BM25 hybrid search.
- Post-retrieval reranking.
- Web search fallback/tool.
- Calculator tool.
- RAG exposed as an agent tool.
- LLM-driven tool selection.
- Multi-step tool execution loop.
- Proper hallucination correction that changes/retrieves better evidence.
- Automatic RAGAS evaluation in development/deployment.
- Agent evaluation.
- Agent tracing/observability dashboard.
- Strong distinction between follow-up questions and unrelated new questions.
- MCP integration.
- SQL/database tool.
- Production deployment validation.
- Consolidation/optimization of PostgreSQL connections across checkpointer and registry.

---

# 24. What NOT to Do

Do not:

- add tools randomly without a routing reason;
- introduce multiple agents before the single-agent tool loop works;
- replace the current RAG architecture without evidence that it is necessary;
- tune retrieval blindly without inspecting retrieved chunks;
- interpret `"I don't know"` as a hallucination;
- interpret `"grounded"` as proof that the question was answered;
- add MCP before understanding ordinary tool calling;
- add hybrid search/reranking merely because they sound advanced;
- change multiple pipeline layers at once during debugging.

The project is being developed deliberately from:

```text
Reliable RAG
    ↓
Observable RAG
    ↓
Tool-enabled agent
    ↓
Advanced agentic system
```

---

# 25. Development Commands

## Start FastAPI

From the project root:

```powershell
uvicorn agentic_rag.api.main:app --reload
```

Expected:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

## Start Streamlit

In another terminal:

```powershell
streamlit run app/streamlit_app.py
```

## Health check

```text
http://127.0.0.1:8000/health
```

Expected:

```json
{"status": "ok"}
```

---

# 26. Current Development Order

The intended development order from this point is:

```text
CURRENT
│
├── Stable conversational UI                         ✅
├── FastAPI backend                                  ✅
├── PostgreSQL checkpointing                        ✅
├── Pinecone retrieval                               ✅
├── Corrective RAG                                   ✅
├── Contextual follow-up support                    ✅/refine
├── Debug/observability                             🔧
│
▼
NEXT
│
├── RAG as a tool
├── Calculator tool
├── Web search tool
├── Agent tool selection
├── Tool execution loop
├── Multi-step tool use
├── Tool-result reasoning
│
▼
LATER
│
├── Better planning
├── Better memory
├── Evaluation
├── Tracing
├── MCP
├── SQL / external tools
└── Production deployment
```

---

# 27. Current Project Position — One-Paragraph Handoff

**This project is a FastAPI + Streamlit + LangGraph Agentic RAG application. It ingests PDFs/images/audio, chunks and embeds the content, stores vectors in Pinecone, generates document overviews, and uses a corrective LangGraph RAG pipeline with contextualized queries, retrieval, relevance grading, query rewriting/re-retrieval, grounded generation, hallucination checking, and PostgreSQL-backed conversation state. The Streamlit UI now behaves as a persistent conversational interface and sends the same session ID for follow-ups and new questions. The RAG layer is considered approximately 7/10 maturity: advanced/corrective RAG, but not yet a true tool-using agent. The next major phase is to expose the existing RAG retrieval capability as a tool, add calculator and web-search tools, implement LLM-driven tool selection and a tool execution loop, and only then progress toward MCP, multi-step planning, evaluation, and advanced agentic behavior.**

---

# 28. Session Startup Instruction for Another Chatbot

When this file is loaded into a new session, the assistant should assume:

> The user is continuing development of the Agentic RAG project described in this document. Do not ask the user to explain the project from scratch. First use this file to understand the architecture, completed work, known issues, and next milestone. If source code is provided, inspect the current source before relying on historical values in this document. Clearly distinguish completed features, current implementation, planned features, and unresolved gaps. Prefer incremental changes over unnecessary rewrites.

---

# 29. Source Reference

This document was based on the project's existing `PROJECT_NOTES.md` reference and the development history established during the current project work.

Where historical notes and current source code disagree, **current source code wins**.

This document should be updated whenever a major architectural decision, implementation milestone, debugging discovery, or roadmap change occurs.

---

# 30. Change Log

## Initial project

- Started as a RAG-focused application.
- Established document ingestion, embeddings, vector storage, and LLM generation.
- Moved toward LangGraph to support corrective workflows.

## Retrieval architecture

- Moved to Pinecone for persistent/deployable vector storage.
- Added document overview generation.
- Added corrective relevance grading and query rewriting.

## Persistence

- Replaced in-process memory with PostgreSQL/LangGraph checkpointing.
- Connected FastAPI lifespan to checkpointer lifecycle.

## Backend

- Added FastAPI REST boundary.
- Added `/query`, `/ingest`, and `/health`.

## Frontend

- Streamlit became a thin API client.
- Added persistent visible chat history.
- Added support for multiple questions in one conversation.
- Preserved the same backend session ID for follow-ups.

## Debugging

- Diagnosed Uvicorn import-path issue.
- Diagnosed PostgreSQL port mismatch:
  - application originally attempted `5442`;
  - local PostgreSQL was actually listening on `5432`;
  - Docker had no running containers.
- Identified misleading interpretation of:
  - `I don't know`
  - `grounded`.
- Identified overly restrictive generation instruction:
  - `Keep the answer concise.`
- Identified that `contextualize_question()` existed but needed to be connected into the graph.

## Current direction

The project is now moving from:

```text
Corrective RAG
```

to:

```text
Agentic RAG
```

by adding tool access and LLM-driven tool selection while keeping the existing RAG subsystem as a reliable capability.

---

# 31. Golden Rule

**Do not rebuild what already works.**

The current RAG should become the foundation of the agentic system.

The next architectural question is not:

> "How do we make the RAG more complicated?"

It is:

> **"How does an agent decide when to use this RAG capability, when to use another tool, and when it has enough information to answer?"**

---

# 32. Recent Development Update — Multi-Provider, Retrieval Scoring, Performance Work

This section records the development work completed after the previous project baseline. It is intentionally written as a compact handoff so another chatbot/LLM can understand **what changed, why it changed, how it was approached, what was verified, and what remains unresolved**.

## 32.1 Multi-provider LLM architecture

### Objective

The project was approaching provider limits during active development, particularly with Groq. Instead of making the RAG graph dependent on one inference provider, the LLM layer was expanded into a configurable provider abstraction with fallback.

### Providers

Current configured provider options:

```text
Groq
Cerebras
NVIDIA NIM
OpenRouter
Bedrock (prepared, currently disabled)
```

Provider order is configured through settings rather than hard-coded into graph nodes.

Current development order has been tested with different sequences. One observed working sequence was:

```text
Groq → Cerebras → OpenRouter → NVIDIA
```

The exact order remains a configuration/latency decision rather than a graph-level dependency.

### Configuration changes

`config.py` was expanded to hold:

- Groq API key/model;
- Cerebras API key/model;
- NVIDIA API key/model/base URL;
- OpenRouter API key/model/base URL;
- Bedrock region/model settings;
- Pinecone settings;
- PostgreSQL URL;
- embedding/chunking settings;
- retry/debug settings.

Secrets remain in `.env`; provider credentials are not hard-coded in application code.

### Provider behavior

The provider chain attempts providers in configured order and falls back when a provider call fails.

Observed validation:

- Groq: working;
- NVIDIA: working;
- OpenRouter: working;
- Cerebras: integration works, but inference returned HTTP `402 payment_required` because of account/quota restrictions;
- fallback behavior was verified by allowing a provider to fail and successfully obtaining a response from another provider.

### Important discovery

Fallback currently depends on the provider call returning/raising an error. A provider that hangs for a long time can prevent the chain from reaching the next provider.

Observed NVIDIA behavior during development:

```text
relevance grading   ≈ 17 sec
query rewriting     ≈ 70 sec
some generation     > 5 min observed
```

This established a production concern: **provider calls must eventually have bounded timeouts so fallback cannot be blocked indefinitely.**

### Design rationale

The provider layer should remain independent of graph logic. Graph nodes should ask for an LLM capability (`fast` / `primary`) rather than directly depending on a specific provider.

Future provider-layer improvements should include:

```text
provider selection
      ↓
timeout
      ↓
retry policy
      ↓
fallback
      ↓
provider latency/failure diagnostics
```

Do not solve provider latency by modifying every graph node individually. The provider abstraction is the correct boundary.

---

## 32.2 Retrieval scoring and overview/content retrieval correction

### Problem discovered

`nodes.py` referenced an overview retrieval helper that no longer existed in the current `vectorstore.py` after retrieval code was updated.

Instead of restoring an obsolete helper, the retrieval path was normalized around the current scored retrieval API.

### Current approach

`retrieve()` now obtains:

```text
overview results
    +
content results
    ↓
combined scored results
    ↓
sorted by similarity score
    ↓
retrieval metrics
    ↓
retrieval confidence
```

Overview retrieval uses a metadata filter for overview chunks, while normal content retrieval uses the normal vector search.

The combined results are sorted by score before being returned.

### Why this was done

The project needs retrieval-quality information before making CRAG more selective. Instead of automatically calling an LLM relevance grader for every query, the system first needs inexpensive retrieval signals such as:

- top similarity score;
- second score;
- score gap;
- mean score;
- retrieval confidence.

These signals are now available for future adaptive routing.

### Validation

A focused retrieval test was added/run successfully. It verified:

- documents are returned;
- scores are returned;
- document/score counts match;
- scores are sorted descending;
- top score is correct;
- confidence is populated;
- retrieval trace is produced.

The retrieval-layer test passed successfully.

---

## 32.3 CRAG cost/latency optimization direction

### Problem

The corrective RAG pipeline can invoke multiple LLM calls for a single user request:

```text
contextualization
      ↓
relevance grading
      ↓
query rewriting (if needed)
      ↓
re-retrieval
      ↓
generation
      ↓
hallucination checking
```

This is useful for quality, but expensive in terms of:

- API requests;
- tokens;
- provider rate limits;
- latency.

Removing CRAG entirely is not acceptable because the corrective behavior is an important quality feature.

### Chosen direction

Move toward **adaptive/selective CRAG**, not removal of CRAG.

Target behavior:

```text
Retrieve
   ↓
retrieval confidence
   │
   ├── HIGH → skip expensive relevance grading → generate
   │
   ├── BORDERLINE → perform LLM relevance grading
   │
   └── LOW → corrective recovery / rewrite / re-retrieve
```

The thresholds must not be guessed. The existing relevance grader should first be used as a calibration oracle against representative questions. Only after validating that inexpensive retrieval signals correlate with relevance should the relevance LLM call become conditional.

### Important UX constraint

Optimization must satisfy all three conditions:

```text
fewer LLM calls
        +
no meaningful latency increase
        +
no degradation in retrieval/answer quality
```

A heuristic that takes almost as long as the LLM call it replaces is not considered an optimization.

---

## 32.4 Performance instrumentation

### Objective

The project was being debugged largely from logs and user-perceived latency. A reusable `PerformanceTracker` was introduced so expensive stages can be measured rather than guessed.

The tracker supports stage timing and bottleneck reporting.

### Instrumented RAG stages

Timing was added around the major graph operations:

```text
contextualize_question
retrieve
grade_documents
rewrite_query
generate
check_hallucination
```

The intent is stage-level instrumentation, not micro-timing every line of Python.

### Tracker improvement

The initial tracker stored one float per stage. This was identified as insufficient for CRAG because a stage can execute more than once:

```text
retrieve #1
      ↓
grade #1
      ↓
rewrite
      ↓
retrieve #2
      ↓
grade #2
```

The tracker was therefore redesigned to preserve repeated stage invocations and report:

- total stage time;
- number of calls;
- individual executions for repeated stages;
- total request time;
- bottleneck stage.

### Standalone timing validation

A timing test was successfully run and produced a valid bottleneck report:

```text
query_prep                         0.05 sec
embedding_generation              0.20 sec
vector_db_search                  0.45 sec
post_processing                   0.02 sec
-------------------------------------------
TOTAL                             0.72 sec

BOTTLENECK: vector_db_search
```

This verified that the tracker itself can measure stages and identify the largest contributor.

### End-to-end timing validation

The RAG test was also instrumented at the graph invocation level. One three-question run produced:

```text
graph_invoke_q1                  16.73 sec
graph_invoke_q2                  44.77 sec
graph_invoke_q3                   7.75 sec
-------------------------------------------
TOTAL                            69.25 sec

BOTTLENECK: graph_invoke_q2
```

The second query was the follow-up question:

```text
Explain it in more detail.
```

This establishes that follow-up execution can be substantially slower, but this outer measurement alone does **not** identify which internal node is responsible. Node-level timing remains a debugging/observability refinement rather than a reason to change the RAG architecture blindly.

### Important instrumentation lesson

The tracker is in-memory. Inspecting a newly imported tracker from a separate `python -c` process will correctly show:

```text
stages = {}
```

because that is a new Python process and a new tracker instance. This is not evidence that the tracker failed.

For production/concurrent use, tracker state should eventually become request-scoped rather than a module-global object.

---

## 32.5 Ingestion performance investigation

A 70+ page Explainable AI PDF was uploaded as a realistic ingestion stress test. Ingestion was observed running for more than two minutes.

This triggered a separate performance investigation because ingestion latency and query latency are different pipelines.

The intended ingestion timing breakdown is:

```text
file handling
    ↓
document loading/parsing
    ↓
overview generation
    ↓
chunking
    ↓
embedding generation
    ↓
Pinecone upsert
```

The project should not assume that embeddings or Pinecone are the bottleneck until the same document is measured stage-by-stage.

A standalone retrieval timing test showed `vector_db_search` as the largest contributor for that isolated test, but this must not be interpreted as proof that Pinecone is the bottleneck for full-document ingestion.

### Current status

- Performance instrumentation exists.
- Query-level baseline exists.
- Retrieval timing test passes.
- Full ingestion stage profiling is still an open optimization task.

---

## 32.6 Generation/rewrite latency findings

During CRAG testing, the following provider-level timings were observed with NVIDIA:

```text
Relevance grading:
    ≈ 17.22 sec

Query rewriting:
    ≈ 70.61 sec

Some generation calls:
    > 5 minutes observed
```

The rewrite node itself is not computationally expensive. It constructs a small prompt and waits for the provider chain:

```text
rewrite_query
    ↓
fast_provider_chain.invoke()
    ↓
NVIDIA
```

Therefore the ~70 second rewrite time is primarily provider/model invocation latency, not Python query-rewriting logic.

Similarly, a generation request that remains stuck for several minutes indicates a provider invocation/fallback/timeout problem before it can be considered a pure RAG-generation problem.

### Resulting design decision

Before optimizing individual CRAG nodes, stabilize the provider layer with bounded request timeouts and reliable fallback.

The project should also distinguish between:

```text
FAST workload
- contextualization
- relevance grading
- query rewriting
- hallucination classification

QUALITY workload
- final answer generation
```

Simple classification/rewrite tasks do not necessarily need the same large model used for final generation.

This fast-vs-quality model separation is a planned optimization, not yet fully implemented.

---

## 32.7 Provider-rate-limit observation

During a run using:

```text
Groq → Cerebras → OpenRouter → NVIDIA
```

Groq produced a fast response in at least one successful path, but console output also showed rate-limit / too-many-request behavior during development.

This reinforces the need for:

- provider fallback;
- bounded retries;
- timeout handling;
- provider-specific diagnostics;
- configurable provider order.

The goal is not to always use the theoretically fastest provider. The goal is to obtain the best practical combination of **latency, availability, quota, and answer quality**.

---

## 32.8 Testing milestones completed in this phase

The following validations were completed:

### Provider configuration test

Confirmed configured provider availability without exposing credentials:

```text
Groq       = configured
Cerebras   = configured
NVIDIA     = configured
OpenRouter = configured
Bedrock    = not configured/enabled
```

### Provider fallback test

Cerebras returned:

```text
HTTP 402 payment_required
```

The chain successfully fell back and produced a response from another provider.

### RAG test

The standalone RAG test was corrected to construct the graph using the real PostgreSQL checkpointer:

```text
build_graph(checkpointer)
```

The end-to-end RAG path was successfully executed.

### Retrieval test

Passed successfully after the retrieval scoring/overview retrieval correction.

### Timing test

Passed successfully and correctly identified a bottleneck in the synthetic retrieval timing workload.

---

## 32.9 Current architecture after these changes

The current system should be understood as:

```text
                         USER
                           │
                           ▼
                    Streamlit UI
                           │
                           ▼
                       FastAPI
                           │
                           ▼
                    PostgreSQL state
                           │
                           ▼
                       LangGraph
                           │
              ┌────────────┴────────────┐
              │                         │
       contextualize              retrieval
                                        │
                              ┌─────────┴─────────┐
                              │                   │
                         overview             content
                              │                   │
                              └─────────┬─────────┘
                                        ▼
                              scored retrieval
                                        │
                              confidence/metrics
                                        │
                                        ▼
                              relevance grading
                                  │           │
                              relevant     irrelevant
                                  │           │
                                  │       rewrite/retrieve
                                  │           │
                                  └─────┬─────┘
                                        ▼
                                    generation
                                        │
                                        ▼
                                hallucination check
                                        │
                                        ▼
                                   record turn
                                        │
                                        ▼
                                      END

LLM layer underneath all LLM nodes:

Groq → Cerebras → OpenRouter → NVIDIA
          configurable/fallback order
```

The architecture is still **Corrective / Advanced RAG**, not yet a true tool-using agent.

---

# 33. Current Development Position — Updated

The project is currently in a **stabilization and optimization checkpoint immediately before the Agentic phase**.

### Completed / working

```text
FastAPI backend                              ✅
Streamlit conversational UI                 ✅
PostgreSQL checkpointing                     ✅
Pinecone retrieval                           ✅
Document overview retrieval                  ✅
Contextual follow-up handling                ✅
Corrective relevance grading                 ✅
Query rewriting/re-retrieval                 ✅
Grounded generation                          ✅
Hallucination checking                       ✅
Multi-provider LLM abstraction              ✅
Provider fallback                            ✅
Retrieval scoring/metrics                    ✅
Retrieval timing test                        ✅
End-to-end RAG validation                    ✅
```

### In progress / known issues

```text
Provider timeout/fallback hardening           🔧
Provider-level latency diagnostics            🔧
Fast-vs-quality model separation              🔧
Generation prompt/context size profiling      🔧
Full ingestion bottleneck profiling            🔧
Request-scoped performance tracker             🔧
Adaptive CRAG threshold calibration            🔧
```

### Next major implementation phase

After the provider/performance baseline is sufficiently stable:

```text
Current RAG
    ↓
Expose RAG retrieval as a tool
    ↓
Add calculator tool
    ↓
Add web-search tool
    ↓
LLM-driven tool selection
    ↓
Tool execution loop
    ↓
Tool-result observation/reasoning
    ↓
Multi-step Agentic RAG
```

MCP should be introduced later, after ordinary tool calling is understood and working.

---

# 34. Current Optimization Strategy

The project will **not** optimize by blindly deleting CRAG components.

The preferred sequence is:

```text
1. Stabilize provider calls
       ↓
2. Bound provider latency with timeouts
       ↓
3. Improve fallback behavior
       ↓
4. Separate fast vs quality LLM workloads
       ↓
5. Calibrate retrieval-confidence thresholds
       ↓
6. Make relevance grading conditional
       ↓
7. Reduce unnecessary rewrite/re-retrieval cycles
       ↓
8. Optimize generation context size
       ↓
9. Measure quality + latency + LLM call count
       ↓
10. Freeze the optimized RAG baseline
       ↓
11. Build the agent/tool layer
```

### Optimization objective

Every optimization must be judged against:

```text
LLM calls ↓
Token usage ↓
Latency ↓ or unchanged
Quality ≥ baseline
Groundedness ≥ baseline
```

A change that saves one LLM call but makes the user wait longer or lowers answer quality is **not considered successful**.

---

# 35. Handoff Instructions — Latest State

For a new chatbot/LLM continuing this project:

1. Read this `PROJECT.md` before asking the user to explain the architecture.
2. Treat current source code as authoritative if it conflicts with historical notes.
3. Do not remove CRAG simply because it adds LLM calls; the goal is adaptive/selective CRAG.
4. Do not assume NVIDIA latency is representative of every provider.
5. Do not add arbitrary provider-specific logic to graph nodes; provider reliability belongs in the provider abstraction.
6. Do not optimize retrieval `k`, rewriting, or context size without measurements.
7. The retrieval scoring infrastructure exists specifically to support future adaptive CRAG routing.
8. The timing infrastructure exists, but it is currently primarily a development diagnostic and should not be treated as a finished production observability system.
9. The next major architectural milestone remains **tool-enabled Agentic RAG**, but provider reliability and the RAG baseline should be sufficiently stable before adding tool complexity.
10. Preserve the existing RAG subsystem. The intended agent should use it as a capability/tool rather than replacing it.
