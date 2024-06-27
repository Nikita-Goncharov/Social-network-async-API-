from aiohttp import web

from models.main_models import Dialog
from utils.json_response import json_response
from database.base_orm import async_session_factory
from models.manager import DialogManager, UserManager, Manager
from middleware.token_check_middleware import user_token_required


@user_token_required
async def dialog_get_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            dialogs_manager = DialogManager(session)
            user_manager = UserManager(session)
            request_user_token = request.headers.get("Authorization")

            page = int(request.rel_url.query.get("page", 1))
            count = int(request.rel_url.query.get("count", 10))
            count = count if count <= 100 else 100
            _, profile = await user_manager.get_profile_by_token(request_user_token)
            dialogs, total_count = await dialogs_manager.pagination_getting_dialogs_for_profile(profile.id, page=page, count=count)
            dialogs = [dialog[0].as_dict() for dialog in dialogs]
            response = {
                "success": True,
                "message": "Dialogs list",
                "dialogs": dialogs,
                "total_count": total_count
            }
            return json_response(response)
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


@user_token_required
async def dialog_post_handler(request: web.Request) -> web.Response:  # TODO: can`t create dialog if exists
    async with async_session_factory() as session:
        try:
            manager = Manager(session)
            user_manager = UserManager(session)
            request_user_token = request.headers.get("Authorization")
            request_body = await request.json()
            another_person_profile_id = request_body["profile_id"]

            _, profile = await user_manager.get_profile_by_token(request_user_token)
            data = {
                "first_profile": profile.id,
                "second_profile": another_person_profile_id
            }
            await manager.create(Dialog, data)
            return json_response({"success": True, "message": "Dialog created successfully"})
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


@user_token_required
async def dialog_delete_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            dialog_manager = DialogManager(session)
            request_body = await request.json()
            dialog_id = request_body["dialog_id"]

            await dialog_manager.delete_dialog(dialog_id)
            return json_response({"success": True, "message": "Dialog created successfully"})
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)
