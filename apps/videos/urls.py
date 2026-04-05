from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    # Main TikTok Feed
    path('', views.feed_view, name='feed'),

    # Infinite Scroll API (Shuffle Engine)
    path('api/shuffled/', views.get_shuffled_chunk, name='get_shuffled'),

    # Direct Device/Camera Upload
    path('upload/', views.upload_video, name='upload'),

    # Single Video View
    path('video/<uuid:video_id>/', views.video_detail, name='video_detail'),
]