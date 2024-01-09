import pytest

from http import HTTPStatus

from django.http import HttpResponse
from django.test.client import Client
from django.urls import reverse

from users.models import User

pytestmark = pytest.mark.django_db


class TestUserLogic:
    """Набор тестов для проверки логики пользователей."""
    def test_anonymous_can_registation(self, client: Client, registration_data: dict[str, str]):
        """Тест проверяет, может ли анонимный пользователь успешно зарегистрироваться."""
        old_count_users: int = User.objects.count()
        response: HttpResponse = client.post(reverse('registration'), data=registration_data)  # type: ignore

        assert response.status_code == HTTPStatus.FOUND
        assert old_count_users < User.objects.count()
