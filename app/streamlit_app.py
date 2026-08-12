"""
Streamlit frontend.

The RAG pipeline lives behind FastAPI.
This file is responsible only for:

- document upload
- ingestion
- displaying conversation history
- sending questions to the FastAPI backend
"""

import os
import uuid

import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

API_URL = os.getenv(
    "RAG_API_URL",
    "http://127.0.0.1:8000",
)


# ============================================================
# Session State
# ============================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# HTTP Session
# ============================================================

@st.cache_resource
def get_http_session() -> requests.Session:
    """
    Reuse one HTTP connection pool across Streamlit reruns.
    """
    return requests.Session()


http = get_http_session()


# ============================================================
# Page
# ============================================================

st.title("Agentic RAG assistant")

st.write(
    "Ask questions grounded in your ingested documents."
)


# ============================================================
# Document Upload
# ============================================================

st.subheader("Upload documents")

uploaded_files = st.file_uploader(
    "Add PDFs, images, or audio to the knowledge base",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "mp3",
        "wav",
        "m4a",
    ],
    accept_multiple_files=True,
)


if uploaded_files and st.button("Ingest"):

    with st.spinner("Ingesting documents..."):

        files_payload = [
            (
                "files",
                (
                    f.name,
                    f.getvalue(),
                    f.type or "application/octet-stream",
                ),
            )
            for f in uploaded_files
        ]

        response = http.post(
            f"{API_URL}/ingest",
            files=files_payload,
            timeout=300,
        )

        response.raise_for_status()

    for result in response.json():

        st.success(
            f"{result['filename']}: "
            f"{result['chunks_indexed']} chunks indexed"
        )


# ============================================================
# Divider
# ============================================================

st.divider()


# ============================================================
# Conversation History
# ============================================================

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Show grounding information only for assistant messages
        if message["role"] == "assistant":

            if message.get("grounded"):

                st.caption("Grounded in context")

            else:

                st.caption(
                    "Could not fully verify against context"
                )


# ============================================================
# New Question
# ============================================================

question = st.chat_input(
    "Ask a question about your documents..."
)


# ============================================================
# Process Question
# ============================================================

if question:

    # --------------------------------------------------------
    # Display user question immediately
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    # --------------------------------------------------------
    # Store user question
    # --------------------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question,
        }
    )


    # --------------------------------------------------------
    # Query FastAPI backend
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = http.post(
                    f"{API_URL}/query",
                    json={
                        "question": question,
                        "session_id": st.session_state.session_id,
                    },
                    timeout=120,
                )

                response.raise_for_status()

                data = response.json()

                answer = data["answer"]
                grounded = data["grounded"]

            except requests.RequestException as exc:

                answer = (
                    "I couldn't connect to the RAG backend. "
                    "Please make sure the FastAPI server is running."
                )

                grounded = False

                st.error(str(exc))


        # ----------------------------------------------------
        # Display answer
        # ----------------------------------------------------

        st.markdown(answer)

        if grounded:

            st.caption("Grounded in context")

        else:

            st.caption(
                "Could not fully verify against context"
            )


    # --------------------------------------------------------
    # Store assistant response
    # --------------------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer,
            "grounded": grounded,
        }
    )