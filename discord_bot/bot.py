import discord
import httpx
from discord import Embed
from discord import Member
from discord.ext import commands
from discord.ext.commands import Context  # type: ignore

from env import ENV

BASE_URL = ENV.BACKEND_URI
HEADERS = {
    "Authorization": f"Bearer {ENV.BACKEND_AUTH_TOKEN}",
}

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
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/check-ins/",
                json={"nickname": nickname},
                headers=HEADERS,
            )

            if response.status_code == 200:
                data = response.json()
                embed = Embed(
                    title="🎉 Check-In Successful!",
                    description=data["detail"],
                    color=discord.Color.green(),
                )
            elif response.status_code == 400:
                data = response.json()
                embed = Embed(
                    title="❌ Oops!",
                    description=data["detail"],
                    color=discord.Color.orange(),
                )
            elif response.status_code == 401:
                embed = Embed(
                    title="🔒 Unauthorized",
                    description="You are not authorized to perform this action.",
                    color=discord.Color.red(),
                )
            elif response.status_code == 500:
                embed = Embed(
                    title="🚨 Server Error",
                    description="Please try again later.",
                    color=discord.Color.red(),
                )
            else:
                embed = Embed(
                    title="⚠️ Unknown Error",
                    description=f"Status code: {response.status_code}",
                    color=discord.Color.red(),
                )

            await ctx.send(embed=embed)

    except httpx.RequestError as e:
        print(f"Error occurred while making the request: {e}")
        return await ctx.send(
            embed=Embed(
                title="🚨 Server Error",
                description="Please try again later.",
                color=discord.Color.red(),
            )
        )


def main():
    intents.messages = True
    intents.message_content = True
    bot.run(ENV.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
