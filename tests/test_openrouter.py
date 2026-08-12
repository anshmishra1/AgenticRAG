from agentic_rag.config import settings
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
    model=settings.openrouter_model,
)

print("=" * 60)
print("OPENROUTER TEST")
print("=" * 60)

print(f"Model: {settings.openrouter_model}")
print(f"Endpoint: {settings.openrouter_base_url}")

response = llm.invoke(
    "Answer this in one short sentence: What is 2 + 2?"
)

print("\nResponse:")
print(response.content)

print("=" * 60)