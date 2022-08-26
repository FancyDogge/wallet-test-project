from django.db import models
from django.contrib.auth.models import User
import string
import random


# Creating unique ID for wallets
def get_uuid():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Wallet(models.Model):
    class Currency(models.TextChoices):
        RUB = "RUB"
        EUR = "EUR"
        USD = "USD"

    class CardType(models.TextChoices):
        VISA = "visa"
        MASTERCARD = "mastercard"
    
    name = models.CharField(
        max_length=8, editable=False, unique=True, default=get_uuid
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    type = models.CharField(max_length=10, choices=CardType.choices)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.pk}, Wallet: {self.name}, Owner: {self.owner.username}"


class Transaction(models.Model):

    class Status(models.TextChoices):
        PAID = "PAID"
        FAILED = "FAILED"

    sender = models.ForeignKey(Wallet, related_name="sender", on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(Wallet, related_name="reciever", on_delete=models.DO_NOTHING)
    transfer_amount = models.DecimalField(max_digits=14, decimal_places=2)
    commision = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=6, choices=Status.choices)
    timestamp = models.DateTimeField(auto_now_add=True)