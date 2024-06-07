import logging

from aiohttp import web
from aiohttp_middlewares import cors_middleware

from handlers.un_follow_handler import un_follow_handler
from handlers.service_handler import github_pull_updates, api_docs
from handlers.message_handler import message_post_handler, message_get_handler
from handlers.post_handler import post_get_handler, post_create_handler
from handlers.auth_handler import logout_handler, login_handler, register_handler, whoami_handler
from handlers.dialog_handler import dialog_get_handler, dialog_post_handler, dialog_delete_handler
from handlers.profile_handler import profile_get_handler, profiles_get_handler, profile_put_handler

API_PATH = "/api/v0.2/"


async def create_app() -> web.Application:
    app = web.Application(middlewares=[cors_middleware(allow_all=True, allow_credentials=True)])
    # LOG_FORMAT_MAP
    # "a": "remote_address",
    # "t": "request_start_time",
    # "P": "process_id",
    # "r": "first_request_line",
    # "s": "response_status",
    # "b": "response_size",
    # "T": "request_time",
    # "Tf": "request_time_frac",
    # "D": "request_time_micro",
    # "i": "request_header",
    # "o": "response_header",

    logging.basicConfig(level=logging.INFO)
    app.add_routes([
        web.get("/", api_docs),
        web.get(f"{API_PATH}", api_docs),
        web.post(f"{API_PATH}register", register_handler),
        web.post(f"{API_PATH}login", login_handler),
        web.post(f"{API_PATH}logout", logout_handler),
        web.get(f"{API_PATH}whoami", whoami_handler),

        web.get(f"{API_PATH}profile", profile_get_handler),
        web.get(f"{API_PATH}profiles", profiles_get_handler),
        web.put(f"{API_PATH}profiles", profile_put_handler),

        web.get(f"{API_PATH}posts", post_get_handler),
        web.post(f"{API_PATH}posts", post_create_handler),

        web.post(f"{API_PATH}follow", un_follow_handler),
        web.delete(f"{API_PATH}follow", un_follow_handler),

        web.get(f"{API_PATH}dialogs", dialog_get_handler),
        web.post(f"{API_PATH}dialogs", dialog_post_handler),
        web.delete(f"{API_PATH}dialogs", dialog_delete_handler),

        web.get(f"{API_PATH}messages", message_get_handler),
        web.post(f"{API_PATH}messages", message_post_handler),

        web.post(f"{API_PATH}pull_repository_changes", github_pull_updates),
    ])

    return app
