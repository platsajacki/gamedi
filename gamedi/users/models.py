from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager
from games.models import Game


class User(AbstractUser):
    """Модель для хранения информации о пользователях."""
    games = models.ManyToManyField(
        Game,
        related_name='users',
        verbose_name='Игры',
        blank=True,
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
