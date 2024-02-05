import asyncio

from aiohttp import web

from handlers.handlers import users_handler, profiles_handler
from database.base_orm import add_default_data


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.route("*", "/api/v0.1/users", users_handler),
        web.route("*", "/api/v0.1/profiles", profiles_handler),
        # web.route("*", "/api/v0.1/posts", posts_handler),
        # web.route("*", "/api/v0.1/dialogs", dialogs_handler),
        # web.route("*", "/api/v0.1/messages", messages_handler),
    ])
    asyncio.run(add_default_data())
    web.run_app(app)
