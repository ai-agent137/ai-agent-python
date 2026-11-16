from app.langchain_models.langchain_provider import LangChainLLMProvider
from app.llm.base import BaseLLMProvider
from app.llm.factory import LLMProviderFactory
from app.core.config import settings

async def get_llm_provider() -> BaseLLMProvider:
    # 配置控制底层模型调用方式
    if settings.default_llm_provider.startswith("langchain_"):
        provider = settings.default_llm_provider.replace("langchain_", "")

        return LangChainLLMProvider(
            provider=provider,
            model=settings.default_model,
        )

    return LLMProviderFactory.create(
        provider=settings.default_llm_provider,
    )