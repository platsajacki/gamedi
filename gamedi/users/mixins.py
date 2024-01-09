from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse

from .models import User


class UserAttribute:
    """Миксин для добавления атрибутов к представлению пользователя."""
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserDispatch:
    """Миксин для проверки доступа к представлениям для пользователей."""
    def dispatch(
            self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse | PermissionDenied:
        """
        Проверяет, имеет ли текущий пользователь доступ к представлению,
        и если нет, вызывает исключение PermissionDenied.
        """
        if request.user.username != kwargs['username']:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
