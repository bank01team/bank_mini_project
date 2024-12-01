from rest_framework import serializers
from .models import Users  # 또는 CustomUser 모델을 import

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

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
