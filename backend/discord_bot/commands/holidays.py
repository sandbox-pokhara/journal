from datetime import timedelta

import discord
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import Holiday
from core.models import Message
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

    return await message.add_reaction("👍")


async def list_upcoming_holidays(message: discord.Message):
    today = timezone.localtime(timezone.now()).date()

    holidays = Holiday.objects.filter(
        date__gte=today, date__lt=today + timedelta(days=30)
    )
    content = "\n".join([f"{h.date}: {h.description}" async for h in holidays])
    return await message.channel.send(
        embed=discord.Embed(
            title="🎉 Upcoming Holidays!",
            description=content,
            color=discord.Color.green(),
        )
    )
