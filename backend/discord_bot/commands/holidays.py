import discord
import httpx
from django.contrib.auth.models import User

from core.models import Holiday, Message, Webhook
from discord_bot.utils import get_date_from_message


async def create_holiday(user: User, message: discord.Message):
    date = get_date_from_message(message.content)

    if await Holiday.objects.filter(date=date).aexists():
        return await message.channel.send(
            embed=discord.Embed(
                title="❌ Oops!",
                description=f"Holiday already exists for date {date}.",
                color=discord.Color.orange(),
            )
        )

    holiday = await Holiday.objects.acreate(
        created_by=user, description=message.content, date=date
    )
    await Message.objects.acreate(id=message.id, holiday=holiday)

    webhooks: list[Webhook] = []
    async for webhook in Webhook.objects.all():
        webhooks.append(webhook)

    if webhooks:
        payload = {
            "username": "Sandbox Check Ins",
            "content": f"holiday - {message.content}",
        }
        headers = {"Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            for webhook in webhooks:
                try:
                    response = await client.post(
                        webhook.webhook_url, json=payload, headers=headers
                    )
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    return await message.channel.send(
                        embed=discord.Embed(
                            title="❌ Oops!",
                            description=(
                                "Failed to send webhook:"
                                f" {e.response.status_code}, {e.response.text}"
                            ),
                        )
                    )
                except httpx.RequestError as e:
                    return await message.channel.send(
                        embed=discord.Embed(
                            title="❌ Oops!",
                            description=f"An error occurred while requesting {e}.",
                        )
                    )

    return await message.add_reaction("👍")
