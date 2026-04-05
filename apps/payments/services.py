from django.db import transaction
from .models import Transaction

class PaymentService:
    """
    Handles all financial logic for VibePlay.
    """
    @staticmethod
    def process_deposit(user, amount, description="Wallet Deposit"):
        """
        Adds funds to a user's balance and records the transaction.
        """
        try:
            with transaction.atomic():
                # 1. Update the User's balance field
                user.balance += amount
                user.save()

                # 2. Create the Transaction record
                return Transaction.objects.create(
                    user=user,
                    amount=amount,
                    transaction_type='deposit',
                    description=description
                )
        except Exception as e:
            print(f"Payment Error: {e}")
            return None

    @staticmethod
    def process_gift(sender, receiver, amount):
        """
        Transfers money from one user to another (e.g., tipping a creator).
        """
        if sender.balance < amount:
            return False, "Insufficient funds"

        try:
            with transaction.atomic():
                # Deduct from sender
                sender.balance -= amount
                sender.save()

                # Add to receiver
                receiver.balance += amount
                receiver.save()

                # Record for both
                Transaction.objects.create(
                    user=sender, amount=-amount,
                    transaction_type='gift', description=f"Gift to {receiver.username}"
                )
                Transaction.objects.create(
                    user=receiver, amount=amount,
                    transaction_type='gift', description=f"Gift from {sender.username}"
                )
            return True, "Success"
        except Exception:
            return False, "Transaction failed"