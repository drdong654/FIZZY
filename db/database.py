import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("No DATABASE provided. Please set the URL environment variable")

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=database_url)
# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)