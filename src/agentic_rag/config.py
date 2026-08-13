"""Central application settings loaded from environment / .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the PDF RAG application.

    Defaults provide a usable local configuration while every value can be
    overridden through environment variables or .env.
    """

    # =========================================================
    # API Keys
    # =========================================================
    groq_api_key: str = ""
   