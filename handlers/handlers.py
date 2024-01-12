import json

from aiohttp import web
from database.base import database_engine
from database.users_managment import select_all_users, create_new_user, update_user, delete_user


async def users_handler(request):
    try:
        match request.method:
            case "GET":
                users = await select_all_users(database_engine)
                # Convert Row objects(from database) to dicts
                users = [user._asdict() for user in users]  # TODO: not good
                users = {
                    "success": True,
                    "message": f"Users list",
                    "users": users
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
