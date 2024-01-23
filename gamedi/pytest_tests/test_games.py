import pytest
from pytest_lazyfixture import lazy_fixture as lf

from http import HTTPStatus
from unittest.mock import patch

from django.test.client import Client
from django.urls import reverse

from games.forms import RoleMessageFormSet
from users.models import User

pytestmark = pytest.mark.django_db


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
    """Проверяет доступность страницы игры в профиле. Только для владельцев игры."""
    assert visitor.get(reverse(name, args=(owner.username, game_slug[0]))).status_code == status


class TestGameProfileDetailView:
    """Тестирует представление игры в профиле пользователя."""
    def test_game_profile_detail_view_get_context_data(self, game_slug: tuple[str], owner: User, owner_client: Client):
        """Тест метода get_context_data в GameProfileDetailView."""
        context = owner_client.get(reverse('games:game', args=(owner.username,) + game_slug)).context
        assert 'formset' in context
        assert isinstance(context['formset'], RoleMessageFormSet)

    def test_game_profile_detail_view_post_error_send_message(
            self, game_slug: tuple[str], owner: User, owner_client: Client, formset_data: dict[str, str]
    ):
        """Если сообщения не отправлены, в ответе должно быть 'exception'."""
        response = owner_client.post(reverse('games:game', args=(owner.username,) + game_slug), data=formset_data)
        assert 'exception' in response.context

    @pytest.mark.usefixtures('five_user_files')
    def test_game_profile_detail_view_post_valide_formset(
            self, game_slug: tuple[str], owner: User, owner_client: Client, formset_data: dict[str, str]
    ):
        """При валидном FormSet, направляются письма."""
        with patch('users.utils.get_role_and_file_email') as mock_send_message:
            response = owner_client.post(reverse('games:game', args=(owner.username,) + game_slug), data=formset_data)
            assert response.status_code == HTTPStatus.OK
            assert mock_send_message.call_count == int(formset_data['form-INITIAL_FORMS'])

    @pytest.mark.usefixtures('five_user_files')
    def test_game_profile_detail_view_post_invalide_formset(
            self, game_slug: tuple[str], owner: User, owner_client: Client, formset_data: dict[str, str]
    ):
        """При невалидном FormSet, письма не отравляются, FormSet направляется обратно."""
        formset_data['form-1-email'] = formset_data['form-0-email']
        with patch('users.utils.get_role_and_file_email') as mock_send_message:
            response = owner_client.post(reverse('games:game', args=(owner.username,) + game_slug), data=formset_data)
            assert response.status_code == HTTPStatus.OK
            assert mock_send_message.call_count == 0
            assert 'formset' in response.context
            for i in range(int(formset_data['form-INITIAL_FORMS'])):
                assert response.context['formset'].data[f'form-{i}-email'] == formset_data[f'form-{i}-email']
                assert response.context['formset'].data[f'form-{i}-role'] == formset_data[f'form-{i}-role']
