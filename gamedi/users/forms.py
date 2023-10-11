from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import User


class UserCreateForm(UserCreationForm):
    """Кастомная форма регистрации пользователя."""
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}


class UserUpdateForm(forms.ModelForm):
    """Кастомная форма обновления профиля пользователя."""
    class Meta:
        model = User
        fields = (
            'username', 'first_name',
            'last_name', 'email',
        )
