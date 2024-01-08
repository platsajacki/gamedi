from django.urls import path

from .views import ProfileDetailView, ProfileGameDetailView, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('<slug:username>/', ProfileDetailView.as_view(), name='profile'),
    path('<slug:username>/update/', ProfileUpdateView.as_view(), name='update'),
    path('<slug:username>/games/<slug:slug>', ProfileGameDetailView.as_view(), name='game'),
]
