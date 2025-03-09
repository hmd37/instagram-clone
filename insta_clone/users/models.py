from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True,
        blank=True, null=True
    )
    email = models.EmailField(
        unique=True, blank=True, null=True
    )
    password = models.CharField(
        max_length=128
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True
    )
    bio = models.TextField(
        blank=True
    )
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following'
    )

    def __str__(self):
        return self.username
