from django.db import models
from wallet.models import Wallet


class Transaction(models.Model):
    class Status(models.TextChoices):
        PAID = "PAID"
        FAILED = "FAILED"

    sender = models.ForeignKey(
        Wallet, related_name="sender", on_delete=models.DO_NOTHING
    )
    receiver = models.ForeignKey(
        Wallet, related_name="reciever", on_delete=models.DO_NOTHING
    )
    transfer_amount = models.DecimalField(max_digits=14, decimal_places=2)
    commision = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=6, choices=Status.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"id: {self.pk} || From: {self.sender.name} >>> To: {self.receiver.name}"
