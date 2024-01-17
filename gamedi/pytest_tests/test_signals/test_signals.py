import pytest

from os import path, remove

from django.core.files.uploadedfile import SimpleUploadedFile

from games.models import AdminGameFile, Game, UserGameFile

pytestmark = pytest.mark.django_db


class TestFileSignals:
    def test_signal_delete_gamefile_game(self, game_with_img: Game):
        """Проверяет, что сигнал удаления файла игры также удаляет фактический файл."""
        assert path.exists(path_img := game_with_img.cover.path)
        game_with_img.delete()
        assert not path.exists(path_img)

    def test_signal_delete_gamefile_file_models(self, file_instance: AdminGameFile | UserGameFile):
        """Проверяет, что сигнал удаления экземпляра модели файла также удаляет фактический файл."""
        assert path.exists(path_img := file_instance.file.path)
        file_instance.delete()
        assert not path.exists(path_img)

    def test_signal_update_gamefile_game(self, game_with_img: Game, image_with_another_name: SimpleUploadedFile):
        """Проверяет, что сигнал обновления файла игры также обновляет фактический файл."""
        assert path.exists(path_img := game_with_img.cover.path)
        game_with_img.cover = image_with_another_name
        game_with_img.save()

        assert not path.exists(path_img)
        game_with_img.cover == image_with_another_name
        assert path.exists(game_with_img.cover.path)  # type: ignore[attr-defined]
        remove(game_with_img.cover.path)  # type: ignore[attr-defined]
        remove(game_with_img.hover_cover.path)

    def test_signal_update_gamefile_file_models(
        self, file_instance: AdminGameFile | UserGameFile, image_with_another_name: SimpleUploadedFile
    ):
        """Проверяет, что сигнал обновления экземпляра модели файла также обновляет фактический файл."""
        assert path.exists((old_file := file_instance.file).path)
        file_instance.file = image_with_another_name
        file_instance.save()

        assert path.exists(file_instance.file.path)  # type: ignore[attr-defined]
        file_instance.file != old_file
        file_instance.file == image_with_another_name
        remove(file_instance.file.path)  # type: ignore[attr-defined]
