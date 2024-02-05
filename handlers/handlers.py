from aiohttp import web
from database.base_orm import async_session_factory
from database.orm.users_managment_orm import select_users, create_new_user, update_user, delete_user


async def users_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            match request.method:
                case "GET":
                    # url params: page=1, 2, 3 .....(by default=1) and count=10, 20, 33(by default=10, maximum=100)
                    page = int(request.rel_url.query.get("page", 1))
                    count = int(request.rel_url.query.get("count", 10))
                    count = count if count <= 100 else 100
                    users, total_count = await select_users(session, page=page, count=count)

                    users = [user[0].as_dict() for user in users]  # Why here user[0] ???
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
                    await create_new_user(session, new_user)
                    return web.json_response({"success": True, "message": "User created"}, status=200)
                case "PUT":
                    updated_user = await request.json()
                    await update_user(session, updated_user)
                    return web.json_response({"success": True, "message": "User updated"}, status=200)
                case "DELETE":
                    deleted_user = await request.json()
                    await delete_user(session, deleted_user)
                    return web.json_response({"success": True, "message": "User deleted"}, status=200)
                case _:
                    return web.json_response({"success": False, "message": "This method not available"}, status=404)
        except Exception as ex:
            return web.json_response({"success": False, "message": f"Error: {ex}"}, status=500)


async def profiles_handler(request: web.Request) -> web.Response:
    pass
