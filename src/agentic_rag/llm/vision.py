"""Vision-capable image captioning, using a multimodal model on Groq.

Llama 4 Scout (the original vision model here) was deprecated by Groq in June 2026.
Llama 4 Maverick is the current active vision-capable model on the same provider/key.
"""
import base64
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from agentic_rag.config import settings

_VISION_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"


def caption_image(path: str | Path) -> str:
    """Describes an image in detail via a multimodal LLM call. Returns plain text
    so it can be embedded and retrieved exactly like any other document chunk."""
    image_bytes = Path(path).read_bytes()
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    mime = "image/png" if Path(path).suffix.lower() == ".png" else "image/jpeg"

    vision_llm = ChatGroq(groq_api_key=settings.groq_api_key, model_name=_VISION_MODEL)
    message = HumanMessage(content=[
        {
            "type": "text",
            "text": "Describe this image in detail, including any visible text, "
                    "so it can be searched and retrieved later.",
        },
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
    ])
    response = vision_llm.invoke([message])
    return response.content