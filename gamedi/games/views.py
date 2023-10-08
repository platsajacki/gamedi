from django.views import generic

from .models import Game


class GameListView(generic.ListView):
    """Представление главной странцы сайта."""
    model = Game
    queryset = Game.objects.all()
