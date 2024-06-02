from aiohttp import web

from database.base_orm import async_session_factory
from .json_response import json_response
from models.main_models import Profile
from models.manager import UserManager, Manager, FollowProfileManager
from middleware.token_check_middleware import user_token_required


async def profile_get_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = Manager(session)
            profile_id = int(request.rel_url.query.get("profile_id"))
            profile = await manager.get_by_id(Profile, profile_id)
            profile_dict = profile.as_dict()
            profile_dict["user"] = {
                "id": profile.user_obj.id,
                "username": profile.user_obj.username,
                "email": profile.user_obj.email
            }

            profile_response = {
                "success": True,
                "message": "User profile",
                "profile": profile_dict
            }
            return json_response(profile_response)
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


async def profiles_get_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = Manager(session)
            user_manager = UserManager(session)
            following_manager = FollowProfileManager(session)
            # url params: page=1, 2, 3 .....(by default=1) and count=10, 20, 33(by default=10, maximum=100)
            page = int(request.rel_url.query.get("page", 1))
            count = int(request.rel_url.query.get("count", 10))
            request_user_token = request.headers.get("Authorization")

            count = count if count <= 100 else 100
            profiles, total_count = await manager.pagination_getting(Profile, page=page, count=count)

            if request_user_token is not None:
                exists, profile = await user_manager.get_profile_by_token(request_user_token)
                if exists:
                    followed_profiles = await following_manager.get_followed_profile_ids(profile.id)
                else:
                    return json_response({"success": False, "message": f"Error: There is no user logged with that token"}, status=404)
            else:
                followed_profiles = []

            profiles_json_list = []
            for profile in profiles:
                profile = profile[0]
                profile_dict = profile.as_dict()

                if request_user_token is not None:
                    profile_dict["followed"] = True if profile_dict["id"] in followed_profiles else False

                profile_dict["user"] = {"id": profile.user_obj.id, "username": profile.user_obj.username, "email": profile.user_obj.email}
                profiles_json_list.append(profile_dict)
            response = {
                "success": True,
                "message": "Profiles list",
                "profiles": profiles_json_list,
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
            request_user_token = request.headers.get("Authorization")
            _, user = await manager.is_user_exists_by_token(request_user_token)
            updated_profile = await request.json()
            updated_profile["id"] = user.profile.id
            await manager.update(Profile, updated_profile)
            return json_response({"success": True, "message": "Profile updated"})

        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)