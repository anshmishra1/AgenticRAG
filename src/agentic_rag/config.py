"""Central application settings loaded from environment / .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the PDF RAG application."""

    # API Keys
    groq_api_key: str = ""
    cerebras_api_key: str = ""
    nvidia_api_key: str = ""
    openrouter_api_key: str = ""
    pinecone_api_key: str = ""
    hf_token: str = ""

    # Primary provider models
    groq_model: str = "llama-3.3-70b-versatile"
    cerebras_model: str = "gpt-oss-120b"
    nvidia_model: str = "meta/llama-3.1-70b-instruct"
    openrouter_model: str = "openai/gpt-4o-mini"
    bedrock_model: str = "meta.llama3-3-70b-instruct-v1:0"

    # Fast-tier models
    groq_fast_model: str = "llama-3.1-8b-instant"
    cerebras_fast_model: str = "llama3.1-8b"
    nvidia_fast_model: str = "meta/llama-3.1-8b-instruct"
    openrouter_fast_model: str = "qwen/qwen-2.5-7b-instruct"
    bedrock_fast_model: str = "us.meta.llama3-1-8b-instruct-v1:0"

    # Provider endpoints and fallback order
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    provider_order: str = "cerebras,groq,nvidia,openrouter"

    # LLM request timeouts
    fast_llm_timeout: float = 15.0
    primary_llm_timeout: float = 45.0

    # Bedrock
    bedrock_enabled: bool = False
    aws_bedrock_region: str = "us-east-1"

    # Vector database
    pinecone_index_name: str = "agentic-rag"

    # PostgreSQL / LangGraph checkpointing
    postgres_url: str = (
        "postgresql://postgres:postgres@localhost:5442/postgres"
        "?sslmode=disable"
    )

    # RAG / pipeline
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 1500
    chunk_overlap: int = 300
    max_retries: int = 2

    # Conversation / generation optimization
    max_history_messages_for_generation: int = 2
    max_generation_context_documents: int = 5
    max_generation_context_chars: int = 12000
    max_generation_output_chars: int = 12000

    # Retrieval assessment - absolute score gate
    retrieval_min_top_score: float = 0.35
    retrieval_strong_top_score: float = 0.55

    # Retrieval assessment - relative shape gate (used only once the absolute
    # floor above is cleared). Moved here from module-level constants in
    # nodes.py so every retrieval threshold lives in one place.
    retrieval_top_to_mean_ratio: float = 1.10
    retrieval_gap_ratio: float = 0.02
    retrieval_overview_margin: float = 0.02

    # Development
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()