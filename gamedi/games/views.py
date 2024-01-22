from typing import Any

from django.http import FileResponse, HttpRequest, HttpResponse
from django.views import generic

from games.mixins import UserGameDispatch
from games.models import Game
from games.services import DownloadingGameFilesService, GameProfileDetailContextService, GameProfileDetailPostService


class GameListView(generic.ListView):
    """Представление главной страницы сайта."""
    model = Game
    queryset = Game.published.all()


class GameDetailView(generic.DetailView):
    """Представление отдельной страницы игры."""
    model = Game
    queryset = Game.published.all()


class GameProfileDetailView(UserGameDispatch, generic.DetailView):
    """Представление игры в профиле пользователя."""
    model = Game
    template_name = 'games/game_profile.html'
    queryset = Game.published.all()

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Получает контекст для отображения игры в профиле пользователя."""
        return GameProfileDetailContextService(context=super().get_context_data(**kwargs))()

    def post(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponse:
        """Обрабатывает POST запрос."""
        self.object: Game = self.get_object()
        return GameProfileDetailPostService(
            request=request,
            context=super().get_context_data(),
            template_name=self.template_name,
            kwargs=kwargs,
        )()


class DownloadingGameFilesTemplateView(UserGameDispatch, generic.View):
    """Класс представления для скачивания файлов игры в виде zip-архива."""
    def get(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> FileResponse:
        """Обрабатывает GET запрос и отдает zip-архив с файлами игры пользователю."""
        return DownloadingGameFilesService(kwargs=kwargs)()
