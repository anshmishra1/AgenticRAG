"""Central settings, loaded from environment / .env.
Never hardcode API keys elsewhere.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =========================================================
    # API Keys
    # =========================================================

    groq_api_key: str = ""
    cerebras_api_key: str = ""
    nvidia_api_key: str = ""
    openrouter_api_key: str = ""

    pinecone_api_key: str = ""
    hf_token: str = ""


    # =========================================================
    # LLM Provider Models
    # =========================================================

    groq_model: str = "llama-3.3-70b-versatile"

    # Current Cerebras public production model.
    # Also supports function calling / tools.
    cerebras_model: str = "gpt-oss-120b"

    nvidia_model: str = "meta/llama-3.1-70b-instruct"

    # OpenRouter model slug.
    # Can be changed without modifying Python code.
    openrouter_model: str = "openai/gpt-4o-mini"

    # Bedrock model will be configured when Bedrock is enabled.
    bedrock_model: str = "meta.llama3-3-70b-instruct-v1:0"


    # =========================================================
    # Provider Endpoints
    # =========================================================

    nvidia_base_url: str = (
        "https://integrate.api.nvidia.com/v1"
    )

    openrouter_base_url: str = (
        "https://openrouter.ai/api/v1"
    )


    # =========================================================
    # Provider Configuration
    # =========================================================

    # Provider priority for automatic fallback.
    #
    # Available:
    # groq
    # cerebras
    # nvidia
    # openrouter
    # bedrock
    #
    # We will make this configurable in provider.py.
    provider_order: str = (
        "cerebras,groq,nvidia,openrouter"
    )

    # Bedrock is deliberately disabled for now.
    bedrock_enabled: bool = False

    aws_bedrock_region: str = "us-east-1"


    # =========================================================
    # Vector Database
    # =========================================================

    pinecone_index_name: str = "agentic-rag"


    # =========================================================
    # PostgreSQL / LangGraph Checkpointing
    # =========================================================

    postgres_url: str = (
        "postgresql://postgres:postgres@localhost:5442/postgres"
        "?sslmode=disable"
    )


    # =========================================================
    # RAG / Pipeline Settings
    # =========================================================

    embedding_model: str = "all-MiniLM-L6-v2"

    chunk_size: int = 1500

    chunk_overlap: int = 300

    max_retries: int = 2


    # =========================================================
    # Development
    # =========================================================

    debug: bool = False


    # =========================================================
    # Pydantic Settings
    # =========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()