from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.v1.auth.views import set_csrf_token

urlpatterns = [
    # Nuxt/Web endpoints (cookie-based)
    path("nuxt/csrf/", set_csrf_token),
    path("nuxt/", include("dj_rest_auth.urls")),
    # Mobile endpoints (token-based)
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
