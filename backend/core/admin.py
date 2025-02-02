from django.contrib import admin

from .models import Absence
from .models import CheckIn
from .models import Holiday
from .models import Journal
from .models import Token


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin[CheckIn]):
    list_display = (
        "id",
        "user",
        "message",
        "date_created",
    )
    list_filter = ("date_created",)


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin[Absence]):
    list_display = (
        "id",
        "user",
        "message",
        "days",
        "date_created",
    )
    list_filter = ("date_created",)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin[Journal]):
    list_display = (
        "id",
        "user",
        "message",
        "date_created",
    )
    list_filter = ("date_created",)


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin[Holiday]):
    list_display = (
        "id",
        "description",
        "date",
        "created_by",
        "date_created",
    )
    list_filter = ("date_created",)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin[Token]):
    list_display = ["key", "user", "date_created"]
    fields = ("user",)
    autocomplete_fields = ["user"]
