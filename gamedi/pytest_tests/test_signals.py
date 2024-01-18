import pytest
from pytest_lazyfixture import lazy_fixture as lf

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


@pytest.mark.parametrize(
    'obj',
    [
        lf('game_obj_without_order_number_and_is_published'),
        lf('user_game_file_obj_without_order_number_and_is_published'),
        lf('admin_game_file_obj_without_order_number_and_is_published'),
    ]
)
class TestOrdersNumbersSignalsFirstObj:
    """Проверяет автоперестановку порядковых номеров при первом создании объекта."""
    def test_first_obj_without_order_number(self, obj: Game | UserGameFile | AdminGameFile):
        """Игра первая, не указан порядковый номер и статус публикации."""
        obj.save()
        assert obj.__class__.objects.first().order_number == 1  # type: ignore[union-attr]

    def test_first_published_obj_without_order_number(self, obj: Game | UserGameFile | AdminGameFile):
        """Игра первая, публикуемая, не указан порядковый номер."""
        obj.is_published = True
        obj.save()
        assert obj.__class__.objects.first().order_number == 1  # type: ignore[union-attr]

    def test_first_unpublished_obj_without_order_number(self, obj: Game | UserGameFile | AdminGameFile):
        """Игра первая, непубликуемая, не указан порядковый номер."""
        obj.is_published = False
        obj.save()
        assert obj.__class__.objects.first().order_number is None  # type: ignore[union-attr]

    def test_first_published_obj_with_wrong_order_number(self, obj: Game | UserGameFile | AdminGameFile):
        """Игра первая, публикуемая, не указан порядковый номер."""
        obj.is_published = True
        obj.order_number = 100
        obj.save()
        assert obj.__class__.objects.first().order_number == 1  # type: ignore[union-attr]


class TestOrdersNumbersSignalsDelete:
    """Проверяет автоперестановку порядковых номеров при удалении или снятии объекта с публикации."""
    @pytest.mark.parametrize('obj', [lf('game'), lf('user_game_file'), lf('admin_game_file')])
    def test_unpublish_published_obj(self, obj: Game | UserGameFile | AdminGameFile):
        """У снятого с публикации объекта нет порядкового номера."""
        obj.is_published = False
        obj.save()
        assert obj.__class__.objects.first().order_number is None  # type: ignore[union-attr]
