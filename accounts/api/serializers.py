from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'password')


class RegisterUserSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(max_length=128, required=True)

    def validate(self, attrs):
        if attrs['repeat_password'] != attrs['password']:
            raise serializers.ValidationError("Passwords does not match!")
        return attrs

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        token = Token.objects.create(user=user)

        return token

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'repeat_password')
