from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.views import UserCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('', include('games.urls', namespace='games')),
    path('info/', include('pages.urls', namespace='pages')),
    path('profile/', include('users.urls', namespace='users')),
]

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
