from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CompanyCreateView, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = router.urls

urlpatterns += [
    path("company/create/", CompanyCreateView.as_view()),
]
