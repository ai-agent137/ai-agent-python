from fastapi import FastAPI, Query
from app.api.v1.chat import router as chat_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.rag import router as rag_router
from app.api.v1.health import router as health_router
from app.api.v1.api import api_router

from app.core.config import settings
def createApp() -> FastAPI:
    app = FastAPI(
    title=settings.app_name,
    description="Python + FastAPI + LLM + Agent",
    version= settings.app_version,
)
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/")
    async def root():
        return {
            "appName": settings.app_name,
            "env": settings.app_env,
            "version": settings.app_version
        }
    return app
app = createApp()    