from django.db import models

from core.models import Description, NameString, PublishedModel, SlugModel


class Genre(NameString, Description, SlugModel, PublishedModel, models.Model):
    """Модель для хранения информации о жанре игр."""
    name = models.CharField(
        max_length=128, unique=True,
        verbose_name='Наименование'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
