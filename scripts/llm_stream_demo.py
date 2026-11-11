import asyncio
import json

import httpx

from app.core.config import settings


async def main():
    if not settings.dashscope_api_key:
        raise RuntimeError("请先在 .env 中配置 DEEPSEEK_API_KEY")

    url = f"{settings.qwen_base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.dashscope_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-v4-pro-0813",
        "messages": [
            {
                "role": "user",
                "content": "请用三句话解释什么是 AI Agent。",
            }
        ],
        "temperature": 0.7,
        "stream": True,
    }

    full_answer = ""

    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream(
            "POST",
            url,
            headers=headers,
            json=payload,
        ) as response:
            print("status_code:", response.status_code)
            response.raise_for_status()

            async for line in response.aiter_lines():
                print(line)
                if not line:
                    continue

                if not line.startswith("data:"):
                    continue

                data = line.removeprefix("data:").strip()

                if data == "[DONE]":
                    break

                chunk = json.loads(data)

                # 用量统计等数据块可能没有候选内容，choices 会是空列表。
                choices = chunk.get("choices") or []
                if not choices:
                    continue

                delta = choices[0].get("delta") or {}
                content = delta.get("content")

                if content:
                    full_answer += content
                    # print(content, end="", flush=True)

    print("\n\nfull_answer:")
    print(full_answer)


if __name__ == "__main__":
    asyncio.run(main())
