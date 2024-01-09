from django.contrib.auth.models import AbstractUser
from django.db import models

from games.models import Game
from users.managers import CustomUserManager


class User(AbstractUser):
    """Модель для хранения информации о пользователях."""
    email = models.EmailField(
        blank=False, unique=True,
        verbose_name='Электронная почта'
    )
    games = models.ManyToManyField(
        Game,
        related_name='users',
        verbose_name='Игры',
        blank=True,
    )

    objects = CustomUserManager()  # type: ignore[misc]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
