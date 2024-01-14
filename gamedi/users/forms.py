from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError

from users.models import User


class UserCreateForm(UserCreationForm):
    """Регистрация пользователя."""
    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {'username': UsernameField}


class UserUpdateForm(forms.ModelForm):
    """Обновление профиля пользователя."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserMessageForm(forms.Form):
    """Отправка файлов игры."""
    role = forms.CharField(label='Роль', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(label='Электронная почта')


UserMessageFormSetDefault = forms.formset_factory(form=UserMessageForm, extra=0)


class UserMessageFormSet(UserMessageFormSetDefault):  # type: ignore
    """FormSet для отправки файлов игры с дополнительной проверкой электронной почты."""
    def valide_emails(self) -> None:
        """Проверяет, что все поля электронной почты заполнены, и нет дубликатов адресов электронной почты."""
        total_forms: int = int(self.data.get('form-INITIAL_FORMS', 0))
        if not total_forms:
            raise ValidationError('Все поля электронной почты должны быть заполнены.')
        email_set: set = set()
        for i in range(total_forms):
            email: str = self.data.get(f'form-{i}-email')
            if email in email_set:
                raise ValidationError('Дублирование адресов электронной почты не разрешено.')
            email_set.add(email)

    def clean(self) -> None:
        """Запуск валидации."""
        self.valide_emails()
