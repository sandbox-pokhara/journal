import discord
from django.contrib.auth.models import User

from core.models import Journal


async def create_journal(user: User, message: discord.Message):
    await Journal.objects.acreate(user=user, message=message.content)
    return await message.add_reaction("✅")
