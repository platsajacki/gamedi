import pytest

from django.test.client import Client

pytestmark = pytest.mark.django_db


class TestUserLogic:
    def test_anonymous_can_registation(client: Client):
        ...
