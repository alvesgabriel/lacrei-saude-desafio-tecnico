import typing

from rest_framework import permissions


class IsOwnerOrCreate(permissions.BasePermission):
    """
    Custom permission to only create object and other actions is for only owner
    """

    @typing.override
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True
        return obj.pk == request.user.pk
