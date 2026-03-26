import asyncio
from app.db.connection import engine
from app.db.base import Base

from app.models.user_sql import UserSQL

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())
