from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin  # type: ignore

from .models import Absence
from .models import CheckIn
from .models import Holiday
from .models import Journal
from .models import Token


@admin.register(CheckIn)
class CheckInAdmin(DjangoQLSearchMixin, admin.ModelAdmin[CheckIn]):
    list_display = (
        "id",
        "user",
        "message",
        "date_created",
    )
    list_filter = ("date_created",)


@admin.register(Absence)
class AbsenceAdmin(DjangoQLSearchMixin, admin.ModelAdmin[Absence]):
    list_display = (
        "id",
        "user",
        "message",
        "is_partial",
        "is_break",
        "days",
        "date_created",
    )
    list_filter = (
        "date_created",
        "is_partial",
        "is_break",
    )


@admin.register(Journal)
class JournalAdmin(DjangoQLSearchMixin, admin.ModelAdmin[Journal]):
    list_display = (
        "id",
        "user",
        "message",
        "date_created",
    )
    list_filter = ("date_created",)


@admin.register(Holiday)
class HolidayAdmin(DjangoQLSearchMixin, admin.ModelAdmin[Holiday]):
    list_display = (
        "id",
        "description",
        "date",
        "created_by",
        "date_created",
    )
    list_filter = ("date_created",)


@admin.register(Token)
class TokenAdmin(DjangoQLSearchMixin, admin.ModelAdmin[Token]):
    list_display = ["key", "user", "date_created"]
    fields = ("user",)
    autocomplete_fields = ["user"]
