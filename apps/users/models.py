from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    """
    Custom User Model for VibePic.
    Uses UUID as primary key and supports a Follower/Following system.
    """
    # 1. Identity & Security
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # 2. Profile Details
    profile_pic = models.ImageField(
        upload_to='profiles/%Y/%m/',
        default='profiles/default_avatar.png',
        null=True,
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True)

    # 3. Social Graph (The Follow Logic)
    # symmetrical=False allows TikTok style: I follow you, but you don't have to follow me.
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    # 4. Digital Wallet / Gifting
    coins = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    # Helper methods for the Profile UI
    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def post_count(self):
        # Accesses videos related to this user
        return self.videos.count()