import pytest
from pytest_lazyfixture import lazy_fixture as lf

from tempfile import NamedTemporaryFile

from django.core.files.uploadedfile import SimpleUploadedFile

from games.models import AdminGameFile, Game, UserGameFile


@pytest.fixture
def user_game_file(game: Game, temp_img_data: dict) -> UserGameFile:
    """Фикстура, создающая и возвращающая объект пользовательского файла."""
    with NamedTemporaryFile(**temp_img_data) as file:
        return UserGameFile.objects.create(
            name='Файл для пользователя',
            file=file.name,
            game=game,
            order_number=1,
            is_published=True,
        )


@pytest.fixture
def admin_game_file(game: Game, temp_img_data: dict) -> AdminGameFile:
    """Фикстура, создающая и возвращающая объект файла админа."""
    with NamedTemporaryFile(**temp_img_data) as file:
        return AdminGameFile.objects.create(
            name='Файл для администратора',
            file=file.name,
            game=game,
            order_number=1,
            is_published=True,
        )


@pytest.fixture
def user_game_file_obj_without_order_number_and_is_published(game: Game, temp_img_data: dict) -> UserGameFile:
    """Фикстура,  создающая и возвращающая объект пользовательского файла c картинкой, не сохраняя в базе."""
    with NamedTemporaryFile(**temp_img_data) as file:
        return UserGameFile(
            name='Файл для пользователя',
            file=file.name,
            game=game,
        )


@pytest.fixture
def admin_game_file_obj_without_order_number_and_is_published(
    game: Game, temp_img_data: dict
) -> AdminGameFile:
    """Фикстура,  создающая и возвращающая объект пользовательского файла c картинкой, не сохраняя в базе."""
    with NamedTemporaryFile(**temp_img_data) as file:
        return AdminGameFile(
            name='Файл для администратора',
            file=file.name,
            game=game,
        )


@pytest.fixture
def user_game_file_with_img(game: Game, image_data: dict) -> UserGameFile:
    """Фикстура, создающая и возвращающая объект пользовательского файла c картинкой."""
    with SimpleUploadedFile(**image_data) as file:
        return UserGameFile.objects.create(
            name='Файл для пользователя',
            file=file,
            game=game,
        )


@pytest.fixture
def admin_game_file_with_img(game: Game, image_data: dict) -> AdminGameFile:
    """Фикстура, создающая и возвращающая объект файла администратора c картинкой."""
    with SimpleUploadedFile(**image_data) as file:
        return AdminGameFile.objects.create(
            name='Файл для администратора',
            file=file,
            game=game,
        )


@pytest.fixture(
    params=[
        lf('user_game_file_with_img'),
        lf('admin_game_file_with_img')
    ]
)
def file_instance(request) -> AdminGameFile | UserGameFile:
    """Фикстура с параметризацией для тестов файлов."""
    return request.param
