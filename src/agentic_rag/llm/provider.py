"""Provider-agnostic LLM layer with two configurable tiers and fallback."""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from agentic_rag.config import settings

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


_MODELS: dict[str, dict[str, str]] = {
    "primary": {
        "groq": settings.groq_model,
        "cerebras": settings.cerebras_model,
        "nvidia": settings.nvidia_model,
        "openrouter": settings.openrouter_model,
        "bedrock": settings.bedrock_model,
    },
    "fast": {
        "groq": settings.groq_fast_model,
        "cerebras": settings.cerebras_fast_model,
        "nvidia": settings.nvidia_fast_model,
        "openrouter": settings.openrouter_fast_model,
        "bedrock": settings.bedrock_fast_model,
    },
}


class ProviderChain:
    """Configurable LLM provider chain with automatic fallback."""

    def __init__(self, tier: str = "primary") -> None:
        if tier not in _MODELS:
            raise ValueError(
                f"Invalid tier '{tier}'. Expected one of {list(_MODELS.keys())}."
            )

        self.tier = tier
        self._last_provider: str | None = None
        self._providers = self._build_providers()

        if not self._providers:
            raise RuntimeError(
                f"No LLM provider initialized for tier '{self.tier}'. "
                "Check .env settings for API keys and PROVIDER_ORDER."
            )

        logger.info(
            "LLM provider chain initialized (%s tier): %s",
            self.tier,
            [name for name, _ in self._providers],
        )

    @property
    def timeout(self) -> float:
        return (
            settings.fast_llm_timeout
            if self.tier == "fast"
            else settings.primary_llm_timeout
        )

    def _build_providers(self) -> list[tuple[str, BaseChatModel]]:
        available = {
            "groq": self._build_groq,
            "cerebras": self._build_cerebras,
            "nvidia": self._build_nvidia,
            "openrouter": self._build_openrouter,
            "bedrock": self._build_bedrock,
        }

        configured_order = [
            provider.strip().lower()
            for provider in settings.provider_order.split(",")
            if provider.strip()
        ]

        providers: list[tuple[str, BaseChatModel]] = []

        for provider_name in configured_order:
            builder = available.get(provider_name)
            if builder is None:
                logger.warning(
                    "Unknown provider '%s' in PROVIDER_ORDER. Skipping.",
                    provider_name,
                )
                continue

            try:
                provider = builder()
                if provider is not None:
                    providers.append((provider_name, provider))
            except Exception as exc:
                logger.warning(
                    "Could not initialize provider '%s' (%s tier): %s",
                    provider_name,
                    self.tier,
                    exc,
                )

        return providers

    def _build_groq(self) -> BaseChatModel | None:
        if not settings.groq_api_key:
            logger.info("Groq skipped: GROQ_API_KEY not configured.")
            return None

        from langchain_groq import ChatGroq

        return ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=_MODELS[self.tier]["groq"],
            timeout=self.timeout,
        )

    def _build_cerebras(self) -> BaseChatModel | None:
        if not settings.cerebras_api_key:
            logger.info("Cerebras skipped: CEREBRAS_API_KEY not configured.")
            return None

        from langchain_cerebras import ChatCerebras

        return ChatCerebras(
            api_key=settings.cerebras_api_key,
            model=_MODELS[self.tier]["cerebras"],
            timeout=self.timeout,
        )

    def _build_nvidia(self) -> BaseChatModel | None:
        if not settings.nvidia_api_key:
            logger.info("NVIDIA skipped: NVIDIA_API_KEY not configured.")
            return None

        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=settings.nvidia_api_key,
            base_url=settings.nvidia_base_url,
            model=_MODELS[self.tier]["nvidia"],
            timeout=self.timeout,
        )

    def _build_openrouter(self) -> BaseChatModel | None:
        if not settings.openrouter_api_key:
            logger.info("OpenRouter skipped: OPENROUTER_API_KEY not configured.")
            return None

        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            model=_MODELS[self.tier]["openrouter"],
            timeout=self.timeout,
        )

    def _build_bedrock(self) -> BaseChatModel | None:
        if not settings.bedrock_enabled or not settings.aws_bedrock_region:
            logger.info("Bedrock skipped: disabled or AWS region not configured.")
            return None

        from langchain_aws import ChatBedrockConverse

        return ChatBedrockConverse(
            region_name=settings.aws_bedrock_region,
            model=_MODELS[self.tier]["bedrock"],
        )

    def invoke(self, prompt: Any):
        """Invoke providers in configured order until one succeeds."""
        last_error: Exception | None = None

        for index, (name, llm) in enumerate(self._providers, start=1):
            try:
                logger.info(
                    "[LLM:%s] Attempt %d/%d → %s",
                    self.tier,
                    index,
                    len(self._providers),
                    name,
                )
                response = llm.invoke(prompt)
                self._last_provider = name
                logger.info("[LLM:%s] %s → SUCCESS", self.tier, name)
                return response
            except Exception as exc:
                logger.warning(
                    "[LLM:%s] %s → FAILED: %s",
                    self.tier,
                    name,
                    exc,
                )
                last_error = exc

        raise RuntimeError(
            f"All configured LLM providers failed for {self.tier} tier. "
            f"Last error: {last_error}"
        )

    def as_langchain_llm(self) -> BaseChatModel:
        return self._providers[0][1]

    @property
    def primary_provider(self) -> str:
        return self._providers[0][0]

    @property
    def last_provider(self) -> str | None:
        return self._last_provider

    @property
    def provider_names(self) -> list[str]:
        return [name for name, _ in self._providers]


provider_chain = ProviderChain(tier="primary")
fast_provider_chain = ProviderChain(tier="fast")
