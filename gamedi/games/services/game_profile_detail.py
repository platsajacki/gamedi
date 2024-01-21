import logging
from dataclasses import dataclass
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.services import BaseService
from games.forms import RoleMessageFormSet
from users.utils import send_role_and_file_email

logger = logging.getLogger(__name__)


@dataclass
class GameProfileDetailContextService(BaseService):
    """Получает контекст для отображения игры в профиле пользователя."""
    context: dict[str, Any]

    def act(self) -> dict[str, Any]:
        """Флаг "need_empty_formset - (bool)" указывает, нужно ли включать пустой FormSet в контекст."""
        if self.context.get('need_empty_formset', True):
            self.context['formset'] = RoleMessageFormSet(
                initial=[{'role': file.name} for file in self.context['object'].users_files.all()]
            )
        return self.context


@dataclass
class GameProfileDetailPostService(BaseService):
    """Обрабатывает POST запрос и отправляет ответ пользователю."""
    request: HttpRequest
    context: dict[str, Any]
    template_name: str
    kwargs: dict[str, Any]

    def act(self) -> HttpResponse:
        """При валидности FormSet направляет игрокам файлы."""
        formset: RoleMessageFormSet = RoleMessageFormSet(self.request.POST)
        valid_formset: bool = formset.is_valid()
        self.context['need_empty_formset'] = not valid_formset
        context: dict[str, Any] = GameProfileDetailContextService(self.context)()
        if valid_formset:
            try:
                send_role_and_file_email(request=self.request, context=context, formset=formset)
            except Exception as e:
                context['exception'] = 'Ошибка отправки. Попробуйте отправить снова или скачайте полный файл с игрой.'
                logger.error(msg=e, exc_info=True)
        else:
            context['formset'] = formset
        return render(self.request, self.template_name, context)
