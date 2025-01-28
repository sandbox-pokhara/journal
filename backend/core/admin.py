from django.contrib import admin

from .models import CheckIn
from .models import Token


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin[CheckIn]):
    list_display = (
        "id",
        "user",
        "get_check_in_date",
    )

    search_fields = ("id",)

    list_filter = ("date_created",)

    @admin.display(description="Check-in Date")
    def get_check_in_date(self, obj: CheckIn):
        return obj.date_created


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin[Token]):
    list_display = ["key", "user", "date_created"]
    fields = ("user",)
    autocomplete_fields = ["user"]
