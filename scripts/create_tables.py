import asyncio
from app.db.init_db import init_db

async def main():
    await init_db()
    print("数据库表创建完成")
if __name__ == "__main__" :
   asyncio.run(main())