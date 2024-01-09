import os
from typing import Any

from django.db.models import F, FileField, Max, QuerySet
from django.db.models.signals import post_delete, pre_delete, pre_save
from django.dispatch import receiver

from games.models import AdminGameFile, Game, UserGameFile


@receiver(pre_delete, sender=Game)
@receiver(pre_delete, sender=AdminGameFile)
@receiver(pre_delete, sender=UserGameFile)
def delete_gamefile(
    sender: Game | AdminGameFile | UserGameFile,
    instance: Game | AdminGameFile | UserGameFile,
    **kwargs: dict[str, Any]
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
    sender: Game | AdminGameFile | UserGameFile,
    instance: Game | AdminGameFile | UserGameFile,
    **kwargs: dict[str, Any]
) -> None:
    """
    Обновляет файл, связанный с объектом перед обновлением,
    удаляя старый файл.
    """
    for field_name in sender.get_files_filds():
        if (old_instance := sender.objects.filter(id=instance.id)).exists():  # type: ignore
            old_file: FileField = getattr(old_instance.first(), field_name)
            old_file_path: str = getattr(old_file, 'path')
            file: FileField = getattr(instance, field_name)
            if old_file != file and os.path.isfile(old_file_path):
                os.remove(old_file_path)


@receiver(pre_save, sender=Game)
@receiver(pre_save, sender=AdminGameFile)
@receiver(pre_save, sender=UserGameFile)
def update_orders_numbers(
    sender: Game | AdminGameFile | UserGameFile,
    instance: Game | AdminGameFile | UserGameFile,
    **kwargs: dict[str, Any]
) -> None:
    """
    Меняет порядковые номера элементов при создании или изменении элемента.
    """
    if sender == Game:
        queryset: QuerySet = sender.objects.all()  # type: ignore
    else:
        queryset: QuerySet = sender.objects.filter(game=instance.game)  # type: ignore
    # Если в модели нет элементов.
    if not queryset:
        if instance.is_published:
            instance.order_number = 1
        else:
            instance.order_number = None
        return
    old_elem: QuerySet = queryset.filter(id=instance.id)
    old_elem_exists: bool = old_elem.exists()
    if old_elem_exists:
        old_order_number: int = old_elem.first().order_number  # type: ignore
    # У неопубликованного и только что снятого с публикации
    # элемента нет порядкового номера.
    if not instance.is_published:
        instance.order_number = None
        if old_elem_exists and old_order_number is not None:
            queryset.filter(
                order_number__gt=old_order_number
            ).update(
                order_number=F('order_number') - 1
            )
        return
    max_order_number: int = (
        queryset
        .aggregate(Max('order_number'))
        ['order_number__max']
    )
    # Если элемент новый или вновь опубликованный,
    # обновляем порядковые номера после его порядкого номера.
    if (
        instance.id is None
        or old_elem_exists
        and old_order_number is None
    ):
        if instance.order_number > max_order_number:
            instance.order_number = max_order_number + 1
            return
        queryset.filter(
            order_number__gte=instance.order_number
        ).update(
            order_number=F('order_number') + 1
        )
        return
    # Eсли элемент меняет порядковый номер.
    if instance.order_number != old_order_number:
        if instance.order_number and instance.order_number > max_order_number:
            queryset.filter(
                order_number__gt=old_order_number
            ).update(
                order_number=F('order_number') - 1
            )
            instance.order_number = max_order_number
        else:
            queryset.filter(
                order_number__gt=old_order_number,
                order_number__lte=instance.order_number
            ).update(
                order_number=F('order_number') - 1
            )
            queryset.filter(
                order_number__lt=old_order_number,
                order_number__gte=instance.order_number
            ).update(
                order_number=F('order_number') + 1
            )


@receiver(post_delete, sender=Game)
@receiver(post_delete, sender=AdminGameFile)
@receiver(post_delete, sender=UserGameFile)
def delete_orders_numbers(
    sender: Game | AdminGameFile | UserGameFile,
    instance: Game | AdminGameFile | UserGameFile,
    **kwargs: dict[str, Any]
) -> None:
    """Меняет порядковые номера элементов при удалении элемента."""
    if sender == Game:
        queryset: QuerySet = sender.objects.all()  # type: ignore
    else:
        queryset: QuerySet = sender.objects.filter(game=instance.game)  # type: ignore
    queryset.filter(
        order_number__gt=instance.order_number
    ).update(
        order_number=F('order_number') - 1
    )
