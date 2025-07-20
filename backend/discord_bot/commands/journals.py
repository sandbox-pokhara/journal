import discord
import httpx
from django.contrib.auth.models import User

from core.models import Journal, Message, Webhook


async def create_journal(user: User, message: discord.Message):
    journal = await Journal.objects.acreate(user=user, message=message.content)
    await Message.objects.acreate(id=message.id, journal=journal)

    webhooks: list[Webhook] = []
    async for webhook in Webhook.objects.all():
        webhooks.append(webhook)

    if webhooks:
        payload = {
            "username": "Sandbox Journal",
            "content": f"journal - {user.username} - {message.content}",
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
