from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import User


class UserCreateForm(UserCreationForm):
    """Кастомная форма регистрации пользователя."""
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}
