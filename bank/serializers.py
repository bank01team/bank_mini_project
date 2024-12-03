from typing import Any

from rest_framework import serializers

from bank.models import TransactionHistory

from .models import Accounts


class BankTransactionSerializer(serializers.ModelSerializer[TransactionHistory]):
    class Meta:
        model = TransactionHistory
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer[Accounts]):
    class Meta:
        model = Accounts
        fields = "__all__"

    def create(self, validated_data: dict[str, Any]) -> Accounts:
        account = Accounts.objects.create(**validated_data)
        return account
