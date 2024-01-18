import pytest

from tempfile import NamedTemporaryFile

from django.conf import settings
from django.test import Client

from games.models import AdminGameFile, Game, Genre, UserGameFile
from users.models import User

pytest_plugins = ['pytest_tests.test_signals.fixtures']


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
def registration_data() -> dict[str, str]:
    """Возвращает словарь с регистрационными данными."""
    return {
        'username': 'test',
        'email': 'test@test.ru',
        'password1': 'first_test',
        'password2': 'first_test',
    }


@pytest.fixture
def username(user: User) -> tuple[str]:
    """Фикстура, возвращающая 'username' пользователя."""
    return user.username,


@pytest.fixture
def genre() -> Genre:
    """Фикстура, создающая и возвращающая объект жанра."""
    return Genre.objects.create(name='Жанр', description='Описание')


@pytest.fixture
def temp_img_data() -> dict:
    return {
        'prefix': 'file',
        'suffix': '.png',
        'dir': settings.MEDIA_ROOT,
    }


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
