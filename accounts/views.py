from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions

from accounts import serializers
from accounts import models
from accounts.permissions import ProfileOwnerOnly
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class LoginAPIView(TokenObtainPairView):
    serializer_class = serializers.UserLoginSerializer
    permission_classes = [permissions.AllowAny]

class ProfileByIdAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "profile_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [ProfileOwnerOnly()]
    
    def get_serializer_class(self):
        if self.request.method != "GET":
            return serializers.UserUpdateSerializer
        return serializers.UserBaseSerializer