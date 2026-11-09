from fastapi import APIRouter, HTTPException, Depends
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

@router.get("/error-demo")
async def error_demo():
    raise HTTPException(
        status_code=400,
        detail="这是一个错误示例"
    )