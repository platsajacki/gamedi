from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http.response import HttpResponseBase


class UserGameDispatch(LoginRequiredMixin):
    """Миксин для проверки доступа к игре в профиле для пользователей."""
    def dispatch(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponseBase:
        """
        Проверяет, имеет ли текущий пользователь доступ к представлению и игре,
        и если нет, вызывает исключение PermissionDenied.
        """
        if (
            request.user.username != kwargs['username']
            or request.user.is_authenticated
            and request.user.username == kwargs['username']
            and not request.user.games.filter(slug=kwargs['slug']).exists()
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
