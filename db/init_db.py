import asyncio

from asyncpg import connection
from sqlalchemy import text
from db.database import engine
from db.models import Base


async def main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
