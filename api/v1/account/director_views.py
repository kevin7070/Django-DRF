from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from apps.account.models import CompanyRole
from apps.account.permissions import IsCompanyManager, IsSameCompanyObject
from apps.account.serializers import (
    CompanyRoleSerializer,
    UserSerializer,
)


class DirectorCompanyRoleViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyRoleSerializer
    permission_classes = [
        IsAuthenticated,
        IsCompanyManager,
        IsSameCompanyObject,
    ]

    def get_queryset(self):
        return CompanyRole.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        if instance.is_protected:
            raise PermissionDenied("Permission denied")
        instance.delete()


User = get_user_model()


class DirectorUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsCompanyManager,
        IsSameCompanyObject,
    ]

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company)

    def perform_update(self, serializer):
        serializer.save()
