from typing import Any

import discord
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import localdate
from django.utils.timezone import timedelta
from tabulate import tabulate

from core.models import Absence
from core.models import CheckIn
from core.models import Holiday


async def summary(user: User, message: discord.Message):
    # upcoming holiday
    today = timezone.localtime(timezone.now()).date()

    holidays = Holiday.objects.filter(
        date__gte=today, date__lt=today + timedelta(days=30)
    )
    content = "\n".join([f"{h.date}: {h.description}" async for h in holidays])

    upcoming_holiday_embed = discord.Embed(
        title="🎉 Upcoming Holidays!",
        description=content,
        color=discord.Color.green(),
    )

    # list absence
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
    list_absence_embed = discord.Embed(
        title=f"🎉 Absences for User {user.username}!",
        description=content,
        color=discord.Color.green(),
    )

    # attendence table
    table: list[list[Any]] = []
    async for u in User.objects.all():
        total_days = (
            localdate(timezone.now()) - localdate(u.date_joined)
        ).days + 1
        holidays_count = await Holiday.objects.filter(
            date__gte=localdate(u.date_joined),
            date__lte=localdate(timezone.now()),
        ).acount()
        check_ins = await CheckIn.objects.filter(user=u).acount()
        absences = await Absence.objects.filter(user=u).acount()
        days_to_cover = total_days - holidays_count - check_ins - absences

        table.append([u.username, f"{check_ins}/{absences}/{days_to_cover}"])
    attendance_table = tabulate(
        table,
        headers=["username", "result"],
        tablefmt="rounded_outline",
    )
    attendance_info = "\nresult = check-ins/absences/days-to-cover\n"

    await message.channel.send(
        f"```{attendance_table}{attendance_info}```",
        embeds=[upcoming_holiday_embed, list_absence_embed],
    )
