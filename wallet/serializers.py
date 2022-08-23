from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet


class FullWalletSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ['balance'] 

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return Wallet.objects.create(**validated_data)