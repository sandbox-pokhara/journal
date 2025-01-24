import discord
from discord.ext import commands
from discord.ext.commands import Context  # type: ignore

from env import ENV

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}.")


@bot.command()
async def hello(ctx: Context):  # type: ignore
    await ctx.send("Hello, I am journal bot.")


def main():
    # Set up bot intents
    intents.messages = True
    intents.message_content = True
    bot.run(ENV.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
