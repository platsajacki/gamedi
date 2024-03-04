import json
import logging
from dataclasses import dataclass
from requests import HTTPError

from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound

from yookassa import Payment  # type: ignore[import-untyped]

from core.services import BaseService
from purchases.models import Purchase

logger = logging.getLogger(__name__)


@dataclass
class ConfirmationService(BaseService):
    """Сервис подтверждения платежей."""
    request: HttpRequest

    @transaction.atomic
    def act(self) -> HttpResponseNotFound | HttpResponse:
        """Обрабатывает данные платежа, если 'succeeded' присваивает пользователю игру."""
        try:
            data: dict = json.loads(self.request.body.decode())
            if self.request.user.is_anonymous and (payment := data.get('object')):
                Payment.find_one(payment_id := payment['id'])
                purchase = Purchase.objects.get(idempotence_key=payment['metadata']['idempotence_key'])
                purchase.payment_id, purchase.status = payment_id, payment['status']
                if purchase.status == 'succeeded':
                    purchase.income_without_tax = payment['income_amount']['value']
                    purchase.user.games.add(purchase.game)
                purchase.save()
                return HttpResponse()
        except (json.JSONDecodeError, HTTPError, Purchase.DoesNotExist, KeyError) as e:
            logger.error(msg=e, exc_info=True)
            return HttpResponseNotFound()
        return HttpResponseNotFound()
