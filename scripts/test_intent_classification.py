import asyncio

from app.llm.factory import LLMProviderFactory
from app.service.structured_output_service import structured_output_service


async def main():
    provider = LLMProviderFactory.create("qwen")

    questions = [
        "我的订单怎么还没发货？",
        "我想退款，怎么操作？",
        "这款衣服有黑色吗？",
        "我要找人工客服。",
    ]

    for question in questions:
        result = await structured_output_service.classify_intent(
            user_question=question,
            model="deepseek-v4.1-flash-1017",
            llm_provider=provider,
        )

        print("question:", question)
        print(result.model_dump())
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())