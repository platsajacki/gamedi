import pytest
from pytest_lazyfixture import lazy_fixture as lf

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from games.models import AdminGameFile, Game, Genre, UserGameFile


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


@pytest.fixture
def game_with_img(genre: Genre, image_data: dict) -> Game:
    """Фикстура, создающая и возвращающая объект игры c картинкой."""
    with SimpleUploadedFile(**image_data) as file:
        return Game.objects.create(
            name='Игра с картинкой',
            description='Описание',
            slug='slug_with_img',
            genre=genre,
            min_players=8,
            max_players=8,
            price=1500,
            discount=40,
            order_number=1,
            time=4,
            age_restriction=5,
            cover=file,
            hover_cover=file,
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
