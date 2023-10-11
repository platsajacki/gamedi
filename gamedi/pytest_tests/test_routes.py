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
        ('games:detail', pytest.lazy_fixture('game_slug'))
    )
)
def test_pages_availability_for_anonymous_user(client, name, args):
    print(args)
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
            HTTPStatus.FORBIDDEN
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
            HTTPStatus.FORBIDDEN
        ),
    )
)
def test_profile_availability_for_only_profile_owne(
    name, visitor, username, status
):
    url = reverse(name, args=username)
    response = visitor.get(url)
    assert response.status_code == status
