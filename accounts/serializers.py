from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers

from accounts import services
from accounts.utils import create_token

User = get_user_model()


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "image"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "image"]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        password = data.pop("password")
        username = data.pop("username")

        auth_user = services.validate_auth_user_password(
            services.get_user_auth(username), password
        )
        token = create_token(auth_user)
        return token


class UserCreateSerializer(serializers.Serializer):
    # Required Fields
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    # # Optional Fields
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    image = serializers.ImageField(allow_empty_file=True, required=False)

    # Returned Fields
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate_password_confirm(self, confirm_password):
        if confirm_password != self.initial_data.get("password"):  # type: ignore
            raise serializers.ValidationError("Passwords must match")
        return confirm_password

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def validate(self, data):
        data.pop("password_confirm")
        return data

    def create(self, validated_data):
        user = services.create_user(validated_data)
        token = create_token(user)
        return token
