from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        admin = (request.user and request.user.is_authenticated and request.user.role == 'admin')
        return admin or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission only for moderator or admin to create or delete object.
    """

    message = "Access only for moderator or admin!"

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    message = "Changing someone else's content is not allowed!"

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
