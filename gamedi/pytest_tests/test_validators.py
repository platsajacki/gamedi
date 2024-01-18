import pytest

from django.core.exceptions import ValidationError

from games.validators import validate_order_number


def test_validate_order_number_valid():
    """Проверяем, что исключение не выбрасывается при валидных значениях."""
    validate_order_number(1, True)
    validate_order_number(1, False)
    validate_order_number(None, False)


def test_validate_order_number_invalid():
    """Проверяем, что исключение выбрасывается при невалидных значениях."""
    with pytest.raises(ValidationError):
        validate_order_number(0, True)
    with pytest.raises(ValidationError):
        validate_order_number(0, False)
