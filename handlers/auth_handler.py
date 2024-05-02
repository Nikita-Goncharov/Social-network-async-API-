import os
import hashlib
import binascii

from aiohttp import web

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


# TODO: check if user exists already
async def register_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = Manager(session)
            data = await request.json()
            user_data = {
                "username": data.get("username"),
                "email": data.get("email"),
                "password_hash": hashlib.md5(data.get("password").encode("utf-8")).hexdigest()
            }
            user = await manager.create(User, user_data)
            profile_data = {
                "img": "",
                "status": "",
                "education": "",
                "web_site": "",
                "country": "",
                "city": "",
                "birth_date": None,
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
            request_user_token = request.headers.get("Authorization")
            await manager.remove_user_token(request_user_token)
            return json_response({"success": True, "message": "User logout successfully"})
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


@user_token_required
async def whoami_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = UserManager(session)
            request_user_token = request.headers.get("Authorization")
            _, user = await manager.is_user_exists_by_token(request_user_token)
            _, profile = await manager.get_profile_by_token(user.token)
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "token": user.token,
                "profile": {
                    "img": profile.img,
                    "status": profile.status,
                    "education": profile.education,
                    "web_site": profile.web_site,
                    "country": profile.country,
                    "city": profile.city,
                    "birth_date": profile.birth_date
                }
            }
            return json_response({"success": True, "data": data, "message": ""})
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)