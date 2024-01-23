from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator as ASCIIValidator
from django.db import models

from games.models import Game
from users.managers import CustomUserManager


class ASCIIUsernameValidator(ASCIIValidator):
    """Валидатор ASCII с более корректным сообщением об ошибке на русском."""
    message = 'Введите правильное имя пользователя. Может содержать латинские буквы, цифры и @/./+/-/_.'


class User(AbstractUser):
    """Модель для хранения информации о пользователях."""
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        help_text='Обязательно. Не более 150 символов. Только латинские буквы, цифры и @/./+/-/_.',
        validators=[ASCIIUsernameValidator()],
        error_messages={'unique': 'Пользователь с таким именем уже существует.'},
    )
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
