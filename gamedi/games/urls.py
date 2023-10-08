from django.urls import path

from .views import GameListView

app_name = 'games'

urlpatterns = [
    path('', GameListView.as_view(), name='home'),
]
