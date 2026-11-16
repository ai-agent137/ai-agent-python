import asyncio

from app.core.config import settings
from app.langchain_agents.factory import build_ecommerce_agent


async def main():
    agent = build_ecommerce_agent(
        provider=settings.default_model,
        model_name=settings.model,
    )

    async for chunk in agent.astream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "帮我查一下订单 10001 到哪了？",
                }
            ]
        },
        stream_mode="updates",
    ):
        print("chunk:")
        print(chunk)
        print("=" * 80)

    print('finish')
if __name__ == "__main__":
   asyncio.run(main())