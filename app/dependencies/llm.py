from app.llm.base import BaseLLMProvider
from app.llm.factory import LLMProviderFactory


async def get_llm_provider() -> BaseLLMProvider:
    return LLMProviderFactory.create()