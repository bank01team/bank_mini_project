from rest_framework import serializers

from bank.models import TransactionHistory


class BankTransactionSerializer(serializers.ModelSerializer[TransactionHistory]):
    class Meta:
        model = TransactionHistory
        fields = "__all__"
