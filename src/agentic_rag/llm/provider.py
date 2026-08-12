"""Provider-agnostic LLM layer, split into two tiers with dynamic fallback ordering.

'primary' - Larger, 70B-class models used for generate() where answer quality and reasoning matter.
'fast'    - Smaller, high-throughput models (e.g., Llama-3.1-8B, Qwen-2.5) optimized for prompt-tuned 
            classification, query rewriting, grading, and guardrail checks.

Configured providers:
    - Groq
    - Cerebras
    - NVIDIA NIM
    - OpenRouter
    - AWS Bedrock (optional)

Fallback order within each tier is controlled via `settings.provider_order`.
"""

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

# Multi-tier model definitions with fallback options per provider
_MODELS: dict[str, dict[str, str]] = {
    "primary": {
        "groq": getattr(settings, "groq_primary_model", "llama-3.3-70b-versatile"),
        "cerebras": getattr(settings, "cerebras_primary_model", "llama-3.3-70b"),
        "nvidia": getattr(settings, "nvidia_primary_model", "meta/llama-3.3-70b-instruct"),
        "openrouter": getattr(settings, "openrouter_primary_model", "meta-llama/llama-3.3-70b-instruct"),
        "bedrock": getattr(settings, "bedrock_primary_model", "us.meta.llama3-3-70b-instruct-v1:0"),
    },
    "fast": {
        "groq": getattr(settings, "groq_fast_model", "llama-3.1-8b-instant"),
        "cerebras": getattr(settings, "cerebras_fast_model", "llama3.1-8b"),
        "nvidia": getattr(settings, "nvidia_fast_model", "meta/llama-3.1-8b-instruct"),
        "openrouter": getattr(settings, "openrouter_fast_model", "qwen/qwen-2.5-7b-instruct"),
        "bedrock": getattr(settings, "bedrock_fast_model", "us.meta.llama3-1-8b-instruct-v1:0"),
    },
}


class ProviderChain:
    """Configurable LLM provider chain with automatic fallback.

    `tier` dictates which model profile is initialized for the chain:
      - 'primary': high-capability, 70B+ parameter models.
      - 'fast': high-throughput, low-latency models for classification, grading, and routing.
    """

    def __init__(self, tier: str = "primary") -> None:
        if tier not in _MODELS:
            raise ValueError(f"Invalid tier '{tier}'. Expected one of {list(_MODELS.keys())}.")

        self.tier = tier
        self._last_provider: str | None = None
        self._providers = self._build_providers()

        if not self._providers:
            raise RuntimeError(
                f"No LLM provider initialized for tier '{self.tier}'. "
                "Check your .env settings for API keys and PROVIDER_ORDER."
            )

        logger.info(
            "LLM provider chain initialized (%s tier): %s",
            self.tier,
            [name for name, _ in self._providers],
        )

    # =========================================================
    # Provider construction
    # =========================================================

    def _build_providers(self) -> list[tuple[str, BaseChatModel]]:
        available = {
            "groq": self._build_groq,
            "cerebras": self._build_cerebras,
            "nvidia": self._build_nvidia,
            "openrouter": self._build_openrouter,
            "bedrock": self._build_bedrock,
        }

        # Retrieve provider order from settings or default sequence
        raw_order = getattr(settings, "provider_order", "groq,cerebras,nvidia,openrouter,bedrock")
        configured_order = [
            p.strip().lower() for p in raw_order.split(",") if p.strip()
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

    # =========================================================
    # Provider-specific builders
    # =========================================================

    def _build_groq(self) -> BaseChatModel | None:
        if not getattr(settings, "groq_api_key", None):
            logger.info("Groq skipped: GROQ_API_KEY not configured.")
            return None

        from langchain_groq import ChatGroq

        model_name = _MODELS[self.tier]["groq"]
        return ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=model_name,
        )

    def _build_cerebras(self) -> BaseChatModel | None:
        if not getattr(settings, "cerebras_api_key", None):
            logger.info("Cerebras skipped: CEREBRAS_API_KEY not configured.")
            return None

        from langchain_cerebras import ChatCerebras

        model_name = _MODELS[self.tier]["cerebras"]
        return ChatCerebras(
            api_key=settings.cerebras_api_key,
            model=model_name,
        )

    def _build_nvidia(self) -> BaseChatModel | None:
        if not getattr(settings, "nvidia_api_key", None):
            logger.info("NVIDIA skipped: NVIDIA_API_KEY not configured.")
            return None

        from langchain_openai import ChatOpenAI

        model_name = _MODELS[self.tier]["nvidia"]
        base_url = getattr(settings, "nvidia_base_url", "https://integrate.api.nvidia.com/v1")
        return ChatOpenAI(
            api_key=settings.nvidia_api_key,
            base_url=base_url,
            model=model_name,
        )

    def _build_openrouter(self) -> BaseChatModel | None:
        if not getattr(settings, "openrouter_api_key", None):
            logger.info("OpenRouter skipped: OPENROUTER_API_KEY not configured.")
            return None

        from langchain_openai import ChatOpenAI

        model_name = _MODELS[self.tier]["openrouter"]
        base_url = getattr(settings, "openrouter_base_url", "https://openrouter.ai/api/v1")
        return ChatOpenAI(
            api_key=settings.openrouter_api_key,
            base_url=base_url,
            model=model_name,
        )

    def _build_bedrock(self) -> BaseChatModel | None:
        bedrock_enabled = getattr(settings, "bedrock_enabled", True)
        if not bedrock_enabled or not getattr(settings, "aws_bedrock_region", None):
            logger.info("Bedrock skipped: AWS region or BEDROCK_ENABLED not configured.")
            return None

        from langchain_aws import ChatBedrockConverse

        model_name = _MODELS[self.tier]["bedrock"]
        return ChatBedrockConverse(
            region_name=settings.aws_bedrock_region,
            model=model_name,
        )

    # =========================================================
    # Invocation & Fallback Execution
    # =========================================================

    def invoke(self, prompt: Any):
        """Invokes the LLM using configured providers in order until one succeeds."""
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

    # =========================================================
    # Primary LangChain model
    # =========================================================

    def as_langchain_llm(self) -> BaseChatModel:
        """Return the primary provider for LangChain components requiring a BaseChatModel directly.

        Note:
            Automatic fallback only occurs when invoking via `ProviderChain.invoke()`.
        """
        return self._providers[0][1]

    # =========================================================
    # Properties & Diagnostics
    # =========================================================

    @property
    def primary_provider(self) -> str:
        """Return the currently configured primary provider name for this tier."""
        return self._providers[0][0]

    @property
    def last_provider(self) -> str | None:
        """Return the provider used by the most recent successful invocation."""
        return self._last_provider

    @property
    def provider_names(self) -> list[str]:
        """Names of all successfully initialized providers for this tier."""
        return [name for name, _ in self._providers]


# Singletons instantiated per tier
provider_chain = ProviderChain(tier="primary")    # Answer generation
fast_provider_chain = ProviderChain(tier="fast")  # Contextualization, grading, query rewrite, hallucination check