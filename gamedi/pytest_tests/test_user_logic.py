import pytest
from pytest_lazyfixture import lazy_fixture as lf

from http import HTTPStatus

from django.http import HttpResponse, HttpResponseRedirect
from django.test.client import Client
from django.urls import reverse

from users.models import User

pytestmark = pytest.mark.django_db


class TestUserLogic:
    def test_anonymous_can_registation(self, client: Client, registration_data: dict[str, str]):
        """Анонимный пользователь может успешно зарегистрироваться."""
        old_count_users: int = User.objects.count()
        response: HttpResponseRedirect = client.post(reverse('registration'), data=registration_data)  # type: ignore

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse('login')
        assert old_count_users < User.objects.count()

    def test_authorized_user_can_not_registation(self, user_client: Client, registration_data: dict[str, str]):
        """Автороризованный пользователь не может успешно зарегистрироваться."""
        old_count_users: int = User.objects.count()
        response: HttpResponseRedirect = user_client.post(  # type: ignore
            reverse('registration'),
            data=registration_data,
        )

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse('games:home')
        assert old_count_users == User.objects.count()

    @pytest.mark.parametrize(
            'vistor, expected_status',
            [
                (lf('owner_client'), HTTPStatus.OK),
                (lf('user_client'), HTTPStatus.FORBIDDEN),
                (lf('client'), HTTPStatus.FORBIDDEN),
            ]
    )
    def test_only_authenticated_user_can_edit_profile(self, vistor: Client, expected_status: int, owner: User):
        """Только авторизованный пользователь может менять свои данные."""
        update_user_data: dict[str, str] = {
            'username': 'owner_game',
            'email': 'owner_game@django.ru',
            'first_name': 'owner',
            'last_name': 'game',
        }
        response: HttpResponse = vistor.put(  # type: ignore
            reverse('users:update', args=(owner.username,)),
            data=update_user_data,
        )

        assert response.status_code == expected_status
