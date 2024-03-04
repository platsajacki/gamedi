from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from django.conf import settings
from django.http import HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from yookassa import Configuration, Payment  # type: ignore[import-untyped]

from core.services import BaseService
from games.models import Game
from purchases.models import Purchase
from users.models import User


@dataclass
class CreatePurchaseService(BaseService):
    request: HttpRequest
    kwargs: dict[str, Any]

    def get_game(self) -> Game:
        """Получаем игру."""
        return get_object_or_404(Game, slug=self.kwargs.get('slug'))

    def set_configuration(self) -> None:
        """Устанавливаем конфигурацию YooKassa."""
        Configuration.account_id = settings.ID_YOOKASSA
        Configuration.secret_key = settings.SECRET_KEY_YOOKASSA

    def get_payment(self, user: User, game: Game, idempotence_key: str, purchase: Purchase) -> Payment:
        """Создаем объект платежа."""
        return Payment.create(
            {
                'amount': {
                    'value': str(game.final_price),
                    'currency': 'RUB'
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': self.request.build_absolute_uri(
                        reverse('users:profile', args=(user.username,))
                    )
                },
                'capture': True,
                'description': f'№{purchase.id}. Покупка игры "{game.name}" пользователем {user.username}.',
                'metadata': {
                    'idempotence_key': purchase.idempotence_key,
                },
                'receipt': {
                    'customer': {
                        'email': user.email,
                    },
                    'items': [
                        {
                            'description': game.name,
                            'quantity': '1',
                            'amount': {
                                'value': str(game.final_price),
                                'currency': 'RUB'
                            },
                            'vat_code': '1',
                            'measure': 'piece',
                        },
                    ]
                },
            },
            idempotency_key=idempotence_key,
        )

    def act(self) -> HttpResponseRedirect | HttpResponseNotFound:
        """Создаем покупку и перенаправляем на оплату."""
        user, game, uuid = self.request.user, self.get_game(), str(uuid4())
        if user.is_anonymous or user.is_authenticated and game in user.games.all():
            return HttpResponseNotFound()
        purchase = Purchase.objects.create(
            idempotence_key=uuid, user=user, game=game, price=game.final_price  # type: ignore[misc]
        )
        self.set_configuration()
        return HttpResponseRedirect(
            self.get_payment(user=user, game=game, idempotence_key=uuid, purchase=purchase)
            .confirmation.confirmation_url
        )
