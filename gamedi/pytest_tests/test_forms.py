import pytest

from django.core.exceptions import ValidationError

from games.forms import RoleMessageFormSet


def test_role_message_form_set_valid_data(formset_data: dict):
    """RoleMessageFormSet валидна при верных данных"""
    assert RoleMessageFormSet(formset_data).is_valid()


def test_role_message_form_set_duplication_email(formset_data: dict):
    """Дублирование email запрещено."""
    formset_data['form-1-email'] = formset_data['form-0-email']
    with pytest.raises(ValidationError):
        RoleMessageFormSet(formset_data).clean()
