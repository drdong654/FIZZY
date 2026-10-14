import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

Session = sessionmaker(bind=engine)
session = Session()

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("No DATABASE provided. Please set the URL environment variable")

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=database_url)
# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async with AsyncSessionLocal() as session:
    pass