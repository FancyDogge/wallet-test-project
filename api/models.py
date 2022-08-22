from django.db import models
from django.contrib.auth.models import User
import uuid


unique_code = uuid.uuid4().hex[:8].upper()


class Wallet(models.Model):

    class Currency(models.TextChoices):
        RUB = "RUB"
        EUR = "EUR"
        USD = "USD"

    class CardType(models.TextChoices):
        VISA = "visa"
        MASTERCARD = "mastercard"

    name = models.CharField(
        max_length=8, primary_key=True, default=unique_code, editable=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CardType.choices)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet: {self.name}, Owner: {self.owner.username}"
