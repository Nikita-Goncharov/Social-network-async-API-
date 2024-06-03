from utils.json_response import json_response
from models.manager import UserManager
from database.base_orm import async_session_factory


def user_token_required(view):
    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            request = args[-1]
            request_user_token = request.headers.get("Authorization")
            if request_user_token is not None:
                manager = UserManager(session)
                exists, user = await manager.is_user_exists_by_token(request_user_token)
                if exists:
                    response = await view(*args, **kwargs)
                    return response
                else:
                    return json_response({"success": False, "message": "There is no user logged for this token"}, status=404)
            else:
                return json_response({"success": False, "message": "Forbidden, there is no token in header"}, status=403)
    return wrapper
