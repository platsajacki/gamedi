from typing import Any

from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from users.forms import UserCreateForm, UserUpdateForm
from users.mixins import UserDispatch, UserSlug
from users.models import User


class UserCreateView(generic.CreateView):
    """Представление создания профиля пользователя."""
    form_class = UserCreateForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponseBase:
        """Если пользователь уже прошел аутентификацию, он перенаправляется на домашнюю страницу."""
        if request.user.is_authenticated:
            return redirect('games:home')
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(UserSlug, UserDispatch, generic.DetailView):
    """Представление личного кабинета пользователя."""
    model = User
    queryset = User.objects.prefetch_related('games')


class ProfileUpdateView(UserSlug, UserDispatch, generic.UpdateView):
    """Обновление данных пользователя."""
    model = User
    form_class = UserUpdateForm

    def get_success_url(self) -> str:
        """Возвращает URL для перенаправленияпосле успешного обновления профиля."""
        return reverse('users:profile', kwargs={'username': self.request.user.username})
