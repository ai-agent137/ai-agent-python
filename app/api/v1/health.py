from fastapi import APIRouter, HTTPException, Depends
from redis.asyncio import Redis
from app.dependencies.redis import get_redis_client
from app.dependencies.settings import get_app_settings
router = APIRouter()

async def get_request_source() -> str:
    return "dependency"




@router.get("/health")
async def health_check(
    settings: str = Depends(get_app_settings),
):
    return {
        "status": "ok",
        "service": settings.app_name,
        "env": settings.app_env,
        "version": settings.app_version,
        }
@router.get("/health/redis")
async def redis_health(
    redis: Redis = Depends(get_redis_client),
):
    pong = await redis.ping()

    return {
        "status": "ok" if pong else "error",
        "redis": pong,
    }



@router.get("/error-demo")
async def error_demo():
    raise HTTPException(
        status_code=400,
        detail="这是一个错误示例"
    )

@router.get("/system-error-demo")
async def system_error_demo():
    result = 1 / 0
    return {
        "result": result
    }