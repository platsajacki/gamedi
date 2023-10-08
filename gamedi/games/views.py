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
