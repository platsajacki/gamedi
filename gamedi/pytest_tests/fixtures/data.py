import pytest

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from games.models import AdminGameFile, Game, UserGameFile


@pytest.fixture
def registration_data() -> dict[str, str]:
    """Возвращает словарь с регистрационными данными."""
    return {
        'username': 'test',
        'email': 'test@test.ru',
        'password1': 'first_test',
        'password2': 'first_test',
    }


@pytest.fixture
def temp_img_data() -> dict:
    return {
        'prefix': 'file',
        'suffix': '.png',
        'dir': settings.MEDIA_ROOT,
    }


@pytest.fixture
def image_data() -> dict:
    """Фикстура, возвращающая словарь с данными изображения."""
    return {
        'name': 'test_image.jpg',
        'content': open(f'{settings.BASE_DIR}/pytest_tests/image.png', 'rb').read(),
        'content_type': 'image/png',
    }


@pytest.fixture
def image_with_another_name(image_data: dict) -> SimpleUploadedFile:
    """Фикстура, возвращающая словарь с данными изображения."""
    image_data.update(name='test_image2.jpg')
    return SimpleUploadedFile(**image_data)


@pytest.fixture(params=[Game, AdminGameFile, UserGameFile])
def order_number_models(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture
def objs_without_order_number_and_published(
    game_obj_without_order_number_and_is_published: Game,
    admin_game_file_obj_without_order_number_and_is_published: AdminGameFile,
    user_game_file_obj_without_order_number_and_is_published: UserGameFile,
) -> dict:
    "Словарь неопубликованных объектов без порядкового номера, без записи в базу."
    return {
        Game: game_obj_without_order_number_and_is_published,
        AdminGameFile: admin_game_file_obj_without_order_number_and_is_published,
        UserGameFile: user_game_file_obj_without_order_number_and_is_published,
    }


@pytest.fixture
def formset_data() -> dict:
    """Данные для заполнения FormSet."""
    return {
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '2',
        'form-MAX_NUM_FORMS': '',
        'form-0-role': 'Файл для пользователя_1',
        'form-0-email': 'email1@example.com',
        'form-1-role': 'Файл для пользователя_2',
        'form-1-email': 'email2@example.com',
    }
