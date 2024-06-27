from aiohttp import web

from models.main_models import Message, Dialog
from utils.json_response import json_response
from database.base_orm import async_session_factory
from models.manager import UserManager, Manager, MessageManager
from middleware.token_check_middleware import user_token_required


@user_token_required
async def message_get_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            message_manager = MessageManager(session)
            user_manager = UserManager(session)
            request_user_token = request.headers.get("Authorization")

            page = int(request.rel_url.query.get("page", 1))
            count = int(request.rel_url.query.get("count", 10))
            dialog_id = int(request.rel_url.query.get("dialog_id"))

            count = count if count <= 100 else 100
            _, profile = await user_manager.get_profile_by_token(request_user_token)

            messages, total_count = await message_manager.pagination_getting_messages_by_dialog(dialog_id, page=page, count=count)
            messages = [message[0].as_dict() for message in messages]
            response = {
                "success": True,
                "message": "Messages list",
                "messages": messages,
                "total_count": total_count
            }
            return json_response(response)
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


@user_token_required
async def message_post_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = Manager(session)
            user_manager = UserManager(session)
            request_user_token = request.headers.get("Authorization")
            request_body = await request.json()
            dialog_id = request_body["dialog_id"]
            _, profile = await user_manager.get_profile_by_token(request_user_token)
            message_data = {
                "text": request_body["text"],
                "owner": profile.id,
                "dialog": dialog_id
            }

            # TODO: check if this profile have permissions to dialog
            dialog = await manager.get_by_id(Dialog, dialog_id)
            if dialog is not None:
                await manager.create(Message, message_data)
                return json_response({"success": True, "message": "Message created successfully"})
            else:
                return json_response({"success": False, "message": "There is no that dialog"}, status=404)
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)
