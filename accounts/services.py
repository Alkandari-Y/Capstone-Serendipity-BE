from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework import exceptions

User = get_user_model()

def create_user(user_data):
    password = user_data.pop("password")
    try:
        user = User.objects.create(**user_data)
    except IntegrityError as e:
        error_type = str(e).split(".")[-1]
        raise serializers.ValidationError({error_type: [
        f"A user with that {error_type} already exists!"
    ]})
    
    user.set_password(password)
    user.save()
    return user


def get_user_auth(attr):
    user = None

    if "@" in attr:
        user = User.objects.filter(Q(email__iexact=attr)).first()
    else:
        user = User.objects.filter(Q(username__iexact=attr)).first()

    if user is None:
        raise exceptions.AuthenticationFailed(
            detail="Invalid username or email!")
    
    return user

def validate_auth_user_password(user, password):
    if user.check_password(password):
        return user
    else:
        raise exceptions.AuthenticationFailed(
            detail="Invalid password!")
