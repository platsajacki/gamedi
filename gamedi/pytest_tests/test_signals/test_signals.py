import pytest

from os import path

# from django.core.files.uploadedfile import SimpleUploadedFile

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

    # def test_signal_update_gamefile_game(self, game_with_img: Game, image_with_another_name: SimpleUploadedFile):
    #     """Проверяет, что сигнал обновления файла игры также обновляет фактический файл."""
    #     ...

    # def test_signal_update_gamefile_file_models(self, file_instance: AdminGameFile | UserGameFile):
    #     """Проверяет, что сигнал обновления экземпляра модели файла также обновляет фактический файл."""
    #     ...
