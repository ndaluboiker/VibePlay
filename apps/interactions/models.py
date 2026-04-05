from django.db import models
from django.conf import settings
import uuid


# 1. LIKES
class Like(models.Model):
    video = models.ForeignKey('videos.Video', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')  # Prevents double-liking


# 2. COMMENTS & REPLIES
class Comment(models.Model):
    video = models.ForeignKey('videos.Video', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    # Self-referencing ForeignKey allows TikTok-style nested replies
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


# 3. NOTIFICATIONS (The "Inbox" feature)
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('gift', 'Gift'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)

    # Optional: Link to the specific video if the notification is a like/comment/gift
    video = models.ForeignKey('videos.Video', on_delete=models.CASCADE, null=True, blank=True)

    text = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


# 4. USER GIFTS (Virtual Economy)
class Gift(models.Model):
    GIFT_CHOICES = (
        ('rose', 'Rose'),
        ('diamond', 'Diamond'),
        ('crown', 'Crown'),
    )

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gifts_sent')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gifts_received')
    video = models.ForeignKey('videos.Video', on_delete=models.CASCADE, related_name='video_gifts')

    gift_type = models.CharField(max_length=20, choices=GIFT_CHOICES)
    value = models.IntegerField(default=0)  # Point value or coin value
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} sent {self.gift_type} to {self.receiver.username}"