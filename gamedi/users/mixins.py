from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http.response import HttpResponseBase


class UserSlug:
    """Миксин для добавления атрибутов slug к представлению пользователя."""
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserDispatch(LoginRequiredMixin):
    """Миксин для проверки доступа к представлениям для пользователей."""
    def dispatch(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponseBase:
        """
        Проверяет, имеет ли текущий пользователь доступ к представлению,
        и если нет, вызывает исключение PermissionDenied.
        """
        if request.user.username != kwargs['username']:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
