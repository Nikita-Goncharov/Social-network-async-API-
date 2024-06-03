from utils.jwt_generate import generate_user_token
from utils.json_response import json_response


def jwt_required(view):
    async def wrapper(*args, **kwargs):
        request = args[-1]
        request_jwt = request.headers.get("jwt-token")
        payload = await request.json()

        generated_jwt = generate_user_token(payload)
        if request_jwt == generated_jwt:
            response = await view(*args, **kwargs)
            return response
        else:
            return json_response({"success": False, "message": "Forbidden"}, status=403)
    return wrapper
