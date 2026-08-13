from agentic_rag.config import settings
from langchain_openai import ChatOpenAI


def main() -> None:
    if not settings.nvidia_api_key:
        print("NVIDIA test skipped: NVIDIA_API_KEY is not configured.")
        return

    llm = ChatOpenAI(
        api_key=settings.nvidia_api_key,
        base_url=settings.nvidia_base_url,
        model=settings.nvidia_model,
        timeout=settings.primary_llm_timeout,
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


if __name__ == "__main__":
    main()
