from django.core.exceptions import ValidationError


def validate_order_number(order_number: int, is_published: bool) -> None:
    """Проверяет валидность поля 'order_number'."""
    if order_number == 0 or order_number is None and is_published:
        raise ValidationError('Порядковый номер не может быть равен 0 и должен быть у опубликованного элемента.')
