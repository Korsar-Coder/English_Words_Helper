import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

with open("config.json", "r") as file:
    config = json.load(file)

class Base(DeclarativeBase):
    pass

base_url = f"postgresql+asyncpg://{config['user']}:{config['password']}@localhost/{config['database']}"

engine = create_async_engine(base_url)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session