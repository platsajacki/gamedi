from django.urls import path

from users.views import ProfileDetailView, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('<slug:username>/', ProfileDetailView.as_view(), name='profile'),
    path('<slug:username>/update/', ProfileUpdateView.as_view(), name='update'),
]
