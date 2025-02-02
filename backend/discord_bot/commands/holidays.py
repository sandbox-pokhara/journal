import discord
from django.contrib.auth.models import User

from core.models import Holiday
from discord_bot.utils import get_date_from_message


async def create_holiday(user: User, message: discord.Message):
    date = get_date_from_message(message.content)
    holiday = await Holiday.objects.acreate(
        created_by=user, description=message.content, date=date
    )
    return await message.channel.send(
        embed=discord.Embed(
            title="🎉 Holiday Created!",
            description=f"Holiday on date {holiday.date} created by {holiday.created_by}.",
            color=discord.Color.green(),
        )
    )
