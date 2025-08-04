from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .director_views import (
    DirectorCompanyRoleViewSet,
    DirectorUserViewSet,
)
from .views import CompanyCreateView

router = DefaultRouter()
router.register("company/users", DirectorUserViewSet, basename="company-user")
router.register("company/roles", DirectorCompanyRoleViewSet, basename="company-role")

urlpatterns = [
    path("company/create/", CompanyCreateView.as_view(), name="company-create"),
    path("", include(router.urls)),
]
