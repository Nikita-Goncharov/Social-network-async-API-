import json
from typing import Optional

from aiohttp.typedefs import LooseHeaders
from aiohttp.web_response import Response


def json_response(
    data,
    *,
    text: Optional[str] = None,
    body: Optional[bytes] = None,
    status: int = 200,
    reason: Optional[str] = None,
    headers: Optional[LooseHeaders] = None,
    content_type: str = "application/json"
) -> Response:
    """Original json_response: aiohttp.web_response.py

    """

    text = json.dumps(data, default=str)  # For my records from tables i need serialize date/datetime fields
    return Response(
        text=text,
        body=body,
        status=status,
        reason=reason,
        headers=headers,
        content_type=content_type,
    )