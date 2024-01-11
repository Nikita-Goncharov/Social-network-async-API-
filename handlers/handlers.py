from aiohttp import web
from sqlalchemy import text

from database.base import engine

async def users_handler(request):
    match request.method:
        case "GET":
            async with engine.begin() as conn:
                await conn.execute(text("create table if not exists test_table (x int, y int)"))
                await conn.execute(text("INSERT INTO test_table (x, y) VALUES (:x, :y)"), [{"x": 1, "y": 1}, {"x": 2, "y": 4}])
                await conn.commit()
            return web.Response(text="GET REQUEST")
        case "POST":
            return web.Response(text="POST REQUEST")
        case "PUT":
            return web.Response(text="PUT REQUEST")
        case "DELETE":
            return web.Response(text="DELETE REQUEST")
