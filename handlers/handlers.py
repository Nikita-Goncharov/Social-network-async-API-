import json
from typing import Optional

from aiohttp import web
from aiohttp.typedefs import LooseHeaders
from aiohttp.web_response import Response

from database.base_orm import async_session_factory
from database.orm.users_managment_orm import select_users, create_new_user, update_user, delete_user, create_profile_for_user
from database.orm.profiles_managment_orm import get_profile, update_profile


def json_response(
    data,
    *,
    text: Optional[str] = None,
    body: Optional[bytes] = None,
    status: int = 200,
    reason: Optional[str] = None,
    headers: Optional[LooseHeaders] = None,
    content_type: str = "application/json"
) -> Response:
    """Original json_response: aiohttp.web_response.py

    """
    text = json.dumps(data, default=str)  # For my records from tables i need serialize date/datetime fields
    return Response(
        text=text,
        body=body,
        status=status,
        reason=reason,
        headers=headers,
        content_type=content_type,
    )


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
    async with async_session_factory() as session:
        try:
            match request.method:
                case "GET":
                    profile_id = int(request.rel_url.query.get("profile_id"))
                    if profile_id is not None:
                        profile = await get_profile(session, profile_id)
                        profile_response = {
                            "success": True,
                            "message": "Users list",
                            "profile": profile[0].as_dict()
                        }
                        return json_response(profile_response, headers={"Access-Control-Allow-Origin": "*"})
                    else:
                        return web.json_response(
                            {"success": False, "message": f"Error: There is no profile_id in query params"},
                            status=500
                        )
                case "POST":
                    data = await request.json()
                    user_id = data.pop("user_id")
                    await create_profile_for_user(session, user_id, data)
                    return web.json_response({"success": True, "message": "Profile added to user"}, status=200)
                case "PUT":
                    updated_profile = await request.json()
                    await update_profile(session, updated_profile)
                    return web.json_response({"success": True, "message": "Profile updated"}, status=200)
                case _:
                    return web.json_response(
                        {"success": False, "message": "Error: This method not available"},
                        status=404
                    )
        except Exception as ex:
            return web.json_response({"success": False, "message": f"Error: {ex}"}, status=500)
