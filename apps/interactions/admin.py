from django.contrib import admin
from .models import Comment, Like, Notification, Gift

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'text', 'created_at')
    search_fields = ('user__username', 'text')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'gift_type', 'value', 'created_at')
    list_filter = ('gift_type',)