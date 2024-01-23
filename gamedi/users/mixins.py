from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http.response import HttpResponseBase


class UserSlug:
    """Миксин для добавления атрибутов slug к представлению пользователя."""
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserDispatch:
    """Миксин для проверки доступа к представлениям для пользователей."""
    def dispatch(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponseBase:
        """Текущий пользователь доступ к представлению? Если нет, вызывает исключение PermissionDenied."""
        if request.user.is_anonymous or request.user.is_authenticated and request.user.username != kwargs['username']:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc]
