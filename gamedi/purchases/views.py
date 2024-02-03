from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.views import generic

from purchases.services import ConfirmationService, CreatePurchaseService


class CreatePurchaseView(LoginRequiredMixin, generic.View):
    """Покупка игры."""
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """Если у пользователя уже есть игра, возвращает Forbidden."""
        if request.user.is_authenticated and request.user.games.filter(slug=kwargs['slug']).exists():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
        """Обрабатывает GET или перенаправляет на оплату."""
        return CreatePurchaseService(request=request, kwargs=kwargs)()


class ConfirmationView(generic.View):
    """Принимает статус платежа от YooKassa."""
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """Информация об оплате принимается от анонимного пользователя."""
        if request.user.is_authenticated:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse | HttpResponseNotFound:
        """Обрабатывет POST запрос. Отключен CSRF."""
        return ConfirmationService(request=request)()
