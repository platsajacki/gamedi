import pytest

from games.models import Game, Gener


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username='Клиент')


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def genre():
    genre = Gener.objects.create(
        name='Жанр',
        discription='Описание',
    )
    return genre


@pytest.fixture
def game(genre):
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
    return game.slug,
