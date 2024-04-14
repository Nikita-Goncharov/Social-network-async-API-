import asyncio

from aiohttp import web

from handlers.profile_handler import profile_handler
from handlers.service_handler import github_pull_updates, api_docs
from handlers.auth_handler import logout_handler, login_handler, register_handler
from handlers.post_handler import post_handler
from database.base_orm import add_default_data


app = web.Application()

if __name__ == "__main__":
    app.add_routes([
        web.get("/", api_docs),
        web.route("*", "/api/v0.2/register", register_handler),
        web.route("*", "/api/v0.2/login", login_handler),
        web.route("*", "/api/v0.2/logout", logout_handler),

        web.route("*", "/api/v0.2/profiles", profile_handler),
        web.post("/api/v0.2/pull_repository_changes", github_pull_updates),
        web.route("*", "/api/v0.2/posts", post_handler),

        # web.route("*", "/api/v0.1/dialogs", dialogs_handler),
        # web.route("*", "/api/v0.1/messages", messages_handler),
    ])
    asyncio.run(add_default_data())
    web.run_app(app)
