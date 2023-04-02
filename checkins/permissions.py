from rest_framework.permissions import BasePermission


class RespondentOnly(BasePermission):
    message = "You must be the the owner of this resource."

    def has_object_permission(self, request, view, obj):
        return obj.checkin.user == request.user
