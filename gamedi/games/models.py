from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

from .utils import get_file_path
from core.models import NameString, Discription


class Gener(NameString, Discription, models.Model):
    """Модель для хранения информации о жанре игр."""
    ...

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Game(NameString, Discription, models.Model):
    """Модель для хранения информации о игре."""
    genre = models.ForeignKey(
        Gener,
        on_delete=models.PROTECT,
        related_name='games',
        verbose_name='Жанр'
    )
    min_players = models.PositiveSmallIntegerField(
        verbose_name='Минимальное количество играков'
    )
    max_players = models.PositiveSmallIntegerField(
        verbose_name='Максимальное количество играков'
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Цена'
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Скидка (%)'
    )
    final_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Окончательная цена',
        blank=True,
        null=True,
        editable=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def clean(self) -> None | ValidationError:
        """Проверка валидности полей 'min_players' и 'max_players'."""
        if self.min_players > self.max_players:
            raise ValidationError(
                'Минимальное количество игроков '
                'не может быть больше максимального.'
            )
        return super().clean()

    def save(
            self, *args: tuple[Any], **kwargs: dict[str, Any]
    ) -> None:
        self.final_price = round(self.price * (1 - self.discount / 100), 0)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class GameFile(NameString, models.Model):
    """Модель для хранения файлов, принадлежащих играм."""
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Игра',
    )
    file = models.FileField(
        upload_to=get_file_path,
        verbose_name='Файл',
        unique=True
    )

    class Meta:
        verbose_name = 'Файл игры'
        verbose_name_plural = 'Файлы игр'
