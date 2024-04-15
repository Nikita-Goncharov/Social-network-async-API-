import binascii
import os

from aiohttp import web
from werkzeug.security import generate_password_hash

from database.base_orm import async_session_factory
from middleware.token_check_middleware import user_token_required
from models.main_models import User, Profile
from models.manager import Manager, UserManager
from .json_response import json_response


async def login_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = UserManager(session)
            data = await request.json()
            exists, user = await manager.is_user_exists(data.get("email"), data.get("password"))
            if exists:
                if user.token == "":
                    token = binascii.hexlify(os.urandom(20)).decode()
                    await manager.update(User, {"id": user.id, "token": token})
                else:
                    token = user.token
                return json_response({"success": True, "token": token, "message": "User logged successfully"})
            else:
                return json_response({"success": False, "message": "User is not found"}, status=404)
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


async def register_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = Manager(session)
            data = await request.json()
            user_data = {
                "username": data.get("username"),
                "email": data.get("email"),
                "password_hash": generate_password_hash(data.get("password"))
            }
            user = await manager.create(User, user_data)
            profile_data = {
                "img": data.get("img"),
                "status": data.get("status"),
                "education": data.get("education"),
                "web_site": data.get("web_site"),
                "country": data.get("country"),
                "city": data.get("city"),
                "birth_date": data.get("birth_date"),
                "user": user.id
            }
            profile = await manager.create(Profile, profile_data)
            return json_response({"success": True, "message": "User created successfully"})
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


@user_token_required
async def logout_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = UserManager(session)
            request_user_token = request.headers.get("AuthToken")
            await manager.remove_user_token(request_user_token)
            return json_response({"success": True, "message": "User logout successfully"})
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


@user_token_required
async def whoami_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = UserManager(session)
            request_user_token = request.headers.get("AuthToken")
            _, user = await manager.is_user_exists_by_token(request_user_token)
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "token": user.token
            }
            return json_response({"success": True, "data": data, "message": ""})
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)