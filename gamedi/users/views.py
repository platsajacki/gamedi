from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserCreateForm


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
