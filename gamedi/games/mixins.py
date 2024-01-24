from typing import Any

from django.http import HttpRequest, HttpResponseForbidden
from django.http.response import HttpResponseBase


class UserGameDispatch:
    """Миксин для проверки доступа к игре в профиле для пользователей."""
    def dispatch(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponseBase:
        """Текущий пользователь доступ к игре в профиле? Если нет, возвращает Forbidden."""
        if request.user.is_anonymous or (
            request.user.username != kwargs['username']
            or request.user.is_authenticated
            and request.user.username == kwargs['username']
            and not request.user.games.filter(slug=kwargs['slug']).exists()
        ):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc]
