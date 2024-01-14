from typing import Iterable

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from core.models import Description, NameString, OrderNumberModel, PublishedModel, SlugModel
from games.managers import GameManager, GameQuerySet
from games.utils import get_cover_path, get_hover_path
from games.validators import validate_order_number


class Game(NameString, Description, SlugModel, OrderNumberModel, PublishedModel, models.Model):
    """Модель для хранения информации о игре."""
    name = models.CharField(
        max_length=128, unique=True,
        verbose_name='Наименование'
    )
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
        'games.Genre',
        on_delete=models.PROTECT,
        related_name='games',
        verbose_name='Жанр'
    )
    min_players = models.PositiveSmallIntegerField(
        verbose_name='Минимальное количество игроков'
    )
    max_players = models.PositiveSmallIntegerField(
        verbose_name='Максимальное количество игроков'
    )
    time = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                limit_value=24,
                message='Количество часов должно быть меньше или равно 24'
            )
        ],
        verbose_name='Количество игровых часов'
    )
    age_restriction = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                limit_value=18,
                message='Возрастные ограничения могут быть от 0+ до 18+.'
            )
        ],
        verbose_name='Возрастные ограничения'
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        verbose_name='Цена'
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        verbose_name='Скидка (%)'
    )
    final_price = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        verbose_name='Окончательная цена',
        blank=True,
        null=True,
        editable=False,
    )

    objects = GameQuerySet.as_manager()
    published = GameManager()

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ('order_number',)

    def clean(self) -> None:
        """Проверка валидности полей."""
        if self.min_players and self.max_players and self.min_players > self.max_players:
            raise ValidationError('Минимальное количество игроков не может быть больше максимального.')
        validate_order_number(self.order_number, self.is_published)
        super().clean()

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None
    ) -> None:
        """Высчитывает final_price перед сохранением."""
        self.final_price = round(self.price * (1 - self.discount / 100), 0)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    @staticmethod
    def get_files_filds() -> tuple[str, str]:
        """Получает строчное наименование полей с файлами."""
        return ('cover', 'hover_cover')
