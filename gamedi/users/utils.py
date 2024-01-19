from typing import Any, Mapping

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.mail import EmailMessage, get_connection
from django.forms import BaseFormSet
from django.http import HttpRequest

from users.constants import EMAIL_INVITATION_BODY, EMAIL_INVITATION_SUBJECT
from users.models import User


def define_name(user: User | AnonymousUser) -> str:
    """Возвращает имя пользователя в зависимости от его статуса аутентификации и полноты данных."""
    if user.is_anonymous:
        return 'Безымянный детектив'
    if user.first_name:
        if user.last_name:
            return user.get_full_name()
        return user.first_name
    return user.username


def get_role_and_file_email(username: str, email: str, role: str, game_name: str, file_path: str) -> EmailMessage:
    """Создает объект EmailMessage с информацией о роли и прикрепленным файлом игры.."""
    subject: str = EMAIL_INVITATION_SUBJECT.format(username=username)
    body: str = EMAIL_INVITATION_BODY.format(role=role, game_name=game_name)
    msg: EmailMessage = EmailMessage(subject=subject, body=body, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
    msg.attach_file(file_path)
    return msg


def send_role_and_file_email(request: HttpRequest, formset: BaseFormSet, context: dict[str, Any]) -> None:
    """Отправляет письма с информацией о роли и прикрепленным файлом игры для каждой формы в FormSet."""
    username: str = define_name(request.user)
    formset_data: Mapping[str, Any] = formset.data
    emails_to_send: list[EmailMessage] = []
    for i in range(int(formset_data.get('form-INITIAL_FORMS', 0))):
        role: str = formset_data.get(f'form-{i}-role', '')
        email_message: EmailMessage = get_role_and_file_email(
            username=username,
            email=formset_data.get(f'form-{i}-email', ''),
            role=role,
            game_name=context['object'].name,
            file_path=context['object'].users_files.get(name=role).file.path,
        )
        emails_to_send.append(email_message)
    with get_connection() as connection:
        connection.send_messages(emails_to_send)
