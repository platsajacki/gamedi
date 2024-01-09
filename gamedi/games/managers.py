from django.db.models import QuerySet, Manager


class GameQuerySet(QuerySet):
    """QuerySet для работы с моделью Game."""
    def related_tables(self) -> 'GameQuerySet':
        """
        Отимизирует запрос, присоединяя таблицы.
        """
        return self.select_related('genre')

    def published(self) -> 'GameQuerySet':
        """
        Возвращает QuerySet, фильтрующий опубликованные игры,
        принадлежащие опубликованным жанрам.
        """
        return self.filter(
            is_published=True,
            genre__is_published=True
        )


class GameManager(Manager):
    """Manager для работы с моделью Game."""
    def get_queryset(self) -> GameQuerySet:
        """
        Возвращает QuerySet для модели Game
        с выбранными связанными таблицами и фильтрацией для опубликованных игр.
        """
        return (
            GameQuerySet(self.model)
            .related_tables()
            .published()
        )


class AdminGameFileQuerySet(QuerySet):
    """QuerySet для работы с моделью AdminGameFile."""
    def published(self) -> 'AdminGameFileQuerySet':
        """
        Возвращает QuerySet,
        фильтрующий опубликованные админские файлы игры.
        """
        return self.filter(is_published=True)


class UserGameFileQuerySet(QuerySet):
    """QuerySet для работы с моделью UserGameFile."""
    def published(self) -> 'UserGameFileQuerySet':
        """
        Возвращает QuerySet,
        фильтрующий опубликованые пользовательские файлы игры.
        """
        return self.filter(is_published=True)
