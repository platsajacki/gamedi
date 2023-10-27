from django.db.models import QuerySet, Manager


class GameQuerySet(QuerySet):
    def related_tables(self) -> QuerySet:
        return self.select_related('genre')

    def published(self) -> QuerySet:
        return self.filter(
            is_published=True,
            genre__is_published=True
        )


class GameManager(Manager):
    def get_queryset(self) -> QuerySet:
        return (
            GameQuerySet(self.model)
            .related_tables()
            .published()
        )
