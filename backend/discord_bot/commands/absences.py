import discord
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone

from core.models import Absence
from project.env import ENV


async def create_absence(user: User, message: discord.Message):

    now = timezone.now()
    start_of_month = now.replace(day=1)
    total_absences = (
        await Absence.objects.filter(
            user=user, date_created__gt=start_of_month
        ).aaggregate(Sum("days"))
    )["days__sum"] or 0

    if total_absences >= ENV.ABSENCES_ALLOWED_PER_MONTH:
        return await message.channel.send(
            embed=discord.Embed(
                title="❌ Oops!",
                description=f"You have exceeded your permitted number of absences ({ENV.ABSENCES_ALLOWED_PER_MONTH}) for this month.",
                color=discord.Color.orange(),
            )
        )

    absence = await Absence.objects.acreate(user=user, message=message.content)
    return await message.channel.send(
        embed=discord.Embed(
            title="🎉 Absence Submitted!",
            description=f"Absence was created successfully for user {user.username} on date {absence.date_created.date()}.",
            color=discord.Color.green(),
        )
    )


async def list_absences(user: User, message: discord.Message):
    absences = Absence.objects.filter(user=user)
    if await absences.acount() <= 0:
        content = "No absences found for the user."
    else:
        content = "\n".join(
            [
                f"{a.date_created.date()}, {a.days} day(s), {a.message}"
                async for a in absences
            ]
        )
    return await message.channel.send(
        embed=discord.Embed(
            title=f"🎉 Absences for User {user.username}!",
            description=content,
            color=discord.Color.green(),
        )
    )
