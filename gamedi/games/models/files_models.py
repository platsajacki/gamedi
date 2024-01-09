from django.db import models

from core.models import FileModel, NameString
from games.managers import AdminGameFileQuerySet, UserGameFileQuerySet


class AdminGameFile(NameString, FileModel, models.Model):
    """Модель для хранения файлов, принадлежащих играм."""
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование'
    )
    game = models.ForeignKey(
        'games.Game',
        on_delete=models.CASCADE,
        related_name='admin_files',
        verbose_name='Игра',
    )

    objects = AdminGameFileQuerySet.as_manager()

    class Meta:
        verbose_name = 'Файл игры для администратора'
        verbose_name_plural = 'Файлы игр для администратора'
        unique_together = ('game', 'name',)
        ordering = ('game', 'order_number',)


class UserGameFile(NameString, FileModel, models.Model):
    """Модель для хранения файлов, принадлежащих играм."""
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование'
    )
    game = models.ForeignKey(
        'games.Game',
        on_delete=models.CASCADE,
        related_name='users_files',
        verbose_name='Игра',
    )

    objects = UserGameFileQuerySet.as_manager()

    class Meta:
        verbose_name = 'Файл игры для пользователя'
        verbose_name_plural = 'Файлы игр для пользователя'
        unique_together = ('game', 'name',)
        ordering = ('game', 'order_number',)
