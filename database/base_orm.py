import os
import asyncio

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.orm.users_managment_orm import add_default_users
from models.main_models import Base

load_dotenv()

user = os.environ.get('DBUSER')
password = os.environ.get('DBPASSWORD')
host = os.environ.get('DBHOST')
name = os.environ.get('DBNAME')

database_engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}:5432/{name}")

# async_sessionmaker: a factory for new AsyncSession objects.
# expire_on_commit - don't expire objects after transaction commit
async_session_factory = async_sessionmaker(database_engine, expire_on_commit=True)


async def add_default_data():
    async with database_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # because we should wait until tables will create
    async with async_session_factory() as session:
        users_task = asyncio.create_task(add_default_users(session))
        await users_task
    await database_engine.dispose()
    # TODO: maybe inside users ???
    # profiles_task = asyncio.create_task(add_default_profiles(db))

