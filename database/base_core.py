import os
import asyncio

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

from database.core.users_managment_core import add_default_users

load_dotenv()

user = os.environ.get('DBUSER')
password = os.environ.get('DBPASSWORD')
host = os.environ.get('DBHOST')
name = os.environ.get('DBNAME')

# Postgresql: f"postgresql+asyncpg://{user}:{password}@{host}:5432/{name}"
# MySQL:

database_engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{name}")


async def add_default_data(db=database_engine):
    users_task = asyncio.create_task(add_default_users(db))
    await users_task

