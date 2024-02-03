from typing import Any

from django.http import HttpRequest, HttpResponseForbidden
from django.http.response import HttpResponseBase


class UserSlug:
    """Миксин для добавления атрибутов slug к представлению пользователя."""
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserDispatch:
    """Миксин для проверки доступа к представлениям для пользователей."""
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """Текущий пользователь доступ к представлению? Если нет, возвращает Forbidden."""
        if request.user.is_anonymous or request.user.is_authenticated and request.user.username != kwargs['username']:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc]
