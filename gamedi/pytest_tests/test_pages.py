import pytest

from django.test import Client
from django.urls import reverse


@pytest.mark.parametrize(
    'url, tamplate_name',
    [
        ('pages:about', 'pages/about.html'),
        ('pages:rules', 'pages/rules.html'),
    ]
)
def test_pages(client: Client, url: str, tamplate_name: str):
    """Проверяет шаблоны."""
    assert tamplate_name in [template.name for template in client.get(reverse(url)).templates]
