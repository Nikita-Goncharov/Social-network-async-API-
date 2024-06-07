import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

user = os.environ.get('DBUSER')
password = os.environ.get('DBPASSWORD')
host = os.environ.get('DBHOST')
name = os.environ.get('DBNAME')

# Postgresql: f"postgresql+asyncpg://{user}:{password}@{host}:5432/{name}"

# MySQL:
database_engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{name}")

# async_sessionmaker: a factory for new AsyncSession objects.
# expire_on_commit - don't expire objects after transaction commit
async_session_factory = async_sessionmaker(database_engine, expire_on_commit=False)
