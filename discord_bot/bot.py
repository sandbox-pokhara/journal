import discord
import httpx
from discord import Member
from discord.ext import commands
from discord.ext.commands import Context  # type: ignore

from env import ENV

BASE_URL = ENV.BACKEND_URI

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}.")


@bot.command()
async def hello(ctx: Context):  # type: ignore
    await ctx.send("Hello, I am journal bot.")


@bot.command(name="check-in")
async def checkin(ctx: Context):  # type: ignore
    if isinstance(ctx.author, Member):
        nickname: str = ctx.author.nick or ctx.author.name
    else:
        nickname: str = ctx.author.name
    print(nickname)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/check-ins/",
                json={"nickname": nickname},
            )
        if response.status_code == 200:
            data = response.json()
            await ctx.send(data["detail"])
        else:
            print(
                f"Failed to get a valid response. Status code: {response.status_code}"
            )
            await ctx.send(
                f"Failed to check in. Error: {response.status_code} - {response.text}"
            )

    except httpx.RequestError as e:
        print(f"Error occurred while making the request: {e}")
        await ctx.send(f"An error occurred while processing your request: {e}")


def main():
    # Set up bot intents
    intents.messages = True
    intents.message_content = True
    bot.run(ENV.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
