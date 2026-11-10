import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True # 表示 Redis 返回字符串，而不是 bytes。
)

async def close_redis():
    await redis_client.aclose()