import asyncio

from sqlalchemy import text
from db.database import engine
from db.models import Base

async def main():
    # Создаем все таблицы в базе данных
    async with engine.begin() as connection:  #Мы берем соединение с базой данных и начинаем транзакцию. 
                                              # async with гарантирует, что по завершении блока соединение будет освобождено.
        
        await connection.run_sync(Base.metadata.create_all)

        tables = await connection.scalars(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        )
        print(sorted(tables.all()))

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
