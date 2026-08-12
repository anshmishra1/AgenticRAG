from agentic_rag.config import settings
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    api_key=settings.nvidia_api_key,
    base_url=settings.nvidia_base_url,
    model=settings.nvidia_model,
)

print("=" * 60)
print("NVIDIA TEST")
print("=" * 60)

print(f"Model: {settings.nvidia_model}")
print(f"Endpoint: {settings.nvidia_base_url}")

response = llm.invoke(
    "Answer this in one short sentence: What is 2 + 2?"
)

print("\nResponse:")
print(response.content)

print("=" * 60)