import logging
import os

import discord
import django

from project.env import ENV

logger = logging.getLogger("discord")

# setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

# django imports MUST be done after django setup
from django.contrib.auth.models import User

from core.models import Absence
from core.models import CheckIn
from core.models import Holiday
from core.models import Journal
from core.models import Message
from discord_bot.commands.absences import create_absence
from discord_bot.commands.absences import list_absences
from discord_bot.commands.check_ins import attendance_summary
from discord_bot.commands.check_ins import create_check_in
from discord_bot.commands.holidays import create_holiday
from discord_bot.commands.holidays import list_upcoming_holidays
from discord_bot.commands.journals import create_journal

from .utils import get_date_from_message

EDIT_DELETE_ENABLED_CHANNELS = [
    ENV.CHECK_IN_DISCORD_CHANNEL_ID,
    ENV.ABSENCE_DISCORD_CHANNEL_ID,
    ENV.HOLIDAY_DISCORD_CHANNEL_ID,
    ENV.JOURNAL_DISCORD_CHANNEL_ID,
]


class MyClient(discord.Client):
    async def on_ready(self):
        logger.info(f"Logged on as {self.user}!")

    async def on_message_delete(self, message: discord.Message):
        try:
            if message.channel.id not in EDIT_DELETE_ENABLED_CHANNELS:
                return

            message_record = await Message.objects.aget(id=message.id)

            check_in_id = getattr(message_record, "check_in_id", None)
            absence_id = getattr(message_record, "absence_id", None)
            holiday_id = getattr(message_record, "holiday_id", None)
            journal_id = getattr(message_record, "journal_id", None)

            if check_in_id:
                check_in = await CheckIn.objects.aget(id=check_in_id)
                await check_in.adelete()

            elif absence_id:
                absence = await Absence.objects.aget(id=absence_id)
                await absence.adelete()

            elif journal_id:
                journal = await Journal.objects.aget(id=journal_id)
                await journal.adelete()

            elif holiday_id:
                holiday = await Holiday.objects.aget(id=holiday_id)
                await holiday.adelete()

        except Exception:
            logger.exception(
                "An unexpected error occured. Please check the logs."
            )
            return await message.channel.send(
                embed=discord.Embed(
                    title="❌ Oops!",
                    description=(
                        "An unexcepted error occured. Please check the logs."
                    ),
                    color=discord.Color.orange(),
                )
            )

    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ):
        try:
            if after.channel.id not in EDIT_DELETE_ENABLED_CHANNELS:
                return

            updated_message = after.content
            message_record = await Message.objects.aget(id=after.id)

            check_in_id = getattr(message_record, "check_in_id", None)
            absence_id = getattr(message_record, "absence_id", None)
            holiday_id = getattr(message_record, "holiday_id", None)
            journal_id = getattr(message_record, "journal_id", None)

            if check_in_id:
                check_in = await CheckIn.objects.aget(id=check_in_id)
                check_in.message = updated_message
                await check_in.asave()

            elif absence_id:
                absence = await Absence.objects.aget(id=absence_id)
                absence.message = updated_message
                await absence.asave()

            elif journal_id:
                journal = await Journal.objects.aget(id=journal_id)
                journal.message = updated_message
                await journal.asave()

            elif holiday_id:
                holiday = await Holiday.objects.aget(id=holiday_id)
                holiday.date = get_date_from_message(updated_message)
                holiday.description = updated_message
                await holiday.asave()

        except Exception:
            logger.exception(
                "An unexpected error occured. Please check the logs."
            )
            return await after.channel.send(
                embed=discord.Embed(
                    title="❌ Oops!",
                    description=(
                        "An unexcepted error occured. Please check the logs."
                    ),
                    color=discord.Color.orange(),
                )
            )

    async def on_message(self, message: discord.Message):
        try:
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
                if message.content.lower() == "summary":
                    return await attendance_summary(message)
                else:
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
        except Exception:
            logger.exception(
                "An unexpected error occured. Please check the logs."
            )
            return await message.channel.send(
                embed=discord.Embed(
                    title="❌ Oops!",
                    description=(
                        "An unexcepted error occured. Please check the logs."
                    ),
                    color=discord.Color.orange(),
                )
            )


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(ENV.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
