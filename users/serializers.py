from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from static.constants import Constant
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_id",
            "email",
            "password",
            "username",
            "is_active",
        )
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["user_id", "phone", "is_active"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)

        if password is not None:
            user.set_password(password)

        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only=True)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ("user_id", "email", "username", "password", "access")

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(Constant.INVALID_AUTH_CREDENTIALS)

        try:
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(Constant.INVALID_AUTH_CREDENTIALS)

        return {
            "user_id": user.user_id,
            "email": user.email,
            "username": user.username,
            "access": str(refresh.access_token),
        }
