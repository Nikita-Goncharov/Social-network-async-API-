import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

# TODO: faker for create default users

user = os.environ.get('DBUSER')
password = os.environ.get('DBPASSWORD')
host = os.environ.get('DBHOST')
name = os.environ.get('DBNAME')

engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}:5432/{name}")
