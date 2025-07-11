import discord
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone

from core.models import Absence, Message
from project.env import ENV


async def create_absence(user: User, message: discord.Message):
    now = timezone.now()
    start_of_month = now.replace(day=1)
    total_absences = (
        await Absence.objects.filter(
            user=user,
            date_created__gt=start_of_month,
        ).aaggregate(Sum("days"))
    )["days__sum"] or 0

    if total_absences >= ENV.ABSENCES_ALLOWED_PER_MONTH:
        absence = await Absence.objects.acreate(
            user=user,
            message=message.content,
            is_paid=False,
        )
        await Message.objects.acreate(id=message.id, absence=absence)
        return await message.add_reaction("❌")

    absence = await Absence.objects.acreate(
        user=user,
        message=message.content,
        is_paid=True,
    )
    await Message.objects.acreate(id=message.id, absence=absence)
    return await message.add_reaction("🫡")
