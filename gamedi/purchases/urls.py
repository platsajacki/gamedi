from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from purchases.views import ConfirmationView, CreatePurchaseView

app_name = 'purchases'

urlpatterns = [
    path('payment/games/<slug:slug>/', CreatePurchaseView.as_view(), name='payment'),
    path('payment/confirmation/', csrf_exempt(ConfirmationView.as_view()), name='confirmation',),
]
