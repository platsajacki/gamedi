import logging
from io import BytesIO
from os.path import basename
from typing import Any
from zipfile import ZipFile

from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic

from games.forms import RoleMessageFormSet
from games.managers.files_managers import UserGameFileQuerySet
from games.utils import send_role_and_file_email
from users.mixins import UserDispatch
from users.models import Game

logger = logging.getLogger(__name__)


class GameListView(generic.ListView):
    """Представление главной страницы сайта."""
    model = Game
    queryset = Game.published.all()


class GameDetailView(generic.DetailView):
    """Представление отдельной страницы игры."""
    model = Game
    queryset = Game.published.all()


class GameProfileDetailView(UserDispatch, generic.DetailView):
    """Представление игры в профиле пользователя."""
    model = Game
    template_name = 'users/user_game.html'
    queryset = Game.published.all()

    def get_context_data(self, need_formset: bool = True, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Получает контекст для отображения.
        Флаг "need_formset - (bool)" указывает, нужно ли включать пустой FormSet в контекст.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        if need_formset:
            formset = RoleMessageFormSet(initial=[{'role': file.name} for file in self.object.users_files.all()])
            context['formset'] = formset
        return context

    def post(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponse:
        """Обрабатывает POST запрос. При валидности FormSet направляет игрокам файлы."""
        formset = RoleMessageFormSet(request.POST)
        self.object: Game = self.get_object()
        if formset.is_valid():
            context: dict[str, Any] = self.get_context_data(need_formset=False, **kwargs)
            try:
                send_role_and_file_email(request=request, context=context, formset=formset)
            except Exception as e:
                context['exception'] = 'Ошибка отправки. Попробуйте отправить снова или скачайте полный файл с игрой.'
                logger.error(msg=e, exc_info=True)
            return self.render_to_response(context)
        context: dict[str, Any] = self.get_context_data(**kwargs)  # type: ignore
        context['formset'] = formset
        return self.render_to_response(context)


class DownloadingGameFilesTemplateView(UserDispatch, generic.TemplateView):
    """Класс представления для скачивания файлов игры в виде zip-архива."""
    def get_game_files(self) -> UserGameFileQuerySet:
        """Получает QuerySet файлов игры в кабинете указанного пользователя и для указанной игры.."""
        return get_object_or_404(Game, slug=self.kwargs['slug']).users_files.published()

    def get(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> FileResponse:  # type: ignore
        """Формирует zip-архив и отдает его пользователю."""
        with ZipFile(zip_buffer := BytesIO(), 'w') as zip_file:
            for file in self.get_game_files():
                zip_file.write(file.file.path, basename(file.file.path))
        zip_buffer.seek(0)
        return FileResponse(zip_buffer, as_attachment=True, filename=f'{kwargs["slug"]}_files.zip')
