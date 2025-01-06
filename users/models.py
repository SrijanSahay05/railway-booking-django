from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("passenger", "Passenger"),
        ("staff", "Staff"),
        ("admin", "Admin"),
    )
    username = models.CharField(max_length=150, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ["email", "user_type"]

    def __str__(self):
        return self.username
