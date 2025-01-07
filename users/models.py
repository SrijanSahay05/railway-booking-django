from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    username = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_passenger = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ["email", "user_type"]

    def __str__(self):
        return self.username


