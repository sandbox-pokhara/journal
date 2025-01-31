import secrets

from django.contrib.auth.models import User
from django.db import models


def get_default_token():
    return secrets.token_hex(20)


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"check-in #{self.pk}"


class Token(models.Model):
    key = models.CharField(
        max_length=255, unique=True, default=get_default_token
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
