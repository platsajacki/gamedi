from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

from .utils import get_cover_path, get_hover_path
from core.models import NameString, Discription, SlugModel, FileModel


class Gener(NameString, Discription, SlugModel, models.Model):
    """Модель для хранения информации о жанре игр."""
    ...

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Game(NameString, Discription, SlugModel, models.Model):
    """Модель для хранения информации о игре."""
    cover = models.ImageField(
        upload_to=get_cover_path,
        verbose_name='Обложка',
        unique=True
    )
    hover_cover = models.ImageField(
        upload_to=get_hover_path,
        verbose_name='Наведение на обложку',
        unique=True
    )
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

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

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

    @staticmethod
    def get_files_filds() -> tuple[str]:
        """Получает строчное наименование полей с файлами."""
        return ('cover', 'hover_cover')


class AdminGameFile(NameString, FileModel, models.Model):
    """Модель для хранения файлов, принадлежащих играм."""
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='admin_files',
        verbose_name='Игра',
    )

    class Meta:
        verbose_name = 'Файл игры для администратора'
        verbose_name_plural = 'Файлы игр для администратора'


class UserGameFile(NameString, FileModel, models.Model):
    """Модель для хранения файлов, принадлежащих играм."""
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='users_files',
        verbose_name='Игра',
    )

    class Meta:
        verbose_name = 'Файл игры для пользователя'
        verbose_name_plural = 'Файлы игр для пользователя'
