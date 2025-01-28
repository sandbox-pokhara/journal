from django.contrib.auth.models import User
from django.db import models


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check-in by {self.user} at {self.date_created}"


class Absence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
