from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    # This shows these columns in the admin list view
    list_display = ('id', 'user', 'description', 'created_at')
    # Adds a search bar for users and descriptions
    search_fields = ('user__username', 'description')
    # Adds a filter sidebar on the right
    list_filter = ('created_at', 'user')
    # Ensures the ID (UUID) is readable but not editable
    readonly_fields = ('id', 'created_at')