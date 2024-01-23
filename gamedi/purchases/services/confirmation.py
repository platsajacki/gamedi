import json
from dataclasses import dataclass
from requests import HTTPError

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from yookassa import Payment  # type: ignore[import-untyped]

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
            try:
                Payment.find_one(payment_id := payment.get('id'))
            except HTTPError:
                return HttpResponseNotFound()
            purchase: Purchase = get_object_or_404(
                Purchase, idempotence_key=payment.get('metadata').get('idempotence_key')
            )
            purchase.payment_id, purchase.status = payment_id, payment.get('status')
            if purchase.status == 'succeeded':
                purchase.income_without_tax = payment.get('income_amount').get('value')
                purchase.user.games.add(purchase.game)
            purchase.save()
            return HttpResponse()
        return HttpResponseNotFound()
