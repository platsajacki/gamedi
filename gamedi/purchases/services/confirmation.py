import json
from dataclasses import dataclass

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from core.services import BaseService
from purchases.models import Purchase


@dataclass
class ConfirmationService(BaseService):
    """Сервис подтверждения платежей."""
    request: HttpRequest

    def act(self) -> HttpResponseNotFound | HttpResponse:
        """Обрабатывает данные платежа, если 'succeeded' присваивает пользователю игру."""
        data: dict = json.loads(self.request.body.decode())
        if payment := data.get('object'):
            purchase: Purchase = get_object_or_404(
                Purchase, idempotence_key=payment.get('metadata').get('idempotence_key')
            )
            purchase.payment_id = payment.get('id')
            purchase.status = payment.get('status')
            if purchase.status == 'succeeded':
                purchase.income_without_tax = payment.get('income_amount').get('value')
                purchase.user.games.add(purchase.game)
            purchase.save()
            return HttpResponse()
        return HttpResponseNotFound()
