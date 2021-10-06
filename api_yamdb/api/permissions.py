from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission only for moderator or admin to create or delete object.
    """

    message = "Access only for moderator or admin!"

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)
