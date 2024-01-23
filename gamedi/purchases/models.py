from django.db import models

from games.models import Game
from users.models import User


class PurchaseStatus(models.TextChoices):
    """Перечисление статусов покупок."""
    PENDING = 'pending', 'Платеж создан и ожидает действий от пользователя.'
    SUCCEEDED = 'succeeded', 'Платеж успешно завершен.'
    CANCELED = 'canceled', 'Платеж отменен.'


class Purchase(models.Model):
    """Модель для хранения информации о покупках."""
    idempotence_key = models.UUIDField(
        editable=False,
        unique=True,
    )
    payment_id = models.UUIDField(
        editable=False,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='users',
        verbose_name='Покупатель',
        editable=False,
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        related_name='games',
        verbose_name='Игра',
        editable=False,
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Окончательная цена',
        blank=True,
        editable=False,
    )
    income_without_tax = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Доход без учета налогов',
        default=0,
        editable=False,
    )
    status = models.CharField(
        max_length=20,
        choices=PurchaseStatus.choices,
        default=PurchaseStatus.PENDING,
        verbose_name='Статус',
        editable=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата заказа',
        editable=False,
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
        editable=False,
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
