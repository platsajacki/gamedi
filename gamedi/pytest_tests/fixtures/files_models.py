import pytest
from pytest_lazyfixture import lazy_fixture as lf

from copy import deepcopy
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
def five_user_files(
    user_game_file_obj_without_order_number_and_is_published: UserGameFile, temp_img_data: dict
) -> list[UserGameFile]:
    """Фикстура, создающая и возвращающая 5 объектов файлов пользователя."""
    user_files = []
    for i in range(1, 6):
        with NamedTemporaryFile(**temp_img_data) as file:
            user_file = deepcopy(user_game_file_obj_without_order_number_and_is_published)
            user_file.order_number = i
            user_file.is_published = True
            user_file.name = f'Файл для пользователя_{i}'
            user_file.file = file.name
            user_files.append(user_file)
    return UserGameFile.objects.bulk_create(user_files)


@pytest.fixture
def admin_game_file_obj_without_order_number_and_is_published(game: Game, temp_img_data: dict) -> AdminGameFile:
    """Фикстура,  создающая и возвращающая объект пользовательского файла c картинкой, не сохраняя в базе."""
    with NamedTemporaryFile(**temp_img_data) as file:
        return AdminGameFile(
            name='Файл для администратора без ПП и публикации',
            file=file.name,
            game=game,
        )


@pytest.fixture
def five_admin_files(
    admin_game_file_obj_without_order_number_and_is_published: AdminGameFile, temp_img_data: dict
) -> list[AdminGameFile]:
    """Фикстура, создающая и возвращающая 5 объектов файлов администратора."""
    admin_files = []
    for i in range(1, 6):
        with NamedTemporaryFile(**temp_img_data) as file:
            admin_file = deepcopy(admin_game_file_obj_without_order_number_and_is_published)
            admin_file.order_number = i
            admin_file.is_published = True
            admin_file.name = f'Файл для администратора_{i}'
            admin_file.file = file.name
            admin_files.append(admin_file)
    return AdminGameFile.objects.bulk_create(admin_files)


@pytest.fixture
def user_game_file_with_img(game: Game, image_data: dict) -> UserGameFile:
    """Фикстура, создающая и возвращающая объект пользовательского файла c картинкой."""
    with SimpleUploadedFile(**image_data) as file:
        return UserGameFile.objects.create(
            name='Файл для пользователя без ПП и публикации',
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
