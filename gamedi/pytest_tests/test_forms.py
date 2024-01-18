import pytest

from django.core.exceptions import ValidationError

from games.forms import RoleMessageFormSet


def test_role_message_form_set_valid_data(form_data: dict):
    """RoleMessageFormSet валидна при верных данных"""
    assert RoleMessageFormSet(form_data).is_valid()


def test_role_message_form_set_duplication_email(form_data: dict):
    """Дублирование email запрещено."""
    form_data['form-1-email'] = form_data['form-0-email']
    with pytest.raises(ValidationError):
        RoleMessageFormSet(form_data).clean()


def test_role_message_form_set_empty_email(form_data: dict):
    """Все email должны быть заполнены."""
    form_data['form-1-email'] = ''
    with pytest.raises(ValidationError):
        RoleMessageFormSet(form_data).clean()
