import secrets

from django.contrib.auth.models import User
from django.db import models


def get_default_token():
    return secrets.token_hex(20)


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default="", blank=True)

    def __str__(self):
        return f"CheckIn #{self.pk}"


class Absence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.PositiveSmallIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default="", blank=True)
    is_partial = models.BooleanField(default=False)
    is_break = models.BooleanField(default=False)

    def __str__(self):
        return f"Absence #{self.pk}"


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Journal #{self.pk}"


class Holiday(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.description


class Token(models.Model):
    key = models.CharField(
        max_length=255, unique=True, default=get_default_token
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
