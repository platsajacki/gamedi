from django.shortcuts import get_object_or_404
from django.db. models import QuerySet
from django.views import generic

from .models import Game


class GameListView(generic.ListView):
    """Представление главной странцы сайта."""
    model = Game
    queryset = Game.objects.all()


class GameDetailView(generic.DetailView):
    """Представление отдельной странцы игры."""
    model = Game
    queryset = Game.objects.all()
