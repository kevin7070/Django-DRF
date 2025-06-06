from dj_rest_auth.views import LoginView, LogoutView
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def set_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})


class NuxtLoginView(LoginView):
    def get_response(self):
        original_res = super().get_response()

        user = self.user

        # Remove `access` and `refresh` from response data if they exist
        original_res.data.pop("access", None)
        original_res.data.pop("refresh", None)
        # Change user data
        original_res.data["user"] = {
            "pk": user.pk,
            "username": user.username,
            "email": user.email,
        }

        return original_res


class NuxtLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)

        # Delete cookies
        res.delete_cookie(
            settings.REST_AUTH.get("JWT_AUTH_COOKIE"),
            path="/",
        )
        res.delete_cookie(
            settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE"),
            path="/",
        )
        res.data = {"detail": "Logout successful"}

        return res
