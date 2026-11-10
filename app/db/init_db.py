from app.db.base import Base
from app.db.session import engine

# 必须导入 models，确保 metadata 里能收集到数据库表
from app import models  # noqa: F401


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)