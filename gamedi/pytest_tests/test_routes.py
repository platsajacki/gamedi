import pytest
from pytest_lazyfixture import lazy_fixture as lf

from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from users.models import User

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name, args',
    [
        ('games:home', None),
        ('login', None),
        ('registration', None),
        ('pages:about', None),
        ('pages:rules', None),
        ('games:detail', lf('game_slug'))
    ]
)
def test_pages_availability_for_anonymous_user(client: Client, name: str, args: tuple[str]):
    """Проверяет доступность страниц для анонимных пользователей."""
    assert client.get(reverse(name, args=args)).status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, visitor, status',
    [
        ('users:profile', lf('user_client'), HTTPStatus.OK),
        ('users:profile', lf('client'), HTTPStatus.FORBIDDEN),
        ('users:profile', lf('admin_client'), HTTPStatus.FORBIDDEN),
        ('users:update', lf('user_client'), HTTPStatus.OK),
        ('users:update', lf('client'), HTTPStatus.FORBIDDEN),
        ('users:update', lf('admin_client'), HTTPStatus.FORBIDDEN),
    ]
)
def test_profile_availability_for_only_profile_owner(name: str, visitor: Client, username: tuple[str], status: int):
    """Проверяет доступность страниц профиля только для владельцев профиля."""
    assert visitor.get(reverse(name, args=username)).status_code == status


@pytest.mark.parametrize(
    'name, visitor, status',
    [
        ('games:game', lf('owner_client'), HTTPStatus.OK),
        ('games:game', lf('user_client'), HTTPStatus.FORBIDDEN),
        ('games:game', lf('client'), HTTPStatus.FORBIDDEN),
        ('games:download_files', lf('owner_client'), HTTPStatus.OK),
        ('games:download_files', lf('user_client'), HTTPStatus.FORBIDDEN),
        ('games:download_files', lf('client'), HTTPStatus.FORBIDDEN),
    ]
)
def test_game_availability_for_only_game_owner(
    name: str, visitor: Client, owner: User, game_slug: tuple[str], status: int
):
    """Проверяет доступность страницы игры в профиле только для владельцев игры."""
    assert visitor.get(reverse(name, args=(owner.username, game_slug[0]))).status_code == status
