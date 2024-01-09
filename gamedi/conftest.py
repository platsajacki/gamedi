import pytest

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from games.models import Game, Genre
from users.models import User

IMAGEFILE: SimpleUploadedFile = SimpleUploadedFile(
    name='test_image.jpg',
    content=open(f'{settings.BASE_DIR}/pytest_tests/image.png', 'rb').read(),
    content_type='image/png',
)


@pytest.fixture
def user(django_user_model: User) -> User:
    """Фикстура, создающая и возвращающая первого пользователя."""
    return django_user_model.objects.create(username='first_user', email='first_user@django.ru')


@pytest.fixture
def user_client(user: User, client: Client) -> Client:
    """Фикстура, создающая и возвращающая аутентифицированного первого пользователя."""
    client.force_login(user)
    return client


@pytest.fixture
def username(user: User) -> tuple[str]:
    """Фикстура, возвращающая 'username' пользователя."""
    return user.username,


@pytest.fixture
def genre() -> Genre:
    """Фикстура, создающая и возвращающая объект жанра."""
    return Genre.objects.create(name='Жанр', description='Описание')


@pytest.fixture
def game(genre: Genre) -> Game:
    """Фикстура, создающая и возвращающая объект игры."""
    return Game.objects.create(
        name='Игра',
        description='Описание',
        slug='slug',
        genre=genre,
        min_players=8,
        max_players=8,
        price=1500,
        discount=40,
        time=4,
        age_restriction=5,
        cover=IMAGEFILE,
        hover_cover=IMAGEFILE,
    )


@pytest.fixture
def game_slug(game) -> tuple[str]:
    """Фикстура, возвращающая слаг игры."""
    return game.slug,


@pytest.fixture
def owner(django_user_model: User, game: Game) -> User:
    """Фикстура, создающая и возвращающая владельца игры."""
    owner = django_user_model.objects.create(username='owner_game', email='owner_game@django.ru')
    owner.games.add(game)
    return owner


@pytest.fixture
def owner_client(owner: User, client: Client) -> Client:
    """Фикстура, создающая и возвращающая аутентифицированного владельца игры."""
    client.force_login(owner)
    return client
