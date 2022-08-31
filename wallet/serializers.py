from rest_framework import serializers
from .models import Wallet



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


# отдельн сериал под сендер и реси
# сендер = сериал
