from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView

from apps.account.constants import ADMIN_PERMISSION_DEFAULT
from apps.account.models import CompanyRole
from apps.account.serializers import (
    CompanySerializer,
)


class CompanyCreateView(CreateAPIView):
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        user = self.request.user

        if user.company:
            raise PermissionDenied("Permission denied")

        company = serializer.save()

        admin_role = CompanyRole.objects.create(
            company=company,
            name="Director",
            permissions=ADMIN_PERMISSION_DEFAULT,
            is_protected=True,
        )
        user.company = company
        user.company_role = admin_role
        user.save()
