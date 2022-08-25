from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet


class FullWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ["balance"]

    def create(self, validated_data):

        def welcome_bonus(currency_type):
            bonus_dict = {
                'RUB': 100,
                'USD': 3,
                'EUR': 3,
            }
            return bonus_dict[currency_type]

        validated_data["owner"] = self.context["request"].user
        new_wallet = Wallet.objects.create(**validated_data)
        new_wallet.balance = welcome_bonus(new_wallet.currency)
        new_wallet.save()

        return new_wallet

    
