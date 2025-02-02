import discord
from discord.ext import commands
from discord.ext.commands import Context  # type: ignore

from channels.check_in import perform_checkin
from env import ENV

BASE_URL = ENV.BACKEND_URI
HEADERS = {
    "Authorization": f"Bearer {ENV.BACKEND_AUTH_TOKEN}",
}
checkin_terms = [
    "good morning",
    "good day",
    "good afternoon",
    "good evening",
    "good day sirs",
]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}.")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.channel.id == int(ENV.CHECKIN_CHANNEL_ID):
        if message.content.lower() in checkin_terms:
            await perform_checkin(message=message)
        else:
            embed = discord.Embed(
                title="❌ Invalid Check-In Term",
                description=f"Sorry,It's nor valid format. That.\nValid check-in terms are: {', '.join(checkin_terms)}",
                color=discord.Color.red(),
            )
            await message.channel.send(embed=embed)

    await bot.process_commands(message)


def main():
    intents.messages = True
    intents.message_content = True
    bot.run(ENV.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
