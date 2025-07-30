from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.v1.auth.views import (
    CookieTokenRefreshView,
    LoginView,
    LogoutView,
    set_csrf_token,
)

urlpatterns = [
    # cookie-based
    path("csrf/", set_csrf_token),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/", CookieTokenRefreshView.as_view()),
    # token-based
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]
