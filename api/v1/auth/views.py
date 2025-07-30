from dj_rest_auth.views import LoginView, LogoutView
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def set_csrf_token(request):
    return Response({"detail": "CSRF cookie set"}, status=status.HTTP_200_OK)


class LoginView(LoginView):
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


class LogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)

        # Delete cookies
        if settings.REST_AUTH.get("JWT_AUTH_COOKIE"):
            if res and hasattr(res, "delete_cookie"):
                res.delete_cookie(
                    settings.REST_AUTH.get("JWT_AUTH_COOKIE"),
                    path="/",
                )

        if settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE"):
            if res and hasattr(res, "delete_cookie"):
                res.delete_cookie(
                    settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE"),
                    path="/",
                )

        res.data = {"detail": "Logout successful"}

        return res


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE"))

        if refresh is None:
            return Response(
                {"detail": "Refresh token not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(data={"refresh": refresh})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Set new access token cookie
        res = Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)

        res.set_cookie(
            settings.REST_AUTH.get("JWT_AUTH_COOKIE"),
            serializer.validated_data["access"],
            max_age=60 * 10,  # 10 minutes
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )

        res.set_cookie(
            settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE"),
            serializer.validated_data["refresh"],
            max_age=60 * 60 * 24 * 7,  # 7 days
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )

        return res
