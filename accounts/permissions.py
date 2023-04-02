from rest_framework.permissions import BasePermission

class ProfileOwnerOnly(BasePermission):
    message = "You must be the the owner of this resource."

    def has_object_permission(self, request, view, obj):
        return obj == request.user