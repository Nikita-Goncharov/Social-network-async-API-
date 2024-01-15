import json

from aiohttp import web
from database.base import database_engine
from database.users_managment import select_users, create_new_user, update_user, delete_user


async def users_handler(request):
    try:
        match request.method:
            case "GET":
                # url params: page=1, 2, 3 .....(by default=1) and count=10, 20, 33(by default=10, maximum=100)
                page = int(request.rel_url.query.get("page", 1))
                count = int(request.rel_url.query.get("count", 10))
                count = count if count <= 100 else 100
                users, total_count = await select_users(database_engine, page=page, count=count)
                # Convert Row objects(from database) to dicts
                users = [user._asdict() for user in users]  # TODO: not good
                total_count = total_count._asdict()
                users = {
                    "success": True,
                    "message": f"Users list",
                    "users": users,
                    "total_count": total_count
                }
                users_json = json.dumps(users)
                return web.json_response(users_json, headers={"Access-Control-Allow-Origin": "*"})
            case "POST":
                new_user = await request.json()  # dict
                await create_new_user(database_engine, new_user)
                return web.json_response({"success": True, "message": f"User created"}, status=200)
            case "PUT":
                updated_user = await request.json()
                await update_user(database_engine, updated_user)
                return web.json_response({"success": True, "message": f"User updated"}, status=200)
            case "DELETE":
                deleted_user = await request.json()
                await delete_user(database_engine, deleted_user)
                return web.json_response({"success": True, "message": f"User deleted"}, status=200)
            case _:
                return web.json_response({"success": False, "message": f"This method not available"}, status=404)
    except Exception as ex:
        return web.json_response({"success": False, "message": f"Error: {ex}"}, status=500)
