from django.urls import path

from pages.views import AboutTemplateView, RulesTemplateView

app_name = 'pages'

urlpatterns = [
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('rules/', RulesTemplateView.as_view(), name='rules')
]
