import decimal
from rest_framework import serializers
from .models import Wallet, Transaction
from django.db import transaction


# Serializer with all Wallet model fields
class FullWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ["balance"]

    # Overriding create method of the ModelSerializer
    def create(self, validated_data):
        current_user = self.context["request"].user
        current_user_wallets = current_user.wallet_set.filter(owner=current_user)

        # Function to apply welcome bonus when creating a new wallet
        def welcome_bonus(currency_type):
            bonus_dict = {
                "RUB": 100,
                "USD": 3,
                "EUR": 3,
            }
            return bonus_dict[currency_type]

        # Check if user's wallet count < 5
        if current_user_wallets.count() < 5:
            try:
                validated_data["owner"] = current_user
                new_wallet = Wallet.objects.create(**validated_data)
                new_wallet.balance = welcome_bonus(new_wallet.currency)
                new_wallet.save()
                return new_wallet
            except Exception as e:
                return e

        raise serializers.ValidationError(
            {"error": "you can't have more than 5 wallets!"}
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["commision", "status"]

    # Overriding create method of the ModelSerializer
    def create(self, validated_data):
        # func to calculate commision
        def get_commision(transfer_amount, commision_bool):
            return (
                transfer_amount * decimal.Decimal(0.10)
                if commision_bool
                else decimal.Decimal(0.00)
            )
        # getting sender and receiver ids, transfer_amount
        sender_wallet = Wallet.objects.get(pk=validated_data["sender"].id)
        receiver_wallet = Wallet.objects.get(pk=validated_data["receiver"].id)
        transfer_amount = validated_data["transfer_amount"]
        # commision_bool to determine if transaction will have comission
        commision_bool = (
            False if receiver_wallet.owner == sender_wallet.owner else True
        )

        # check is wallet.owner == current user
        if sender_wallet.owner == self.context["request"].user:
            # check is currency is matching
            if receiver_wallet.currency == sender_wallet.currency:
                try:
                    # adding atomicity to our transaction and wallet balances update
                    with transaction.atomic():
                    # creating transaction instance
                        new_transaction = Transaction.objects.create(
                        sender=sender_wallet,
                        receiver=receiver_wallet,
                        transfer_amount=transfer_amount,
                        commision=get_commision(transfer_amount, commision_bool),
                        status=Transaction.Status.PAID,
                        )
                        sender_balance_after_transac = sender_wallet.balance - (
                            new_transaction.transfer_amount + new_transaction.commision
                        )
                        # updating both balances + check for enough funds
                        if sender_balance_after_transac >= decimal.Decimal(0.00):
                            sender_wallet.balance = sender_balance_after_transac
                        else:
                            raise serializers.ValidationError(
                                {"error": "not enough funds for transaction!"}
                            )
                        sender_wallet.save()
                        receiver_wallet.balance += new_transaction.transfer_amount
                        receiver_wallet.save()
                    return new_transaction
                # if smth goes wrong, create and return FAILED transaction
                except:
                        failed_transaction = Transaction.objects.create(
                        sender=sender_wallet,
                        receiver=receiver_wallet,
                        transfer_amount=transfer_amount,
                        commision=get_commision(transfer_amount, commision_bool),
                        status=Transaction.Status.FAILED,
                        )
                        return failed_transaction

            raise serializers.ValidationError(
                {"error": "wallet currencies are not matching!"}
            )
        raise serializers.ValidationError({"error": "wrong sender wallet!"})