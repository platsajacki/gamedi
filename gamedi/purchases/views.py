from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.views import generic


from purchases.services import ConfirmationService, CreatePurchaseService


class CreatePurchaseView(LoginRequiredMixin, generic.View):
    """Покупка игры."""
    def dispatch(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponseBase:
        """Если у пользователя уже есть игра, вызывает исключение PermissionDenied."""
        if request.user.is_authenticated and request.user.games.filter(slug=kwargs['slug']).exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponseRedirect:
        """Обрабатывает GET или перенаправляет на оплату."""
        return CreatePurchaseService(request=request, kwargs=kwargs)()


class ConfirmationView(generic.View):
    """Принимает статус платежа от YooKassa."""
    def post(
        self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]
    ) -> HttpResponse | HttpResponseNotFound:
        """Обрабатывет POST запрос. Отключен CSRF."""
        return ConfirmationService(request=request)()
