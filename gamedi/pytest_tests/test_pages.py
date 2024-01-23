import pytest
from pytest_lazyfixture import lazy_fixture as lf

from http import HTTPStatus

from django.test import Client
from django.urls import reverse

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
    'url, tamplate_name',
    [
        ('pages:about', 'pages/about.html'),
        ('pages:rules', 'pages/rules.html'),
    ]
)
def test_pages_tamplates(client: Client, url: str, tamplate_name: str):
    """Проверяет шаблоны."""
    assert tamplate_name in [template.name for template in client.get(reverse(url)).templates]
