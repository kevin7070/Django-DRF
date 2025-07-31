from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser


class PrivateSpectacularAPIView(SpectacularAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]


class PrivateSpectacularSwaggerView(SpectacularSwaggerView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]


urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("product/", include("api.v1.product.urls")),
    # API documentation for development
    path("schema/", PrivateSpectacularAPIView.as_view()),
    path("docs/", PrivateSpectacularSwaggerView.as_view(url_name="schema")),
]
