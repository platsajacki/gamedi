from django.urls import path

from .views import GameDetailView, GameListView

app_name = 'games'

urlpatterns = [
    path('', GameListView.as_view(), name='home'),
    path('<slug:slug>/', GameDetailView.as_view(), name='detail'),
]
