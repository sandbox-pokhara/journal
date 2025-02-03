import os

import discord
import django

from project.env import ENV

# setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

# django imports MUST be done after django setup
from django.contrib.auth.models import User

from discord_bot.commands.absences import create_absence
from discord_bot.commands.absences import list_absences
from discord_bot.commands.check_ins import create_check_in
from discord_bot.commands.holidays import create_holiday
from discord_bot.commands.holidays import list_upcoming_holidays
from discord_bot.commands.journals import create_journal


class MyClient(discord.Client):

    async def on_message(self, message: discord.Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        # parse nickname
        if isinstance(message.author, discord.Member):
            nickname: str = message.author.nick or message.author.name
        else:
            nickname: str = message.author.name

        # check if user exists
        try:
            user = await User.objects.aget(username=nickname)
        except User.DoesNotExist:
            return await message.channel.send(
                embed=discord.Embed(
                    title="❌ Oops!",
                    description=(
                        "User doesn't exist. Contact your administrator."
                    ),
                    color=discord.Color.orange(),
                )
            )

        # handle check ins
        if message.channel.id == ENV.CHECK_IN_DISCORD_CHANNEL_ID:
            return await create_check_in(user, message)

        # handle absences
        if message.channel.id == ENV.ABSENCE_DISCORD_CHANNEL_ID:
            if message.content.lower() == "list absences":
                return await list_absences(user, message)
            else:
                return await create_absence(user, message)

        # handle journals
        if message.channel.id == ENV.JOURNAL_DISCORD_CHANNEL_ID:
            return await create_journal(user, message)

        # handle holidays
        if message.channel.id == ENV.HOLIDAY_DISCORD_CHANNEL_ID:
            if message.content.lower() == "list upcoming":
                return await list_upcoming_holidays(message)
            else:
                return await create_holiday(user, message)


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(ENV.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
