import json

from aiohttp import web
from database.base import database_engine
from database.users_managment import select_all_users, create_new_user, update_user, delete_user


async def users_handler(request):
    match request.method:
        case "GET":
            users = await select_all_users(database_engine)

            # Convert Row objects(from database) to dicts
            users = [user._asdict() for user in users]  # TODO: not good
            users = {
                "users": users
            }
            users_json = json.dumps(users)
            return web.json_response(users_json, headers={"Access-Control-Allow-Origin": "*"})
        case "POST":
            new_user = await request.json()  # dict
            await create_new_user(database_engine, new_user)
            return web.Response(text=f"Good ?")
        case "PUT":
            return web.Response(text=f"{dir(request)}")
        case "DELETE":
            return web.Response(text=f"{dir(request)}")
