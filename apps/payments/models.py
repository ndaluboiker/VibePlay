from django.db import models
from django.conf import settings
from decimal import Decimal

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    coins = models.PositiveIntegerField(default=0)  # Used for Gifting
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Real $

    def receive_gift(self, coin_value):
        """When a user gifts, creator gets 40% value in real money."""
        # Assume 1 coin = $0.01 for this example
        total_value = Decimal(coin_value) * Decimal('0.01')
        self.earnings += total_value * Decimal('0.40')
        self.save()
        # The remaining 60% stays as site profit (Admin)