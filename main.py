import asyncio

from aiohttp import web

from handlers.profile_handler import profile_get_handler, profile_put_handler
from handlers.service_handler import github_pull_updates, api_docs
from handlers.auth_handler import logout_handler, login_handler, register_handler, whoami_handler
from handlers.post_handler import post_get_handler, post_create_handler
from database.base_orm import add_default_data


app = web.Application()

if __name__ == "__main__":
    app.add_routes([
        web.get("/", api_docs),
        web.post("/api/v0.2/register", register_handler),
        web.post("/api/v0.2/login", login_handler),
        web.post("/api/v0.2/logout", logout_handler),
        web.get("/api/v0.2/whoami", whoami_handler),

        web.get("/api/v0.2/profiles", profile_get_handler),
        web.put("/api/v0.2/profiles", profile_put_handler),


        web.get("/api/v0.2/posts", post_get_handler),
        web.post("/api/v0.2/posts", post_create_handler),

        # web.route("*", "/api/v0.1/dialogs", dialogs_handler),
        # web.route("*", "/api/v0.1/messages", messages_handler),

        web.post("/api/v0.2/pull_repository_changes", github_pull_updates),
    ])
    asyncio.run(add_default_data())
    web.run_app(app)
