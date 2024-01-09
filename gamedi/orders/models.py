from typing import Iterable

from django.db import models

from games.models import Game
from users.models import User


class Order(models.Model):
    """Модель для хранения информации о заказах."""
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='users',
        verbose_name='Покупатель',
        editable=False
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        related_name='games',
        verbose_name='Игра',
        editable=False
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Окончательная цена',
        blank=True,
        editable=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата заказа',
        editable=False,
    )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None
    ) -> None:
        self.price = self.game.final_price  # type: ignore[assignment]
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
