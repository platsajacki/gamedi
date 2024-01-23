from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http.response import HttpResponseBase


class UserGameDispatch:
    """Миксин для проверки доступа к игре в профиле для пользователей."""
    def dispatch(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponseBase:
        """Текущий пользователь доступ к игре в профиле? Если нет, вызывает исключение PermissionDenied."""
        if request.user.is_anonymous or (
            request.user.username != kwargs['username']
            or request.user.is_authenticated
            and request.user.username == kwargs['username']
            and not request.user.games.filter(slug=kwargs['slug']).exists()
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc]
