from django.urls import path

from users.views import DownloadingGameFilesTemplateView, ProfileDetailView, ProfileGameDetailView, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('<slug:username>/', ProfileDetailView.as_view(), name='profile'),
    path('<slug:username>/update/', ProfileUpdateView.as_view(), name='update'),
    path('<slug:username>/games/<slug:slug>', ProfileGameDetailView.as_view(), name='game'),
    path(
        '<slug:username>/games/<slug:slug>/download/',
        DownloadingGameFilesTemplateView.as_view(),
        name='download_files',
    ),
]
