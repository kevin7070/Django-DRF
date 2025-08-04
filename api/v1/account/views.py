from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView

from apps.account.serializers import CompanySerializer, UserSerializer

User = get_user_model()


class CompanyCreateView(CreateAPIView):
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        if self.request.user.company:
            raise PermissionDenied("Permission denied")
        company = serializer.save()
        self.request.user.company = company
        self.request.user.save()


class IsCompanyManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, "company_role")
            and user.company_role
            and user.company_role.permissions.get("user", {}).get("manage", False)
        )


class UserViewSet(viewsets.ModelViewSet):
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
