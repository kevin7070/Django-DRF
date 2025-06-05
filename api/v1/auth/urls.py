from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # login with cookie-based JWT
    path("nuxt/", include("dj_rest_auth.urls")),
    # * auth/nuxt/login/      > login with username/email + password
    # * auth/nuxt/user/       > get current user info
    # * auth/nuxt/logout/     > logout
    # login using Authorization header
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
