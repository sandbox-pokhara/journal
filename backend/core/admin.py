from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin  # type: ignore

from .models import (
    Absence,
    CheckIn,
    Holiday,
    Journal,
    Message,
    Token,
    UserDetail,
    Webhook,
)


@admin.register(UserDetail)
class UserDetailAdmin(DjangoQLSearchMixin, admin.ModelAdmin[UserDetail]):
    list_display = ("id", "user", "timezone")
    autocomplete_fields = ("user",)


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
        "days",
        "is_paid",
        "date_created",
    )
    list_filter = ("date_created",)


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


@admin.register(Message)
class MessageAdmin(DjangoQLSearchMixin, admin.ModelAdmin[Message]):
    list_display = (
        "id",
        "check_in",
        "absence",
        "holiday",
        "journal",
    )


@admin.register(Token)
class TokenAdmin(DjangoQLSearchMixin, admin.ModelAdmin[Token]):
    list_display = ["key", "user", "date_created"]
    fields = ("user",)
    autocomplete_fields = ["user"]


@admin.register(Webhook)
class WebhookAdmin(DjangoQLSearchMixin, admin.ModelAdmin[Webhook]):
    list_display = ["webhook_url", "date_created"]
