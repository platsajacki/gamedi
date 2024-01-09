import pytest
from pytest_lazyfixture import lazy_fixture as lf

from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from users.models import User

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name, args',
    (
        ('games:home', None),
        ('login', None),
        ('registration', None),
        ('pages:about', None),
        ('pages:rules', None),
        ('games:detail', lf('game_slug'))
    )
)
def test_pages_availability_for_anonymous_user(client: Client, name: str, args: tuple[str]):
    """Проверяет доступность страниц для анонимных пользователей."""
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, visitor, status',
    (
        ('users:profile', lf('user_client'), HTTPStatus.OK),
        ('users:profile', lf('client'), HTTPStatus.FORBIDDEN),
        ('users:profile', lf('admin_client'), HTTPStatus.FORBIDDEN),
        ('users:update', lf('user_client'), HTTPStatus.OK),
        ('users:update', lf('client'), HTTPStatus.FORBIDDEN),
        ('users:update', lf('admin_client'), HTTPStatus.FORBIDDEN),
    )
)
def test_profile_availability_for_only_profile_owner(name: str, visitor: Client, username: tuple[str], status: int):
    """Проверяет доступность страниц профиля только для владельцев профиля."""
    url = reverse(name, args=username)
    response = visitor.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'visitor, status',
    (
        (lf('owner_client'), HTTPStatus.OK),
        (lf('user_client'), HTTPStatus.FORBIDDEN),
        (lf('client'), HTTPStatus.FORBIDDEN),
    )
)
def test_game_availability_for_only_game_owner(visitor: Client, owner: User, game_slug: tuple[str], status: int):
    """Проверяет доступность страницы игры в профиле только для владельцев игры."""
    url = reverse('users:game', args=(owner.username, game_slug[0]))
    response = visitor.get(url)
    assert response.status_code == status
