import pytest
from pytest_lazyfixture import lazy_fixture as lf

from os import path, remove

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import QuerySet

from games.models import AdminGameFile, Game, UserGameFile

pytestmark = pytest.mark.django_db


class TestFileSignals:
    def test_signal_delete_gamefile_game(self, game_with_img: Game):
        """Проверяет, что сигнал удаления файла игры, также удаляет фактический файл."""
        assert path.exists(path_img := game_with_img.cover.path)
        game_with_img.delete()
        assert not path.exists(path_img)

    def test_signal_delete_gamefile_file_models(self, file_instance: AdminGameFile | UserGameFile):
        """Проверяет, что сигнал удаления экземпляра модели файла, также удаляет фактический файл."""
        assert path.exists(path_img := file_instance.file.path)
        file_instance.delete()
        assert not path.exists(path_img)

    def test_signal_update_gamefile_game(self, game_with_img: Game, image_with_another_name: SimpleUploadedFile):
        """Проверяет, что сигнал обновления файла игры, также обновляет фактический файл."""
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
        """Проверяет, что сигнал обновления экземпляра модели файла, также обновляет фактический файл."""
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


@pytest.mark.parametrize('obj', [lf('game'), lf('user_game_file'), lf('admin_game_file')])
def test_unpublish_published_obj(obj: Game | UserGameFile | AdminGameFile):
    """У снятого с публикации объекта нет порядкового номера."""
    assert obj.is_published
    obj.is_published = False
    obj.save()
    assert obj.__class__.objects.first().order_number is None  # type: ignore[union-attr]


@pytest.mark.usefixtures('five_games', 'five_user_files', 'five_admin_files')
class TestOrdersNumbersSignalsAdd:
    """Проверяет автоперестановку порядковых номеров при создании или публикации объекта."""
    def test_insert_obj_at_beginning(
        self, order_number_models: Game | UserGameFile | AdminGameFile, objs_without_order_number_and_published: dict
    ):
        """Публикуемый объект добавляется в начало списка, все порядковые номера должны увеличиться на 1."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        obj: Game | UserGameFile | AdminGameFile = objs_without_order_number_and_published[order_number_models]
        obj.is_published = True
        obj.order_number = 1
        obj.save()
        assert queryset[obj.order_number - 1] == obj
        for i in range(1, len(queryset)):
            assert queryset[i - 1].order_number == i

    def test_insert_obj_at_middle(
        self, order_number_models: Game | UserGameFile | AdminGameFile, objs_without_order_number_and_published: dict
    ):
        """Публикуемый объект добавляется в середину списка, все порядковые номера после должны увеличиться на 1."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        obj: Game | UserGameFile | AdminGameFile = objs_without_order_number_and_published[order_number_models]
        obj.is_published = True
        obj.order_number = 3
        obj.save()
        assert queryset[obj.order_number - 1] == obj
        for i in range(1, len(queryset)):
            assert queryset[i - 1].order_number == i

    def test_insert_obj_at_end(
        self, order_number_models: Game | UserGameFile | AdminGameFile, objs_without_order_number_and_published: dict
    ):
        """Публикуемый объект добавляется в конец списка, порядковые номера не меняются."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        obj: Game | UserGameFile | AdminGameFile = objs_without_order_number_and_published[order_number_models]
        obj.is_published = True
        obj.order_number = len(queryset) + 1
        obj.save()
        queryset = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        length = len(queryset)
        assert queryset[length - 1] == obj
        for i in range(1, length):
            assert queryset[i - 1].order_number == i

    def test_insert_obj_further_at_end(
        self, order_number_models: Game | UserGameFile | AdminGameFile, objs_without_order_number_and_published: dict
    ):
        """Публикуемый объект добавляется дальше, чем len + 1, порядковый номер дложен быть len + 1."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        obj: Game | UserGameFile | AdminGameFile = objs_without_order_number_and_published[order_number_models]
        obj.is_published = True
        obj.order_number = len(queryset) + 100
        obj.save()
        queryset = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        length = len(queryset)
        assert queryset[length - 1] == obj
        for i in range(1, length):
            assert queryset[i - 1].order_number == i


@pytest.mark.usefixtures('five_games', 'five_user_files', 'five_admin_files')
class TestOrdersNumbersSignalsDelete:
    """Проверяет автоперестановку порядковых номеров при удалении или снятии объекта с публикации."""
    def test_delete_obj_from_beginning(self, order_number_models: Game | UserGameFile | AdminGameFile):
        """Удаляется из начала списка, все порядковые номера должны уменьшиться на 1."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        queryset[0].delete()
        for i in range(1, len(queryset)):
            assert queryset[i - 1].order_number == i

    def test_delete_obj_from_middle(self, order_number_models: Game | UserGameFile | AdminGameFile):
        """Удаляется из середины списка, порядковые номера после должны уменьшиться на 1."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        queryset[3].delete()
        for i in range(1, len(queryset)):
            assert queryset[i - 1].order_number == i

    def test_delete_obj_from_end(self, order_number_models: Game | UserGameFile | AdminGameFile):
        """Удаляется из конца списка, порядковые номера не меняются."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')   # type: ignore[misc]
        queryset[len(queryset) - 1].delete()
        for i in range(1, len(queryset)):
            assert queryset[i - 1].order_number == i

    def test_unpublish_obj_from_beginning(self, order_number_models: Game | UserGameFile | AdminGameFile):
        """Снимается с публикации из начала списка, все порядковые номера должны уменьшиться на 1."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        queryset.filter(order_number=queryset[0].order_number).update(is_published=False)
        queryset[0].save()
        for i in range(1, len(queryset)):
            assert queryset[i - 1].order_number == i

    def test_unpublish_obj_from_middle(self, order_number_models: Game | UserGameFile | AdminGameFile):
        """Снимается с публикации из середины списка, порядковые номера после должны уменьшиться на 1."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')  # type: ignore[misc]
        queryset.filter(order_number=queryset[3].order_number).update(is_published=False)
        queryset[3].save()
        for i in range(1, len(queryset)):
            assert queryset[i - 1].order_number == i

    def test_unpublish_obj_from_end(self, order_number_models: Game | UserGameFile | AdminGameFile):
        """Снимается с публикации из конца списка, порядковые номера не меняются."""
        queryset: QuerySet = order_number_models.objects.order_by('order_number')   # type: ignore[misc]
        queryset[len(queryset) - 1].delete()
        for i in range(1, len(queryset)):
            assert queryset[i - 1].order_number == i
