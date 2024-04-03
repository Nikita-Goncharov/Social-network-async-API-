from aiohttp import web

from database.base_orm import async_session_factory
# from database.orm.profiles_managment_orm import get_profile
from .json_response import json_response
from utils.jwt_generate import generate_user_token
from middleware.jwt_middleware import jwt_required


async def login_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            match request.method:
                case "POST":
                    email = ""
                    password = ""
                    exist, id = get_user_by_credencials(session, email, password)
                    profile = await get_profile(session, profile_id)
                    # payload = {
                    #     "email": profile.user.email,
                    #     "username": profile.user.username
                    # }
                    # jwt_token = generate_user_token(payload)
                    # Log user in and create token
                    return json_response({"success": True, "message": "User logged successfully"})
                case _:
                    return json_response(
                        {"success": False, "message": "Error: This method not available"},
                        status=404
                    )
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


async def register_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            match request.method:
                case "POST":
                    # TODO: Create user and profile
                    return json_response({"success": True, "message": "User created successfully"})
                case _:
                    return json_response(
                        {"success": False, "message": "Error: This method not available"},
                        status=404
                    )
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


@jwt_required
async def logout_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            match request.method:
                case "POST":
                    # TODO: logout
                    return json_response({"success": True, "message": "User logout successfully"})
                case _:
                    return json_response(
                        {"success": False, "message": "Error: This method not available"},
                        status=404
                    )
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)