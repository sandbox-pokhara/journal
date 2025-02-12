import discord
from django.contrib.auth.models import User

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
