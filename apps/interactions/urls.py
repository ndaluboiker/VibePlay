from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    # Like and Follow
    path('like/<uuid:video_id>/', views.ajax_like, name='like'),
    path('follow/<uuid:user_id>/', views.ajax_follow, name='follow'),

    # Comments
    path('comments/<uuid:video_id>/', views.get_comments, name='get_comments'),
    path('post-comment/<uuid:video_id>/', views.ajax_post_comment, name='post_comment'),

    # Inbox and Notifications
    path('inbox/', views.inbox_view, name='inbox'),
    path('check-notifs/', views.check_notifications, name='check_notifs'),

    # Search
    path('search/', views.search_vibes, name='search'),
]