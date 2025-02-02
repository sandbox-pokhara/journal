import discord
from django.contrib.auth.models import User

from core.models import Journal


async def create_journal(user: User, message: discord.Message):
    journal = await Journal.objects.acreate(user=user, message=message.content)
    return await message.channel.send(
        embed=discord.Embed(
            title="🎉 Journal Created!",
            description=f"A journal was created by user {user.username} on date {journal.date_created.date()}.",
            color=discord.Color.green(),
        )
    )
