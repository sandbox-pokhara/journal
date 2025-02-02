import discord
import httpx
from discord import Color
from discord import Embed
from discord.ext.commands import Context  # type: ignore

from env import ENV
from utils import make_api_request

BASE_URL = ENV.BACKEND_URI


async def perform_checkin(message: discord.Message) -> None:
    if isinstance(message.author, discord.Member):
        nickname = (
            message.author.nick
            if message.author.nick is not None
            else message.author.name
        )
    else:
        nickname = message.author.name

    response = await make_api_request(
        f"{BASE_URL}/api/v1/check-ins/",
        payload={"nickname": nickname},
    )

    if isinstance(response, httpx.Response):
        data = response.json()
        embed = Embed(
            title="🎉 Check-In Successful!",
            description=data["detail"],
            color=Color.green(),
        )
    else:
        embed = Embed(
            title=response["title"],
            description=response["description"],
            color=response["color"],
        )

    await message.channel.send(embed=embed)
