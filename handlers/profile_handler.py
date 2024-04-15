from aiohttp import web

from database.base_orm import async_session_factory
from .json_response import json_response
from models.main_models import Profile
from models.manager import UserManager, Manager
from middleware.token_check_middleware import user_token_required


async def profile_get_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = Manager(session)
            if request.rel_url.query.get("profile_id", False):
                profile_id = int(request.rel_url.query.get("profile_id"))
                profile = await manager.get_by_id(Profile, profile_id)
                profile_response = {
                    "success": True,
                    "message": "User profile",
                    "profile": profile.as_dict()
                }
                return json_response(profile_response)
            else:
                # url params: page=1, 2, 3 .....(by default=1) and count=10, 20, 33(by default=10, maximum=100)
                page = int(request.rel_url.query.get("page", 1))
                count = int(request.rel_url.query.get("count", 10))
                count = count if count <= 100 else 100
                profiles, total_count = await manager.pagination_getting(Profile, page=page, count=count)
                profiles = [profile[0].as_dict() for profile in profiles]
                response = {
                    "success": True,
                    "message": "Profiles list",
                    "profiles": profiles,
                    "total_count": total_count
                }
                return json_response(response)
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


@user_token_required
async def profile_put_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = UserManager(session)
            request_user_token = request.headers.get("AuthToken")
            _, user = await manager.is_user_exists_by_token(request_user_token)
            updated_profile = await request.json()
            updated_profile["id"] = user.profile.id
            await manager.update(Profile, updated_profile)
            return json_response({"success": True, "message": "Profile updated"})

        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)