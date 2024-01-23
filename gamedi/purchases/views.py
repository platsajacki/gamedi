from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views import generic

from purchases.services import ConfirmationService, CreatePurchaseService
from users.mixins import UserDispatch


class CreatePurchaseView(UserDispatch, generic.View):
    """Покупка игры."""
    def get(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponseRedirect:
        """Обрабатывает GET или перенаправляет на оплату."""
        return CreatePurchaseService(request=request, kwargs=kwargs)()


class ConfirmationView(generic.View):
    """Принимает статус платежа от Yookassa."""
    def post(
        self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]
    ) -> HttpResponse | HttpResponseNotFound:
        """Обрабатывет POST запрос. Отключен CSRF."""
        return ConfirmationService(request=request)()
