import os

import jwt


def generate_user_token(payload):
    secret_key = os.environ.get('SECRET_JWT_KEY')
    return jwt.encode(payload, secret_key, algorithm="HS256")