import logging
from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from users.forms import UserCreateForm, UserMessageFormSet, UserUpdateForm
from users.mixins import UserDispatch, UserSlug
from users.models import Game, User
from users.utils import send_role_and_file_email

logger = logging.getLogger(__name__)


class UserCreateView(generic.CreateView):
    """Представление создания профиля пользователя."""
    form_class = UserCreateForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """Если пользователь уже прошел аутентификацию, он перенаправляется на домашнюю страницу."""
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
        """Возвращает URL для перенаправленияпосле успешного обновления профиля."""
        return reverse('users:profile', kwargs={'username': self.request.user.username})


class ProfileGameDetailView(UserDispatch, generic.DetailView):
    """Представление игры в профиле пользователя."""
    model = User
    template_name = 'users/user_game.html'

    def get_queryset(self) -> QuerySet[Game]:
        """Возвращает QuerySet игр, связанных с указанным пользователем."""
        return get_object_or_404(User, username=self.kwargs['username']).games.all()

    def get_context_data(self, need_formset: bool = True, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Получает контекст для отображения.
        Флаг "need_formset - (bool)" указывает, нужно ли включать пустой FormSet в контекст.
        """
        if self.request.method == 'POST':
            self.object = self.get_object()
        context: dict[str, Any] = super().get_context_data(**kwargs)
        if need_formset:
            formset: UserMessageFormSet = UserMessageFormSet(
                initial=[{'role': file.name} for file in self.object.users_files.all()]
            )
            context['formset'] = formset
        return context

    def post(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> HttpResponse:
        """Обрабатывает POST запрос. При валидности FormSet направляет игрокам файлы."""
        formset: UserMessageFormSet = UserMessageFormSet(request.POST)
        if formset.is_valid():
            context: dict[str, Any] = self.get_context_data(need_formset=False, **kwargs)
            try:
                send_role_and_file_email(request=request, context=context, formset=formset)
            except Exception as e:
                context['exception'] = 'Ошибка отправки. Скачайте полный файл с игрой или попробуйте отправить снова.'
                logger.error(msg=e, exc_info=True)
            return self.render_to_response(context)
        context: dict[str, Any] = self.get_context_data(**kwargs)  # type: ignore
        context['formset'] = formset
        return self.render_to_response(context)
