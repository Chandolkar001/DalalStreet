from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_no = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.username)

class Portfolio(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    balance = models.BigIntegerField(default=2000000)

    def __str__(self):
        return str(self.user.username)

