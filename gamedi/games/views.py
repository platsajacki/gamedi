from django.views import generic

from games.models import Game


class GameListView(generic.ListView):
    """Представление главной страницы сайта."""
    model = Game
    queryset = Game.published.all()


class GameDetailView(generic.DetailView):
    """Представление отдельной страницы игры."""
    model = Game
    queryset = Game.published.all()  # Prefetch
