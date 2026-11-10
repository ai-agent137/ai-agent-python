from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
# 异步数据库引擎
engine = create_async_engine(
    settings.database_url,
    # 是否会打印 SQL
    echo=settings.debug,
    # 表示连接池使用连接前先检查连接是否可用
    pool_pre_ping=True
)
# 异步 Session 工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)