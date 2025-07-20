import discord
import httpx
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone

from core.models import Absence, Message, Webhook
from project.env import ENV


async def create_absence(user: User, message: discord.Message):
    now = timezone.now()
    start_of_month = now.replace(day=1)
    total_absences = (
        await Absence.objects.filter(
            user=user,
            date_created__gt=start_of_month,
        ).aaggregate(Sum("days"))
    )["days__sum"] or 0

    if total_absences >= ENV.ABSENCES_ALLOWED_PER_MONTH:
        absence = await Absence.objects.acreate(
            user=user,
            message=message.content,
            is_paid=False,
        )
        await Message.objects.acreate(id=message.id, absence=absence)
        return await message.add_reaction("❌")

    absence = await Absence.objects.acreate(
        user=user,
        message=message.content,
        is_paid=True,
    )
    await Message.objects.acreate(id=message.id, absence=absence)

    webhooks: list[Webhook] = []
    async for webhook in Webhook.objects.all():
        webhooks.append(webhook)

    if webhooks:
        payload = {
            "username": "Sandbox Journal",
            "content": f"absence - {user.username} - {message.content}",
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

    return await message.add_reaction("🫡")
