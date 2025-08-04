from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


def has_all_perms(role, module, actions):
    return all(role.has_perm(module, action) for action in actions)


class IsCompanyManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, "company_role")
            and user.company_role
            and has_all_perms(user.company_role, "user", ["create", "update", "delete"])
        )


class IsSameCompanyObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if hasattr(obj, "company") and obj.company == request.user.company:
            return True
        return PermissionDenied("Permission denied")
