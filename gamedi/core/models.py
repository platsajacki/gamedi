from django.db import models


class NameString(models.Model):
    """
    Абстарктная модель с полем 'name' и его строковым предсталением.
    """
    name = models.CharField(
        max_length=128, unique=True,
        verbose_name='Наименование'
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Строкового предсталение поля 'name'."""
        return self.name


class Discription(models.Model):
    """Абстарктная модель с полем 'discription'."""
    discription = models.TextField(
        max_length=1024, verbose_name='Описание'
    )

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """Модель для хранения информации о игре."""
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text=(
            'Укажите адрес страницы. Используйте только '
            'латиницу, цифры, дефисы и знаки подчёркивания'
        ),
        verbose_name='Адрес (slug)'
    )

    class Meta:
        abstract = True
