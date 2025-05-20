# urls.py
from django.urls import include, path

from .views import (
    CustomTokenRefreshView,
    CustomTokenView,
    LogoutView,
    MeView,
    get_csrf_token,
)

urlpatterns = [
    path("get-csrf-token/", get_csrf_token, name="get_csrf_token"),
    path("token/", CustomTokenView.as_view(), name="custom_token_obtain"),
    path(
        "token/refresh/", CustomTokenRefreshView.as_view(), name="custom_token_refresh"
    ),
    path("me/", MeView.as_view(), name="me_view"),
    path("logout/", LogoutView.as_view(), name="logout_view"),
]

# Add dj-rest-auth
urlpatterns += [path("dj-rest-auth/", include("dj_rest_auth.urls"))]
