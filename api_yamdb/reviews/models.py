from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    roles = ('user', 'moderator', 'admin')
    bio = models.TextField(
        verbose_name='Биография', 
        blank=True
        )
    role = models.CharField(choices=roles)
    