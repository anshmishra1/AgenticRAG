from agentic_rag.llm.provider import provider_chain


print("\n" + "=" * 60)
print("LLM PROVIDER TEST")
print("=" * 60)

print("\nConfigured providers:")
print(provider_chain.provider_names)

print("\nPrimary provider:")
print(provider_chain.primary_provider)

print("\nTesting ProviderChain...\n")

response = provider_chain.invoke(
    "Answer this in one short sentence: What is 2 + 2?"
)

print("Response:")
print(response.content)

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)