from collections.abc import AsyncGenerator

class MockDBSession():
    async def execute(self, sql: str) -> str:
        return f"执行 SQL：{sql}"
    async def close(self):
        print("关闭 MockDBSession")
async def get_db_session() -> AsyncGenerator[str, None]:
    db = MockDBSession()
    try:
        yield db
    finally:
        await db.close            