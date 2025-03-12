from rest_framework import permissions


class IsProfileOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission: 
    - Users can edit only their own profile.
    - Admins can edit all profiles.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff


class IsPostOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission:
    - Users can edit/delete only their own posts.
    - Admins can edit/delete all posts.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff
