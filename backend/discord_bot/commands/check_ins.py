import discord
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import timedelta

from core.models import CheckIn


async def create_check_in(user: User, message: discord.Message):
    eight_hours_ago = timezone.now() - timedelta(hours=8)
    checkin_count = await CheckIn.objects.filter(
        user=user, date_created__gte=eight_hours_ago
    ).acount()
    if checkin_count >= 1:
        return await message.channel.send(
            embed=discord.Embed(
                title="❌ Oops!",
                description="You have already checked in today.",
                color=discord.Color.orange(),
            )
        )

    check_in = await CheckIn.objects.acreate(
        user=user, message=message.content
    )
    return await message.channel.send(
        embed=discord.Embed(
            title="🎉 Check-In Successful!",
            description=(
                f"User {check_in.user.username} checked in at"
                f" {check_in.date_created.date()}."
            ),
            color=discord.Color.green(),
        )
    )
