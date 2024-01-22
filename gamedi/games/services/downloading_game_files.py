from dataclasses import dataclass
from io import BytesIO
from os.path import basename
from typing import Any
from zipfile import ZipFile

from django.http import FileResponse
from django.shortcuts import get_object_or_404

from core.services import BaseService
from games.managers import UserGameFileQuerySet
from games.models import Game


@dataclass
class DownloadingGameFilesService(BaseService):
    """Сервис для скачивания файлов игры в виде zip-архива."""
    kwargs: dict[str, Any]

    def get_game_files(self) -> UserGameFileQuerySet:
        """Получает QuerySet файлов игры в кабинете указанного пользователя и для указанной игры.."""
        return get_object_or_404(Game, slug=self.kwargs['slug']).users_files.published()

    def act(self) -> FileResponse:
        """Формирует zip-архив и отдает его пользователю."""
        with ZipFile(zip_buffer := BytesIO(), 'w') as zip_file:
            for file in self.get_game_files():
                zip_file.write(file.file.path, basename(file.file.path))
        zip_buffer.seek(0)
        return FileResponse(zip_buffer, as_attachment=True, filename=f'{self.kwargs["slug"]}_files.zip')
