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
