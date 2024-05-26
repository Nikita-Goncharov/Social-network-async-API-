from aiohttp import web

from database.base_orm import async_session_factory
from middleware.token_check_middleware import user_token_required
from models.main_models import FollowProfile
from models.manager import UserManager, FollowProfileManager
from .json_response import json_response


@user_token_required
async def un_follow_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            user_manager = UserManager(session)
            following_manager = FollowProfileManager(session)
            request_json = await request.json()
            profile_id = int(request_json.get("profile_id"))
            token = request.headers.get("Authorization")
            exists, profile = await user_manager.get_profile_by_token(token)
            match(request.method):
                case "POST":
                    if exists:
                        if await user_manager.is_profile_exists(profile_id):
                            if not await following_manager.is_following_exists(profile.id, profile_id):
                                await following_manager.create(
                                    FollowProfile,
                                    {"follower": profile.id, "who_are_followed": profile_id}
                                )
                            return json_response({"success": True, "message": "Profile followed"})
                        else:
                            return json_response(
                                {"success": False, "message": "Can`t follow that profile"},
                                status=404
                            )
                    else:
                        return json_response(
                            {"success": False, "message": "There is no user logged with that token"},
                            status=404
                        )
                case "DELETE":
                    if exists:
                        await following_manager.delete_following(profile.id, profile_id)
                        return json_response({"success": True, "message": "Profile unfollowed"})
                    else:
                        return json_response(
                            {"success": False, "message": "Can`t unfollow that profile"},
                            status=404
                        )
                case _:
                    return json_response({"success": False, "message": f"Unavailable request method"}, status=500)
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)

