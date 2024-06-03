from aiohttp import web

from database.base_orm import async_session_factory
from utils.json_response import json_response
from models.main_models import Post
from models.manager import PostManager, UserManager
from middleware.token_check_middleware import user_token_required


async def post_get_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            post_manager = PostManager(session)
            # url params: page=1, 2, 3 .....(by default=1) and count=10, 20, 33(by default=10, maximum=100)
            page = int(request.rel_url.query.get("page", 1))
            count = int(request.rel_url.query.get("count", 10))
            profile_id = int(request.rel_url.query.get("profile_id", 0))

            count = count if count <= 100 else 100
            posts, total_count = await post_manager.pagination_getting_posts_from_profile(profile_id, page=page, count=count)
            posts = [post[0].as_dict() for post in posts]
            response = {
                "success": True,
                "message": "Posts list",
                "posts": posts,
                "total_count": total_count
            }
            return json_response(response)
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)


@user_token_required
async def post_create_handler(request: web.Request) -> web.Response:
    async with async_session_factory() as session:
        try:
            post_manager = PostManager(session)
            user_manager = UserManager(session)
            post_data = await request.json()
            request_user_token = request.headers.get("Authorization")
            _, user = await user_manager.is_user_exists_by_token(request_user_token)  # we already check if exists in middleware
            post_data["profile"] = user.profile.id
            new_post = await post_manager.create(Post, post_data)
            return json_response({"success": True, "post_id": new_post.id, "message": "Post added"})
        except Exception as ex:
            return json_response({"success": False, "message": f"Error: {str(ex)}"}, status=500)
