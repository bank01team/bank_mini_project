from rest_framework import serializers
from .models import Users

class UserGetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude=['password',"is_active","is_staff","is_admin","last_login"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'