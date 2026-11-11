import asyncio
import httpx

from app.core.config import settings

async def main():
    if not settings.openai_api_key:
        raise RuntimeError(".env config don' not have openai_api_key")
    url = f"{settings.openai_base_url}/responses"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4.1-mini",
        "input": "请用一句话解释什么是 AI Agent。",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            url,
            headers=headers,
            json=payload,
        )

    print("status_code:", response.status_code)
    print("response:")
    print(response.text)
if __name__ == "__main__":
    asyncio.run(main())    