from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


def has_all_perms(role, module, actions):
    return all(role.has_perm(module, action) for action in actions)


class IsCompanyVerified(BasePermission):
    def has_permission(self, request, view):
        return request.user.company and request.user.company.is_verified


class IsCompanyManager(IsCompanyVerified):
    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(user, "company_role")
            and user.company_role
            and has_all_perms(user.company_role, "user", ["create", "update", "delete"])
        )


class IsSameCompanyObject(IsCompanyManager):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "company") and obj.company == request.user.company:
            return True
        return PermissionDenied("Permission denied")
