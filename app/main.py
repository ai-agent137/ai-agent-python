from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.api import api_router

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import register_middleware
from app.redis.client import close_redis
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_redis()
def createApp() -> FastAPI:
    #  设置日志
    setup_logging()
    # 初始化app
    app = FastAPI(
        title=settings.app_name,
        description="Python + FastAPI + LLM + Agent",
        version= settings.app_version,
        debug=settings.debug,
        lifespan=lifespan
    )
    # 跨域
    app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8888",
        "http://127.0.0.1:3000",
        "null",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    # 注册中间件
    register_middleware(app)
    # 注册异常管理器
    register_exception_handlers(app)
    # 注册路由
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