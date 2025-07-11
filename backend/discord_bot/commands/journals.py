import discord
from django.contrib.auth.models import User

from core.models import Journal, Message


async def create_journal(user: User, message: discord.Message):
    journal = await Journal.objects.acreate(user=user, message=message.content)
    await Message.objects.acreate(id=message.id, journal=journal)

    return await message.add_reaction("👍")
