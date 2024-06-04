import hmac
import hashlib


def generate_github_signature(token: bytes, payload: bytes) -> str:
    hash_object = hmac.new(token, msg=payload, digestmod=hashlib.sha1)
    expected_signature = "sha1=" + hash_object.hexdigest()
    return expected_signature
