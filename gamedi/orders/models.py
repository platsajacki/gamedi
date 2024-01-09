from typing import Any

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

    def save(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self.price = self.game.final_price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
