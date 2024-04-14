from aiohttp import web

from database.base_orm import async_session_factory
from .json_response import json_response
from models.main_models import Post
from models.manager import PostManager


async def post_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            manager = PostManager(session)
            match request.method:
                case "GET":
                    # url params: page=1, 2, 3 .....(by default=1) and count=10, 20, 33(by default=10, maximum=100)
                    page = int(request.rel_url.query.get("page", 1))
                    count = int(request.rel_url.query.get("count", 10))
                    profile_id = int(request.rel_url.query.get("profile_id", 0))

                    count = count if count <= 100 else 100
                    posts, total_count = await manager.pagination_getting_posts_from_profile(profile_id, page=page, count=count)
                    posts = [post[0].as_dict() for post in posts]
                    response = {
                        "success": True,
                        "message": "Posts list",
                        "posts": posts,
                        "total_count": total_count
                    }
                    return json_response(response)
                case "POST":
                    post_data = await request.json()  # TODO: check if profile it is  user own, not another user
                    await manager.create(Post, post_data)
                    return json_response({"success": True, "message": "Post added"})
                case _:
                    return json_response(
                        {"success": False, "message": "Error: This method not available"},
                        status=404
                    )
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)
