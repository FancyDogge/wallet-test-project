from rest_framework import serializers
from wallet.models import Wallet
from transactions.models import Transaction
from transactions.utils import (
    check_curr_user_is_sender,
    check_wallet_currs_match,
    create_failed_transaction,
    create_successful_transaction,
)


class TransactionSerializer(serializers.ModelSerializer):
    # repr wallet names instead of pk
    sender = serializers.SlugRelatedField(
        queryset=Wallet.objects.all(), slug_field="name"
    )
    receiver = serializers.SlugRelatedField(
        queryset=Wallet.objects.all(), slug_field="name"
    )

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["commision", "status"]

    # Overriding create method of the ModelSerializer
    def create(self, validated_data):
        # getting sender and receiver ids, transfer_amount
        curr_user = self.context["request"].user
        sender_wallet = Wallet.objects.get(pk=validated_data["sender"].id)
        receiver_wallet = Wallet.objects.get(pk=validated_data["receiver"].id)
        transfer_amount = validated_data["transfer_amount"]

        if check_curr_user_is_sender(
            sender_wallet, curr_user
        ) and check_wallet_currs_match(sender_wallet, receiver_wallet):
            try:
                # adding atomicity to our transaction and wallet balances update
                return create_successful_transaction(
                    sender_wallet, receiver_wallet, transfer_amount
                )
                # if smth goes wrong, create and return FAILED transaction
            except:
                return create_failed_transaction(
                    sender_wallet, receiver_wallet, transfer_amount
                )
