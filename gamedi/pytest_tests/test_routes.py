from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('games:home', None),
        ('login', None),
        ('registration', None),
        ('pages:about', None),
        ('pages:rules', None),
        ('games:detail', pytest.lazy_fixture('game_slug'))
    )
)
def test_pages_availability_for_anonymous_user(client, name, args):
    """Проверяет доступность страниц для анонимных пользователей."""
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, visitor, status',
    (
        (
            'users:profile',
            pytest.lazy_fixture('user_client'),
            HTTPStatus.OK
        ),
        (
            'users:profile',
            pytest.lazy_fixture('client'),
            HTTPStatus.FOUND
        ),
        (
            'users:profile',
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            'users:update',
            pytest.lazy_fixture('user_client'),
            HTTPStatus.OK
        ),
        (
            'users:update',
            pytest.lazy_fixture('client'),
            HTTPStatus.FOUND
        ),
        (
            'users:update',
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.NOT_FOUND
        ),
    )
)
def test_profile_availability_for_only_profile_owner(
    name, visitor, username, status
):
    """Проверяет доступность страниц профиля только для владельцев профиля."""
    url = reverse(name, args=username)
    response = visitor.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'name, visitor, status',
    (
        (
            'users:game',
            pytest.lazy_fixture('owner_client'),
            HTTPStatus.OK
        ),
        (
            'users:game',
            pytest.lazy_fixture('user_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            'users:game',
            pytest.lazy_fixture('client'),
            HTTPStatus.FOUND
        ),
    )
)
def test_game_availability_for_only_game_owner(
        name, visitor, owner, game_slug, status
):
    """
    Проверяет доступность страницы игры в профиле
    только для владельцев игры.
    """
    url = reverse(name, args=(owner.username, game_slug[0]))
    response = visitor.get(url)
    assert response.status_code == status
