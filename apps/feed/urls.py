from django.urls import path
from .views import HomeView

app_name = 'feed'

urlpatterns = [
    # This is the main For You Page (FYP)
    path('', HomeView.as_view(), name='home'),
]