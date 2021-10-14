from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (("user", "USER"), ("moderator", "MODERATOR"), ("admin", "ADMIN"))

    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(verbose_name="Биография", blank=True)
    role = models.CharField(max_length=300, choices=ROLES, default=ROLES[0][0])

    @property
    def is_admin(self):
        return self.is_superuser or self.role == "admin"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    def __str__(self):
        return self.username
