from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import UserCreateForm, UserUpdateForm
from .models import User
from .mixins import UserDispatch, UserAttribute


class UserCreateView(generic.CreateView):
    """Представление создания профиля пользовтеля."""
    form_class = UserCreateForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')

    def dispatch(
            self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """
        Если пользователь уже прошел аутентификацию,
        он перенаправляется на домашнюю страницу.
        """
        if request.user.is_authenticated:
            return redirect('games:home')
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(
    LoginRequiredMixin, UserAttribute, UserDispatch, generic.DetailView
):
    """Представление личного кабинета пользователя."""
    queryset = User.objects.related_games()


class ProfileUpdateView(
    LoginRequiredMixin, UserAttribute, UserDispatch, generic.UpdateView
):
    """Представление личного кабинета пользователя."""
    form_class = UserUpdateForm

    def get_success_url(self) -> str:
        """
        Возвращает URL для перенаправления
        после успешного обновления профиля.
        """
        return reverse(
            'users:profile',
            kwargs={'username': self.request.user.username}
        )


class ProfileGameDetailView(
    LoginRequiredMixin, UserDispatch, generic.DetailView
):
    """Представление игры в профиле пользователя."""
    template_name = 'users/user_game.html'

    def get_queryset(self) -> QuerySet:
        """Возвращает QuerySet игр, связанных с указанным пользователем."""
        user: User = get_object_or_404(User, username=self.kwargs['username'])
        return user.games
