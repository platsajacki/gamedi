from django.db import models

from games.utils import get_file_path
from games.validators import validate_order_number


class NameString(models.Model):
    """
    Абстарктная модель со строковым предсталением поля 'name'.
    """
    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Строкового предсталение поля 'name'."""
        name = getattr(self, 'name', None)
        if name is not None:
            return str(name)

        return super().__str__()


class Description(models.Model):
    """Абстарктная модель с полем 'description'."""
    description = models.TextField(max_length=1024, verbose_name='Описание')

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """Абстрактная модель с полем 'slug'."""
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


class OrderNumberModel(models.Model):
    """Абстрактная модель с полем 'order_number'."""
    order_number = models.PositiveSmallIntegerField(verbose_name='Порядковый номер', null=True, blank=True)

    class Meta:
        abstract = True


class PublishedModel(models.Model):
    """Абстарктная модель с полями 'is_published' и 'created'."""
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        abstract = True


class FileModel(OrderNumberModel, PublishedModel, models.Model):
    """Абстрактная модель с полем 'file' и методом 'get_files_fields'."""
    file = models.FileField(
        upload_to=get_file_path,
        verbose_name='Файл',
        unique=True
    )

    class Meta:
        abstract = True

    def clean(self) -> None:
        """Проверка валидности полей."""
        validate_order_number(self.order_number, self.is_published)
        super().clean()

    @staticmethod
    def get_files_fields() -> tuple[str]:
        """Получает строчное наименование полей с файлами."""
        return ('file',)
