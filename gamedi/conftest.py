import pytest

from games.models import Game, Gener


@pytest.fixture
def user(django_user_model):
    """Фикстура, создающая и возвращающая первого пользователя."""
    return django_user_model.objects.create(username='first_user')


@pytest.fixture
def user_client(user, client):
    """
    Фикстура, создающая и возвращающая
    аутентифицированного первого пользователя.
    """
    client.force_login(user)
    return client


@pytest.fixture
def username(user):
    """Фикстура, возвращающая 'username' пользователя."""
    return user.username,


@pytest.fixture
def genre():
    """Фикстура, создающая и возвращающая объект жанра."""
    genre = Gener.objects.create(
        name='Жанр',
        discription='Описание',
    )
    return genre


@pytest.fixture
def game(genre):
    """Фикстура, создающая и возвращающая объект игры."""
    game = Game.objects.create(
        name='Игра',
        discription='Описание',
        slug='slug',
        genre=genre,
        min_players=8,
        max_players=8,
        price=1500,
        discount=40,
    )
    return game


@pytest.fixture
def game_slug(game):
    """Фикстура, возвращающая слаг игры."""
    return game.slug,


@pytest.fixture
def owner(django_user_model, game):
    """Фикстура, создающая и возвращающая владельца игры."""
    owner = django_user_model.objects.create(username='owner_game')
    owner.games.add(game)
    return owner


@pytest.fixture
def owner_client(owner, client):
    """
    Фикстура, создающая и возвращающая
    аутентифицированного владельца игры.
    """
    client.force_login(owner)
    return client
