from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def welcome_user(sender, instance, created, **kwargs):
    if created:
        # Logic: Send a system notification or log
        # registration event here
        print(f"New VibePlay Creator Joined: {instance.username}")