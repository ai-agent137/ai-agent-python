import asyncio

from app.redis.client import close_redis, redis_client


async def main():
    pong = await redis_client.ping()
    print("PING:", pong)

    await redis_client.set("course:name", "AI Agent 全栈开发实战", ex=60)
    value = await redis_client.get("course:name")
    print("course:name =", value)

    ttl = await redis_client.ttl("course:name")
    print("ttl =", ttl)

    await close_redis()


if __name__ == "__main__":
    asyncio.run(main())