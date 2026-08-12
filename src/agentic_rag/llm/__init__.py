# def __init__(self) -> None:

#     self._last_provider: str | None = None

#     self._providers = self._build_providers()

#     if not self._providers:
#         raise RuntimeError(
#             "No LLM provider is configured. "
#             "Set at least one of GROQ_API_KEY, "
#             "CEREBRAS_API_KEY, NVIDIA_API_KEY, "
#             "or OPENROUTER_API_KEY."
#         )

#     logger.info(
#         "LLM provider chain initialized: %s",
#         [name for name, _ in self._providers],
#     )