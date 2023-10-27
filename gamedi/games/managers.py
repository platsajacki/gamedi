from django.db.models import QuerySet, Manager


class GameQuerySet(QuerySet):
    def related_tables(self) -> 'GameQuerySet':
        """
        Отимизирует запрос, присоединяя таблицы.
        """
        return self.select_related('genre')

    def published(self) -> 'GameQuerySet':
        """
        Возвращает QuerySet, который фильтрует опубликованые игры
        и принадлежат опубликованным жанрам.
        """
        return self.filter(
            is_published=True,
            genre__is_published=True
        )


class GameManager(Manager):
    """
    Возвращает QuerySet для модели Game
    с выбранными связанными таблицами и фильтрацией для опубликованных игр.
    """
    def get_queryset(self) -> GameQuerySet:
        return (
            GameQuerySet(self.model)
            .related_tables()
            .published()
        )
