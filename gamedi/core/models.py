from django.db import models

from games.utils import get_file_path


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
    """Абстарктная модель с полем 'slug'."""
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


class FileModel(models.Model):
    """Абстарктная модель с полем 'file' и методом 'get_files_filds'."""
    file = models.FileField(
        upload_to=get_file_path,
        verbose_name='Файл',
        unique=True
    )
    order_number = models.PositiveSmallIntegerField(
        verbose_name='Порядковый номер'
    )

    class Meta:
        abstract = True
        unique_together = ('game', 'order_number',)
        ordering = ('game', 'order_number',)

    @staticmethod
    def get_files_filds() -> tuple[str]:
        """Получает строчное наименование полей с файлами."""
        return ('file',)
