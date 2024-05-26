import asyncio
import logging

from aiohttp_middlewares import cors_middleware
from aiohttp import web

from handlers.profile_handler import profile_get_handler, profiles_get_handler, profile_put_handler
from handlers.service_handler import github_pull_updates, api_docs
from handlers.auth_handler import logout_handler, login_handler, register_handler, whoami_handler
from handlers.post_handler import post_get_handler, post_create_handler
from handlers.un_follow_handler import un_follow_handler
from database.base_orm import add_default_data


app = web.Application(middlewares=[cors_middleware(allow_all=True, allow_credentials=True)])

if __name__ == "__main__":
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

    FORMAT = '%a %t "%r" %s %b "%{User-Agent}i"'
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    app.add_routes([
        web.get("/", api_docs),
        web.post("/api/v0.2/register", register_handler),
        web.post("/api/v0.2/login", login_handler),
        web.post("/api/v0.2/logout", logout_handler),
        web.get("/api/v0.2/whoami", whoami_handler),

        web.get("/api/v0.2/profile", profile_get_handler),
        web.get("/api/v0.2/profiles", profiles_get_handler),
        web.put("/api/v0.2/profiles", profile_put_handler),

        web.get("/api/v0.2/posts", post_get_handler),
        web.post("/api/v0.2/posts", post_create_handler),

        web.post("/api/v0.2/follow", un_follow_handler),
        web.delete("/api/v0.2/follow", un_follow_handler),

        # web.route("*", "/api/v0.1/dialogs", dialogs_handler),
        # web.route("*", "/api/v0.1/messages", messages_handler),

        web.post("/api/v0.2/pull_repository_changes", github_pull_updates),
    ])

    try:
        asyncio.run(add_default_data())  # TODO: remove in prod
        web.run_app(app, access_log=logger, access_log_format=FORMAT)
    except KeyboardInterrupt:
        exit()
    except RuntimeError:
        exit()
