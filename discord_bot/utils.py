from typing import Any
from typing import Dict
from typing import TypedDict
from typing import Union

import httpx
from discord import Color

from env import ENV

HEADERS = {
    "Authorization": f"Bearer {ENV.BACKEND_AUTH_TOKEN}",
}


class ErrorResponse(TypedDict):
    status: str
    title: str
    description: str
    color: Color


async def make_api_request(
    url: str, payload: Dict[str, Any]
) -> Union[httpx.Response, ErrorResponse]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=HEADERS)

        if response.status_code == 200:
            return response

        elif response.status_code == 400:
            data = response.json()
            return {
                "status": "error",
                "title": "❌ Oops!",
                "description": data.get("detail", "Bad Request"),
                "color": Color.orange(),
            }

        elif response.status_code == 401:
            return {
                "status": "error",
                "title": "🔒 Unauthorized",
                "description": (
                    "You are not authorized to perform this action."
                ),
                "color": Color.red(),
            }

        elif response.status_code == 500:
            return {
                "status": "error",
                "title": "🚨 Server Error",
                "description": "Please try again later.",
                "color": Color.red(),
            }

        else:
            return {
                "status": "error",
                "title": "⚠️ Unknown Error",
                "description": f"Status code: {response.status_code}",
                "color": Color.red(),
            }

    except httpx.RequestError as e:
        print(f"Error occurred while making the request: {e}")
        return {
            "status": "error",
            "title": "🚨 Server Error",
            "description": f"Error details: {e}",
            "color": Color.red(),
        }
