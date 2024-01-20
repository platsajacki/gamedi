import pytest

from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import reverse

from games.forms import RoleMessageFormSet
from games.models import Game
from users.constants import EMAIL_INVITATION_BODY, EMAIL_INVITATION_SUBJECT
from users.models import User
from users.utils import define_name, send_role_and_file_email

pytestmark = pytest.mark.django_db


def test_define_name(user: User):
    """Проверяет корректность имени в зависимости от статуса аутентификации и наличия данных у пользователя."""
    assert define_name(AnonymousUser()) == 'Безымянный детектив'
    assert define_name(user) == user.username
    user.first_name = 'first'
    assert define_name(user) == user.first_name
    user.last_name = 'last'
    assert define_name(user) == user.get_full_name()


@pytest.mark.usefixtures('five_user_files')
class TestSendRoleAndFileEmail:
    """Проверяет, что функция send_role_and_file_email корректно отправляет электронные письма"""
    def test_send_role_and_file_email_all_emails(
        self, mailoutbox: list, owner: User, game: Game, game_slug: tuple[str], formset_data: dict
    ):
        """Корректно отправляет электронные письма со всеми email."""
        with patch('django.core.mail.message.EmailMessage.attach_file') as mock_attach_file:
            request: HttpRequest = RequestFactory().post(reverse('games:game', args=(owner.username, game_slug[0])))
            request.user = owner
            send_role_and_file_email(
                request=request, formset=RoleMessageFormSet(formset_data), context={'object': game}
            )
            assert mock_attach_file.call_count == (INITIAL_FORMS := int(formset_data['form-INITIAL_FORMS']))
            assert len(mailoutbox) == INITIAL_FORMS
            for i, mail in enumerate(mailoutbox):
                assert mail.to[0] == formset_data[f'form-{i}-email']
                assert mail.subject == EMAIL_INVITATION_SUBJECT.format(username=define_name(owner))
                assert mail.body == EMAIL_INVITATION_BODY.format(
                    role=formset_data[f'form-{i}-role'], game_name=game.name
                )

    def test_send_role_and_file_email_empty_email(
        self, mailoutbox: list, owner: User, game: Game, game_slug: tuple[str], formset_data: dict
    ):
        """Корректно отправляет электронные письма, где указан email, с пустым email не отправляет."""
        with patch('django.core.mail.message.EmailMessage.attach_file') as mock_attach_file:
            formset_data['form-1-email'] = ''
            request: HttpRequest = RequestFactory().post(reverse('games:game', args=(owner.username, game_slug[0])))
            request.user = owner
            send_role_and_file_email(
                request=request, formset=RoleMessageFormSet(formset_data), context={'object': game}
            )
            assert mock_attach_file.call_count == (INITIAL_FORMS := int(formset_data['form-INITIAL_FORMS']) - 1)
            assert len(mailoutbox) == INITIAL_FORMS
            for i, mail in enumerate(mailoutbox):
                assert mail.to[0] == formset_data[f'form-{i}-email']
                assert mail.subject == EMAIL_INVITATION_SUBJECT.format(username=define_name(owner))
                assert mail.body == EMAIL_INVITATION_BODY.format(
                    role=formset_data[f'form-{i}-role'], game_name=game.name
                )
