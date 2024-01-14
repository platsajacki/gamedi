from django.contrib.auth.models import UserManager
from django.db.models import QuerySet


class CustomUserManager(UserManager):
    """Кастомный менеджер модели пользователя."""
    def related_games(self) -> QuerySet:
        """
        Возвращает QuerySet,
        предварительно загружающий связанные игры пользователя
        вместе с файлами и жанром.
        """
        return (
            self
            .prefetch_related(
                'games__users_files',
                'games__admin_files',
                'games__genre',
            )
            .order_by('games__users_files__order_number', )
        )
