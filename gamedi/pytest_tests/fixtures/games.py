import pytest

from tempfile import NamedTemporaryFile

from django.core.files.uploadedfile import SimpleUploadedFile

from games.models import Game, Genre


@pytest.fixture
def genre() -> Genre:
    """Фикстура, создающая и возвращающая объект жанра."""
    return Genre.objects.create(name='Жанр', description='Описание')


@pytest.fixture
def game(genre: Genre, temp_img_data: dict) -> Game:
    """Фикстура, создающая и возвращающая объект игры."""
    with NamedTemporaryFile(**temp_img_data) as file:
        return Game.objects.create(
            name='Игра',
            description='Описание',
            slug='slug',
            genre=genre,
            min_players=8,
            max_players=8,
            order_number=1,
            is_published=True,
            price=1500,
            discount=40,
            time=4,
            age_restriction=5,
            cover=file.name,
            hover_cover=file.name,
        )


@pytest.fixture
def game_slug(game) -> tuple[str]:
    """Фикстура, возвращающая слаг игры."""
    return game.slug,


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
            is_published=True,
            time=4,
            age_restriction=5,
            cover=file,
            hover_cover=file,
        )


@pytest.fixture
def game_obj_without_order_number_and_is_published(genre: Genre, temp_img_data: dict) -> Game:
    """Фикстура, создающая и возвращающая объект игры c картинкой, не сохраняя в базе."""
    with NamedTemporaryFile(**temp_img_data) as file:
        return Game(
            name='Игра без ПП и статуса публикации',
            description='Описание',
            slug='without_order_number',
            genre=genre,
            min_players=8,
            max_players=8,
            price=1500,
            discount=40,
            time=4,
            age_restriction=5,
            cover=file.name,
            hover_cover=file.name,
        )
