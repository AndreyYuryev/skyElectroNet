from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email


class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active == True
