import asyncio

from app.llm.factory import LLMProviderFactory
from app.llm.schemas import LLMRequest
from app.prompts.base import PromptScenario
from app.service.prompt_service import prompt_service


async def main():
    provider = LLMProviderFactory.create("qwen")

    messages = prompt_service.render_by_scenario(
        scenario=PromptScenario.ECOMMERCE_CUSTOMER_SERVICE,
        version="v2",
        variables={
            "user_question": "我的订单怎么还没发货？",
            "business_rules": "没有订单号不能查询具体物流；不能编造物流信息。",
            "order_info": "用户未提供订单号。",
        },
    )

    request = LLMRequest(
        model="deepseek-v4-pro-0813",
        messages=messages,
        temperature=0.3,
        stream=False,
    )

    response = await provider.chat(request)

    print("answer:")
    print(response.content)
    print("usage:")
    print(response.usage.model_dump())


if __name__ == "__main__":
    asyncio.run(main())