from aiohttp import web
from handlers.handlers import users_handler


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.route("*", "/api/v0.1/users", users_handler),
        # web.route("*", "/api/v0.1/posts", posts_handler),
        # web.route("*", "/api/v0.1/dialogs", dialogs_handler),
        # web.route("*", "/api/v0.1/messages", messages_handler),
    ])
    web.run_app(app)
