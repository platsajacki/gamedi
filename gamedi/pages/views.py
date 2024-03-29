from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    """Страница о сайте."""
    template_name = 'pages/about.html'


class RulesTemplateView(TemplateView):
    """Страница с правилами."""
    template_name = 'pages/rules.html'


def csrf_failure(request: HttpRequest, reason='') -> HttpResponse:
    """Обработчик ошибки токена CSRF."""
    return render(request, 'pages/403.html', status=HTTPStatus.FORBIDDEN)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Обработчик ошибки 404 (страница не найдена)."""
    return render(request, 'pages/404.html', status=HTTPStatus.NOT_FOUND)


def server_error(request: HttpRequest) -> HttpResponse:
    """Обработчик внутренней ошибки сервера."""
    return render(request, 'pages/500.html', status=HTTPStatus.INTERNAL_SERVER_ERROR)
