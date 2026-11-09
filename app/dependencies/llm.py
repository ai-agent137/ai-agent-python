from app.core.config import settings

class MockLLMProvider:
    def __init__(self, model: str):
        self.model = model

    async def chat(self, messages: str) -> str:
        return f"[{self.model} 模拟回答：{ messages}]"


async def get_llm_provider() -> MockLLMProvider:
    return MockLLMProvider(model=settings.default_model)