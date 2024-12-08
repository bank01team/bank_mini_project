from typing import Any

from matplotlib.rcsetup import validate_color
from rest_framework import serializers

from bank.models import TransactionHistory

from .models import Accounts


class BankTransactionSerializer(serializers.ModelSerializer[TransactionHistory]):
    account_number = serializers.CharField(source="account.account_number", read_only=True)

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
