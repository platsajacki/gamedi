import pytest

from django.test import Client

from games.models import Game
from users.models import User


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
