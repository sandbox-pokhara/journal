import discord
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import localdate
from django.utils.timezone import timedelta

from core.models import Absence
from core.models import CheckIn
from core.models import Holiday


async def summary(user: User, message: discord.Message):
    output = ""

    # attendence table
    table: list[str] = []
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
        day = "day" if days_to_cover == 1 else "days"
        table.append(f"{u.username} has {days_to_cover} {day} to cover.")
    table_str = "\n".join(table)
    output += f"**Attendance:**\n{table_str}\n\n"

    # upcoming holiday
    today = timezone.localtime(timezone.now()).date()

    holidays = Holiday.objects.filter(
        date__gte=today, date__lt=today + timedelta(days=30)
    ).order_by("date")
    if not await holidays.aexists():
        content = "No results."
    else:
        content = "\n".join(
            [
                f"**{h.date}** (**{h.date.strftime('%A')}**): {h.description}"
                async for h in holidays
            ]
        )

    output += f"**Upcoming holidays:**\n{content}\n\n"

    # list absence
    absences = Absence.objects.filter(user=user)
    if await absences.acount() <= 0:
        content = "No results."
    else:
        content = "\n".join(
            [
                f"{a.date_created.date()}, {a.days} day(s), {a.message}"
                async for a in absences
            ]
        )
    output += f"**Absences for user {user.username}:**\n{content}\n\n"

    await message.channel.send(
        embed=discord.Embed(
            title=f"🎉 Summary",
            description=output,
            color=discord.Color.green(),
        )
    )
