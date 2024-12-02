from typing import Any

from rest_framework import serializers

from .models import Users


class UserGetUpdateSerializer(serializers.ModelSerializer[Users]):
    class Meta:
        model = Users
        exclude = ["password", "is_active", "is_staff", "is_admin", "last_login"]


class UserSerializer(serializers.ModelSerializer[Users]):
    class Meta:
        model = Users
        fields = "__all__"


class RegisterSerializer(
    serializers.ModelSerializer[Users]
):  # 타입 지정해줄때 django restframework stubs 도 깔려있어야 오류가 안남.
    password = serializers.CharField(write_only=True, min_length=5)

    def create(self, validated_data: dict[str, Any]) -> Users:
        password = validated_data.pop("password")
        user = Users.objects.create_user(password=password, **validated_data)
        return user

    class Meta:
        model = Users  # CustomUser를 사용한다면 변경
        fields = "__all__"
        # exclued = ["password"]

    # def create(self, validated_data):
    #     user = Users.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #
    #     )
    #     return user
