import os

import discord
import django
from discord import Embed
from discord import Member
from discord.ext import commands
from discord.ext.commands import Context  # type: ignore
from django.utils import timezone
from django.utils.timezone import timedelta

from project.env import ENV

# setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

# django imports MUST be done after django setup
from django.contrib.auth.models import User

from core.models import CheckIn

# setup discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}.")


@bot.command(name="check-in")
async def checkin(ctx: Context):  # type: ignore
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

    await CheckIn.objects.acreate(user=user)
    return await ctx.send(
        embed=Embed(
            title="🎉 Check-In Successful!",
            description="Check-in successful!",
            color=discord.Color.green(),
        )
    )


def main():
    intents.messages = True
    intents.message_content = True
    bot.run(ENV.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
