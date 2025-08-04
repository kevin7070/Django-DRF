from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from apps.account.models import CompanyRole
from apps.account.serializers import (
    CompanyRoleSerializer,
    UserSerializer,
)


class IsCompanyManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, "company_role")
            and user.company_role
            and user.company_role.permissions.get("user", {}).get("manage", False)
        )


class DirectorCompanyRoleViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyRoleSerializer
    permission_classes = [IsCompanyManager, permissions.IsAuthenticated]

    def get_queryset(self):
        return CompanyRole.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.company_role or not user.company_role.has_perm("user", "manage"):
            raise PermissionDenied("Permission denied")
        serializer.save(company=user.company)

    def perform_update(self, serializer):
        role = self.get_object()
        if role.company != self.request.user.company:
            raise PermissionDenied("Permission denied")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.company != self.request.user.company:
            raise PermissionDenied("Permission denied")
        if instance.is_protected:
            raise PermissionDenied("Permission denied")
        instance.delete()


User = get_user_model()


class DirectorUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsCompanyManager, permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company)

    def perform_update(self, serializer):
        target_user = self.get_object()
        actor = self.request.user
        if target_user.company != actor.company:
            raise PermissionDenied("Permission denied")
        serializer.save()
