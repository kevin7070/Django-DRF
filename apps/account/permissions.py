from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsCompanyManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, "company_role")
            and user.company_role
            and user.company_role.permissions.get("user", {}).get("manage", False)
        )


class IsSameCompanyObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if hasattr(obj, "company") and obj.company == request.user.company:
            return True
        return PermissionDenied("Permission denied")
