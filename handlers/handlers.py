import json

from aiohttp import web
from database.base import database_engine
from database.users_managment import select_users, create_new_user, update_user, delete_user


async def users_handler(request: web.Request) -> web.Response:
    try:
        match request.method:
            case "GET":
                # url params: page=1, 2, 3 .....(by default=1) and count=10, 20, 33(by default=10, maximum=100)
                page = int(request.rel_url.query.get("page", 1))
                count = int(request.rel_url.query.get("count", 10))
                count = count if count <= 100 else 100
                users, total_count = await select_users(database_engine, page=page, count=count)
                # Convert RowMapping objects(from database) to dicts
                users = [dict(user) for user in users]
                total_count = dict(total_count)
                users = {
                    "success": True,
                    "message": "Users list",
                    "users": users,
                    "total_count": total_count["total_users"]
                }
                return web.json_response(users, headers={"Access-Control-Allow-Origin": "*"})
            case "POST":
                new_user = await request.json()  # dict
                await create_new_user(database_engine, new_user)
                return web.json_response({"success": True, "message": "User created"}, status=200)
            case "PUT":
                updated_user = await request.json()
                await update_user(database_engine, updated_user)
                return web.json_response({"success": True, "message": "User updated"}, status=200)
            case "DELETE":
                deleted_user = await request.json()
                await delete_user(database_engine, deleted_user)
                return web.json_response({"success": True, "message": "User deleted"}, status=200)
            case _:
                return web.json_response({"success": False, "message": "This method not available"}, status=404)
    except Exception as ex:
        return web.json_response({"success": False, "message": f"Error: {ex}"}, status=500)
