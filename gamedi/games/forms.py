from django import forms
from django.core.exceptions import ValidationError


class RoleMessageForm(forms.Form):
    """Отправка файлов игры."""
    role = forms.CharField(label='Роль', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(label='Электронная почта', required=False)


RoleMessageFormSetDefault = forms.formset_factory(form=RoleMessageForm, extra=0)


class RoleMessageFormSet(RoleMessageFormSetDefault):  # type: ignore
    """FormSet для отправки файлов игры с дополнительной проверкой электронной почты."""
    def valide_emails(self) -> None:
        """Проверяет, что все поля электронной почты заполнены, и нет дубликатов адресов электронной почты."""
        email_set: set = set()
        for i in range(int(self.data.get('form-INITIAL_FORMS', 0))):
            email: str = self.data.get(f'form-{i}-email')
            if email in email_set and email is not None:
                raise ValidationError('Дублирование адресов электронной почты не разрешено.')
            email_set.add(email)

    def clean(self) -> None:
        """Запуск валидации."""
        self.valide_emails()
