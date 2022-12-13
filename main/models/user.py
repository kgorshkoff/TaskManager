from django.contrib.auth.models import AbstractUser
from django.db import models

from main.services import public_storage


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices
    )
    avatar_picture = models.ImageField(null=True, storage=public_storage)
