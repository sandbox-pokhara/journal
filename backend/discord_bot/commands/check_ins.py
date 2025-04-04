import discord
import pytz
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import CheckIn
from core.models import Message
from core.models import UserDetail


async def create_check_in(user: User, message: discord.Message):
    DEFAULT_TZ = "Asia/Kathmandu"
    try:
        user_detail = await UserDetail.objects.aget(user=user)
        user_tz = user_detail.timezone
    except UserDetail.DoesNotExist:
        user_tz = DEFAULT_TZ

    tz = pytz.timezone(user_tz)
    utc_now = timezone.now()
    local_time = utc_now.astimezone(tz)
    today_date = local_time.date()

    checkin_count = await CheckIn.objects.filter(
        user=user, date_created__date=today_date
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
        user=user, message=message.content, date_created=local_time
    )
    await Message.objects.acreate(id=message.id, check_in=check_in)

    return await message.add_reaction("👋")
