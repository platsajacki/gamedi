from django.urls import path

from games.views import GameDetailView, GameListView, DownloadingGameFilesTemplateView, GameProfileDetailView

app_name = 'games'

urlpatterns = [
    path('', GameListView.as_view(), name='home'),
    path('<slug:slug>/', GameDetailView.as_view(), name='detail'),
    path('<slug:username>/games/<slug:slug>', GameProfileDetailView.as_view(), name='game'),
    path(
        '<slug:username>/games/<slug:slug>/download/',
        DownloadingGameFilesTemplateView.as_view(),
        name='download_files',
    ),
]
