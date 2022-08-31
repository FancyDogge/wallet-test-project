import decimal
from rest_framework import serializers
from transactions.models import Transaction
from django.db import transaction


# func to calculate commision
def get_commision(transfer_amount, receiver_wallet, sender_wallet):
    return (
        transfer_amount * decimal.Decimal(0.10)
        if receiver_wallet.owner != sender_wallet.owner
        else decimal.Decimal(0.00)
    )


# check is wallet.owner == current user
def check_curr_user_is_sender(sender_wallet, curr_user):
    if sender_wallet.owner != curr_user:
        raise serializers.ValidationError({"error": "wrong sender wallet!"}, code=400)
    else:
        return True


# check is currency is matching
def check_wallet_currs_match(sender_wallet, receiver_wallet):
    if sender_wallet.currency != receiver_wallet.currency:
        raise serializers.ValidationError(
            {"error": "wallet currencies are not matching!"}, code=400
        )
    else:
        return True


# check for enough funds and transaction where sender_wallet=receiver_wallet
def check_enough_wallet_funds(transaction, sender_wallet, receiver_wallet):
    if sender_wallet != receiver_wallet:
        sender_balance_after_transac = sender_wallet.balance - (
            transaction.transfer_amount + transaction.commision
        )
    else:
        raise serializers.ValidationError(
            {"error": "sender and receiver should be different wallets!"}, code=400
        )

    if sender_balance_after_transac >= decimal.Decimal(0.00):
        return sender_balance_after_transac
    else:
        raise serializers.ValidationError(
            {"error": "not enough funds for transaction!"}, code=400
        )


# adding atomicity to our transaction and wallet balances update
def create_successful_transaction(sender_wallet, receiver_wallet, transfer_amount):
    with transaction.atomic():
        # creating transaction instance
        new_transaction = Transaction.objects.create(
            sender=sender_wallet,
            receiver=receiver_wallet,
            transfer_amount=transfer_amount,
            commision=get_commision(transfer_amount, sender_wallet, receiver_wallet),
            status=Transaction.Status.PAID,
        )

        sender_wallet.balance = check_enough_wallet_funds(
            new_transaction, sender_wallet, receiver_wallet
        )
        sender_wallet.save()

        receiver_wallet.balance += new_transaction.transfer_amount
        receiver_wallet.save()

        return new_transaction


def create_failed_transaction(sender_wallet, receiver_wallet, transfer_amount):
    failed_transaction = Transaction.objects.create(
        sender=sender_wallet,
        receiver=receiver_wallet,
        transfer_amount=transfer_amount,
        commision=get_commision(transfer_amount, sender_wallet, receiver_wallet),
        status=Transaction.Status.FAILED,
    )
    return failed_transaction
