from typing import Type

from django.contrib import admin
from django.http import HttpRequest

from .models import CheckIn


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin[CheckIn]):
    model: Type[CheckIn]
    list_display = (
        "id",
        "user",
        "get_user_full_name",
        "get_check_in_date",
    )

    search_fields = ("id",)

    list_filter = (
        "date_created",
        "user",
    )

    @admin.display(description="Full Name")
    def get_user_full_name(self, obj: CheckIn):
        return obj.user.get_full_name()

    @admin.display(description="Check-in date")
    def get_check_in_date(self, obj: CheckIn):
        return obj.date_created

    def get_queryset(self, request: HttpRequest):
        queryset = super().get_queryset(request)
        return queryset.select_related("user")
