from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        app_label = "accounts"
    
    email = models.EmailField(max_length=150, unique=True)
    image = models.ImageField(upload_to="profiles/images/", default="", blank=True, null=True)