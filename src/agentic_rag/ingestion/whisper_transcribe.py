"""Audio transcription via Groq's hosted Whisper endpoint (free tier: 2,000 requests/day)."""
from pathlib import Path

from groq import Groq  # type: ignore

from agentic_rag.config import settings


def transcribe(path: str | Path) -> str:
    client = Groq(api_key=settings.groq_api_key)
    with open(path, "rb") as audio_file:
        result = client.audio.transcriptions.create(file=audio_file, model="whisper-large-v3")
    return result.text
