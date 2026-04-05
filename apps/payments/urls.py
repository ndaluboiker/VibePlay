from django.urls import path
from . import views

# This matches the namespace='payments' in your config/urls.py
app_name = 'payments'

urlpatterns = [
    # We will add payment paths here later (e.g., wallet, deposit)
    # path('wallet/', views.WalletView.as_view(), name='wallet'),
]