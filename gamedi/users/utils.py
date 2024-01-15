from django.conf import settings
from django.core.mail import EmailMessage


def send_role_and_file_email(username: str, email: str, role: str, game_name: str, file_path: str) -> None:
    """Письмо с ролью и файлами игры."""
    subject: str = f'Приглашение от {username}. GameDi.'
    body: str = f'Ты - {role} в игре {game_name}.'
    msg: EmailMessage = EmailMessage(subject=subject, body=body, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
    msg.attach_file(file_path)
    msg.send()
