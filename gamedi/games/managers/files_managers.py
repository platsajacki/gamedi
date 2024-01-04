from django.db.models import QuerySet


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
