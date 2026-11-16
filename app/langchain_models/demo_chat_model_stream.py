import asyncio
from langchain_core.messages import HumanMessage, SystemMessage

from app.langchain_models.model_factory import LangChainModelFactory


async def main():
    model = LangChainModelFactory.create(
        provider="qwen",
        model="deepseek-v4.1-flash-1017",
        temperature=0.7,
        streaming=True,
    )

    messages = [
        SystemMessage(content="你是一个专业 AI Agent 课程助教。"),
        HumanMessage(content="请用三句话解释 LangChain 的 stream。"),
    ]

    full_text = ""

    async for chunk in model.astream(messages):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            full_text += chunk.content

    print("=" * 80)
    print("full_text:")
    print(full_text)


if __name__ == "__main__":
    asyncio.run(main())