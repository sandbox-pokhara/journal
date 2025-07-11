import secrets

import pytz
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def get_default_token():
    return secrets.token_hex(20)


class UserDetail(models.Model):
    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_detail"
    )
    timezone = models.CharField(
        max_length=50, choices=TIMEZONE_CHOICES, default="Asia/Kathmandu"
    )

    def __str__(self):
        return f"{self.user.username} detail"


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    message = models.TextField(default="", blank=True)

    def __str__(self):
        return f"CheckIn #{self.pk}"


class Absence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.PositiveSmallIntegerField(default=1)
    date_created = models.DateTimeField(default=timezone.now)
    message = models.TextField(default="", blank=True)
    is_paid = models.BooleanField(default=True)

    def __str__(self):
        return f"Absence #{self.pk}"


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    message = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Journal #{self.pk}"


class Holiday(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date = models.DateField()
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.description


class Message(models.Model):
    id = models.BigIntegerField(primary_key=True)
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE,
        related_name="message_journal",
        null=True,
        blank=True,
    )
    absence = models.ForeignKey(
        Absence,
        on_delete=models.CASCADE,
        related_name="message_absence",
        null=True,
        blank=True,
    )
    check_in = models.ForeignKey(
        CheckIn,
        on_delete=models.CASCADE,
        related_name="message_check_in",
        null=True,
        blank=True,
    )
    holiday = models.ForeignKey(
        Holiday,
        on_delete=models.CASCADE,
        null=True,
        related_name="message_holiday",
        blank=True,
    )


class Token(models.Model):
    key = models.CharField(max_length=255, unique=True, default=get_default_token)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)


class JournalRelayWebhook(models.Model):
    webhook_url = models.URLField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
