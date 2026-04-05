from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.feed.urls', namespace='feed')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('videos/', include('apps.videos.urls', namespace='videos')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('interactions/', include('apps.interactions.urls', namespace='interactions')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)