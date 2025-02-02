import os

import discord
import django
from discord import Embed
from discord import Member
from discord.ext import commands
from discord.ext.commands import Context  # type: ignore
from django.db.models import Sum
from django.utils import timezone
from django.utils.timezone import timedelta

from project.env import ENV

# setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

# django imports MUST be done after django setup
from django.contrib.auth.models import User

from core.models import Absence
from core.models import CheckIn
from core.models import Holiday
from core.models import Journal

# setup discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}.")


@bot.command(name="check-in")
async def check_in(ctx: Context[commands.Bot], message: str):
    if ctx.guild is None:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description="⚠️ This command can only be used in server channels, not in DMs.",
                color=discord.Color.red(),
            )
        )

    if isinstance(ctx.author, Member):
        nickname: str = ctx.author.nick or ctx.author.name
    else:
        nickname: str = ctx.author.name

    try:
        user = await User.objects.aget(username=nickname)
    except User.DoesNotExist:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description="User doesn't exist. Contact your administrator.",
                color=discord.Color.orange(),
            )
        )

    eight_hours_ago = timezone.now() - timedelta(hours=8)

    checkin_count = await CheckIn.objects.filter(
        user=user, date_created__gte=eight_hours_ago
    ).acount()
    if checkin_count >= 1:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description="You have already checked in today.",
                color=discord.Color.orange(),
            )
        )

    await CheckIn.objects.acreate(user=user, message=message)
    return await ctx.send(
        embed=Embed(
            title="🎉 Check-In Successful!",
            description="Check-in successful!",
            color=discord.Color.green(),
        )
    )


@bot.command(name="add-absence")
async def add_absence(ctx: Context[commands.Bot], message: str):
    if ctx.guild is None:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description="⚠️ This command can only be used in server channels, not in DMs.",
                color=discord.Color.red(),
            )
        )

    if isinstance(ctx.author, Member):
        nickname: str = ctx.author.nick or ctx.author.name
    else:
        nickname: str = ctx.author.name

    try:
        user = await User.objects.aget(username=nickname)
    except User.DoesNotExist:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description="User doesn't exist. Contact your administrator.",
                color=discord.Color.orange(),
            )
        )

    now = timezone.now()
    start_of_month = now.replace(day=1)
    total_absences = (
        await Absence.objects.filter(
            user=user, date_created__gt=start_of_month
        ).aaggregate(Sum("days"))
    )["days__sum"]

    if total_absences >= ENV.ABSENCES_ALLOWED_PER_MONTH:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description=f"You have exceeded your permitted number of absences ({ENV.ABSENCES_ALLOWED_PER_MONTH}) for this month.",
                color=discord.Color.orange(),
            )
        )

    absence = await Absence.objects.acreate(user=user, message=message)
    return await ctx.send(
        embed=Embed(
            title="🎉 Absence Submitted!",
            description=f"Absence was created successfully for user {user.username} on date {absence.date_created.date()} for {absence.days} day(s) with message {absence.message}.",
            color=discord.Color.green(),
        )
    )


@bot.command(name="add-journal")
async def add_journal(ctx: Context[commands.Bot], message: str):
    if ctx.guild is None:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description="⚠️ This command can only be used in server channels, not in DMs.",
                color=discord.Color.red(),
            )
        )

    if isinstance(ctx.author, Member):
        nickname: str = ctx.author.nick or ctx.author.name
    else:
        nickname: str = ctx.author.name

    try:
        user = await User.objects.aget(username=nickname)
    except User.DoesNotExist:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description="User doesn't exist. Contact your administrator.",
                color=discord.Color.orange(),
            )
        )

    journal = await Journal.objects.acreate(user=user, message=message)
    return await ctx.send(
        embed=Embed(
            title="🎉 Journal Created!",
            description=f"A journal was created by user {user.username} on date {journal.date_created.date()}.",
            color=discord.Color.green(),
        )
    )


@bot.command(name="add-holiday")
async def add_holiday(ctx: Context[commands.Bot], message: str, date: str):
    if ctx.guild is None:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description="⚠️ This command can only be used in server channels, not in DMs.",
                color=discord.Color.red(),
            )
        )

    if isinstance(ctx.author, Member):
        nickname: str = ctx.author.nick or ctx.author.name
    else:
        nickname: str = ctx.author.name

    try:
        user = await User.objects.aget(username=nickname)
    except User.DoesNotExist:
        return await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description="User doesn't exist. Contact your administrator.",
                color=discord.Color.orange(),
            )
        )

    holiday = await Holiday.objects.acreate(
        created_by=user, description=message, date=date
    )
    return await ctx.send(
        embed=Embed(
            title="🎉 Holiday Created!",
            description=f"Holiday on date {holiday.date} created by {holiday.created_by} for {holiday.description}.",
            color=discord.Color.green(),
        )
    )


async def generic_exception_hanlder(
    ctx: Context[commands.Bot], error: Exception
):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description=error,
                color=discord.Color.orange(),
            )
        )
    else:
        await ctx.send(
            embed=Embed(
                title="❌ Oops!",
                description=f"Unexpected exception, check bot logs.",
                color=discord.Color.orange(),
            )
        )


add_absence.error(generic_exception_hanlder)
check_in.error(generic_exception_hanlder)


def main():
    intents.messages = True
    intents.message_content = True
    bot.run(ENV.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
