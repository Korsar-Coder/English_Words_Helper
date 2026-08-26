import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path
import os
from dotenv import load_dotenv


def load_config():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    config = {}
    keys = ("USER", "DATABASE_PASSWORD", "DATABASE_NAME", "JWT_KEY")
    for key in keys:
        config[key] = os.getenv(key)
    return config


main_config = load_config()


class Base(DeclarativeBase):
    pass


base_url = f"postgresql+asyncpg://{main_config['USER']}:{main_config['DATABASE_PASSWORD']}@localhost/{main_config['DATABASE_NAME']}"

engine = create_async_engine(base_url)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
