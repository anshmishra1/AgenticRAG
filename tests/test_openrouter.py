from agentic_rag.config import settings
from langchain_openai import ChatOpenAI


def main() -> None:
    if not settings.openrouter_api_key:
        print("OpenRouter test skipped: OPENROUTER_API_KEY is not configured.")
        return

    llm = ChatOpenAI(
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_base_url,
        model=settings.openrouter_model,
        timeout=settings.primary_llm_timeout,
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


if __name__ == "__main__":
    main()
