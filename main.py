import asyncio

from aiohttp import web

from handlers.profile_handler import profile_handler
from handlers.service_handler import github_pull_updates, api_docs
from database.base_orm import add_default_data
from handlers.auth_handler import logout_handler


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/", api_docs),
        # web.route("*", "/api/v0.1/users", user_handler),
        web.route("*", "/api/v0.1/profiles", profile_handler),
        web.post("/pull_repository_changes", github_pull_updates),
        web.route("*", "/api/v0.1/logout", logout_handler),
        # web.route("*", "/api/v0.1/posts", posts_handler),
        # web.route("*", "/api/v0.1/dialogs", dialogs_handler),
        # web.route("*", "/api/v0.1/messages", messages_handler),
    ])
    asyncio.run(add_default_data())
    web.run_app(app)
