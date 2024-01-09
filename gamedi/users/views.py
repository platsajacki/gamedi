from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from users.forms import UserCreateForm, UserUpdateForm
from users.mixins import UserDispatch, UserSlug
from users.models import Game, User


class UserCreateView(generic.CreateView):
    """Представление создания профиля пользовтеля."""
    form_class = UserCreateForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """
        Если пользователь уже прошел аутентификацию,
        он перенаправляется на домашнюю страницу.
        """
        if request.user.is_authenticated:
            return redirect('games:home')
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(UserSlug, UserDispatch, generic.DetailView):
    """Представление личного кабинета пользователя."""
    model = User
    queryset = User.objects.related_games()


class ProfileUpdateView(UserSlug, UserDispatch, generic.UpdateView):
    """Представление личного кабинета пользователя."""
    model = User
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


class ProfileGameDetailView(UserDispatch, generic.DetailView):
    """Представление игры в профиле пользователя."""
    model = User
    template_name = 'users/user_game.html'

    def get_queryset(self) -> QuerySet[Game]:
        """Возвращает QuerySet игр, связанных с указанным пользователем."""
        user: User = get_object_or_404(User, username=self.kwargs['username'])
        return user.games.all()
