import discord
import httpx
import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import CheckIn, Message, UserDetail, Webhook


async def create_check_in(user: User, message: discord.Message):
    try:
        user_detail = await UserDetail.objects.aget(user=user)
        user_tz = user_detail.timezone
    except UserDetail.DoesNotExist:
        user_tz = settings.TIME_ZONE

    tz = pytz.timezone(user_tz)
    user_local_time = timezone.now().astimezone(tz)
    user_local_midnight = user_local_time.replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    checkin_count = await CheckIn.objects.filter(
        user=user, date_created__gt=user_local_midnight
    ).acount()
    if checkin_count >= 1:
        return await message.channel.send(
            embed=discord.Embed(
                title="❌ Oops!",
                description="You have already checked in today.",
                color=discord.Color.orange(),
            )
        )

    check_in = await CheckIn.objects.acreate(user=user, message=message.content)
    await Message.objects.acreate(id=message.id, check_in=check_in)

    webhooks: list[Webhook] = []
    async for webhook in Webhook.objects.all():
        webhooks.append(webhook)

    if webhooks:
        payload = {
            "username": "Sandbox Check Ins",
            "content": f"check-in - {user.username} - {message.content}",
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

    return await message.add_reaction("👋")
