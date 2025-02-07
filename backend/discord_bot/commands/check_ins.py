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
from core.models import Message


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
    await Message.objects.acreate(id=message.id, check_in=check_in)

    return await message.add_reaction("👋")


async def attendance_summary(message: discord.Message):

    table: list[list[Any]] = []
    async for u in User.objects.all():
        total_days = (
            localdate(timezone.now()) - localdate(u.date_joined)
        ).days + 1
        holidays = await Holiday.objects.filter(
            date__gte=localdate(u.date_joined),
            date__lte=localdate(timezone.now()),
        ).acount()
        check_ins = await CheckIn.objects.filter(user=u).acount()
        absences = await Absence.objects.filter(user=u).acount()
        days_to_cover = total_days - holidays - check_ins - absences
        table.append(
            [
                u.username,
                total_days,
                check_ins,
                absences,
                holidays,
                days_to_cover,
                "yes" if days_to_cover <= 0 else "no",
            ]
        )

    table_str = tabulate(
        table,
        headers=[
            "username",
            "total_days",
            "check_ins",
            "absences",
            "holidays",
            "days_to_cover",
            "is_on_track",
        ],
        tablefmt="rounded_outline",
    )

    return await message.channel.send(f"```{table_str}```")
