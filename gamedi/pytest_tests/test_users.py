import pytest
from pytest_lazyfixture import lazy_fixture as lf

from http import HTTPStatus

from django.http import HttpResponse, HttpResponseRedirect
from django.test import Client
from django.urls import reverse

from games.models import Game
from users.models import User

pytestmark = pytest.mark.django_db


class TestUserRegistrationLogic:
    """Проверяет корректность регистрации и авторизации."""
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
            'email': 'owner_game@django.ru',
            'first_name': 'owner',
            'last_name': 'game',
        }
        response: HttpResponse = vistor.put(  # type: ignore
            reverse('users:update', args=(owner.username,)),
            data=update_user_data,
        )

        assert response.status_code == expected_status


@pytest.mark.usefixtures('five_games')
class TestUserProfileContent:
    """Проверяет содержимое личного кабинета пользователя."""
    def test_games_presence_in_users_profile(self, user: User, username: tuple[str], user_client: Client):
        """Наличие приобретенных игр в личном кабинете."""
        user.games.add(*Game.objects.all())
        user.save()
        response = user_client.get(reverse('users:profile', args=username))
        assert response.status_code == 200
        assert response.context['user'] == user
        for game_name in user.games.values_list('name', flat=True):
            assert game_name in response.content.decode()

    def test_no_games_for_other_user_profile(self, user: User, username: tuple[str], user_client: Client, owner: User):
        """В личном кабинете нет игр других пользователей."""
        owner.games.add(*Game.objects.all())
        owner.save()
        response = user_client.get(reverse('users:profile', args=username))
        assert response.status_code == 200
        assert response.context['user'] == user
        for game_name in owner.games.values_list('name', flat=True):
            assert game_name not in response.content.decode()
