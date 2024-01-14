from django import apps
from django.db.models import Manager, Prefetch, QuerySet


class GameQuerySet(QuerySet):
    """QuerySet для работы с моделью Game."""
    def related_tables(self) -> 'GameQuerySet':
        """
        Отимизирует запрос, присоединяя таблицы.
        """
        return (
            self.select_related('genre')
            .prefetch_related('users')
            .prefetch_related(
                Prefetch(
                    'users_files',
                    queryset=(apps.apps.get_model('games', 'UserGameFile').objects.published())
                )
            )
            .prefetch_related(
                Prefetch(
                    'admin_files',
                    queryset=(apps.apps.get_model('games', 'AdminGameFile').objects.published())
                )
            )
        )

    def published(self) -> 'GameQuerySet':
        """
        Возвращает QuerySet, фильтрующий опубликованные игры,
        принадлежащие опубликованным жанрам.
        """
        return self.filter(is_published=True, genre__is_published=True)


class GameManager(Manager):
    """Manager для работы с моделью Game."""
    def get_queryset(self) -> GameQuerySet:
        """
        Возвращает QuerySet для модели Game
        с выбранными связанными таблицами и фильтрацией для опубликованных игр.
        """
        return GameQuerySet(self.model).related_tables().published()
