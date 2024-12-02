from typing import Any

from rest_framework import serializers

from .models import Accounts


class AccountSerializer(serializers.ModelSerializer[Accounts]):
    class Meta:
        model = Accounts
        fields = "__all__"

    def create(self, validated_data: dict[str, Any]) -> Accounts:
        account = Accounts.objects.create(**validated_data)
        return account
