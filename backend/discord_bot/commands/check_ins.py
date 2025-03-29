from datetime import datetime

import discord
from django.contrib.auth.models import User

from core.models import CheckIn
from core.models import Message


async def create_check_in(user: User, message: discord.Message):
    today_date = datetime.now().date()
    checkin_count = await CheckIn.objects.filter(
        user=user, date_created__date=today_date
    ).acount()
    if checkin_count >= 1:
        return await message.channel.send(
            embed=discord.Embed(
                title="❌ Oops!",
                description="You have already checked in today.",
                color=discord.Color.orange(),
            )
        )

    check_in = await CheckIn.objects.acreate(
        user=user, message=message.content
    )
    await Message.objects.acreate(id=message.id, check_in=check_in)

    return await message.add_reaction("👋")
