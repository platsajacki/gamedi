import os
from typing import Any

from django.db.models import Model
from django.db.models.fields import Field
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .models import Game, AdminGameFile, UserGameFile


@receiver(pre_delete, sender=Game)
@receiver(pre_delete, sender=AdminGameFile)
@receiver(pre_delete, sender=UserGameFile)
def delete_gamefile(
    sender: Model, instance: Model, **kwargs: dict[str, Any]
) -> None:
    """Удаляет файл, связанный с объектом, если он существует."""
    for field_name in sender.get_files_filds():
        path = getattr(instance, field_name).path
        if os.path.isfile(path):
            os.remove(path)


@receiver(pre_save, sender=Game)
@receiver(pre_save, sender=AdminGameFile)
@receiver(pre_save, sender=UserGameFile)
def update_gamefile(
    sender: Model, instance: Model, **kwargs: dict[str, Any]
) -> None:
    """
    Обновляет файл, связанный с объектом перед обновлением,
    удаляя старый файл.
    """
    for field_name in sender.get_files_filds():
        if (old_instance := sender.objects.filter(id=instance.id)).exists():
            old_file: Field = getattr(old_instance.first(), field_name)
            file: Field = getattr(instance, field_name)
            if old_file != file and os.path.isfile(old_file.path):
                os.remove(old_file.path)
