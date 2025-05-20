from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})


def get_cookie_domain(request):
    host = request.get_host()
    domain = host.split(":")[0].lower()
    if domain in ["localhost", "127.0.0.1"]:
        return (
            None  # Cookie does not need to specify domain, avoiding cross-port errors
        )
    return domain


# @method_decorator(csrf_exempt, name="dispatch")
class CustomTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"detail": "Invalid username or password"}, status=401)

        res = Response({"success": "Login successfully"}, status=200)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        domain = get_cookie_domain(request)
        res.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            # max_age=10 * 60,  # 10 minutes
            max_age=10,  # 10 seconds for test
            domain=domain,
            path="/",
        )
        res.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            # max_age=7 * 24 * 60 * 60,  # 7 days
            max_age=20,  # 20 seconds for test
            domain=domain,
            path="/",
        )
        print("Access Token:", str(refresh.access_token))
        return res


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request):
        raw_refresh_token = request.COOKIES.get("refresh_token")
        if not raw_refresh_token:
            return Response({"detail": "Refresh token missing"}, status=401)

        try:
            refresh = RefreshToken(raw_refresh_token)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
        except Exception as e:
            return Response(
                {"detail": "Invalid refresh token", "error": str(e)}, status=401
            )

        domain = get_cookie_domain(request)

        res = Response({"success": "Refresh token successfully"}, status=200)
        res.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            # max_age=10 * 60,  # 10 minutes
            max_age=10,  # 10 seconds for test
            domain=domain,
            path="/",
        )
        res.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            # max_age=7 * 24 * 60 * 60,  # 7 days
            max_age=20,  # 20 seconds for test
            domain=domain,
            path="/",
        )

        return res


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
            }
        )


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        raw_refresh_token = request.COOKIES.get("refresh_token")
        try:
            # Blacklist the current refresh token when logging out
            raw_token_obj = RefreshToken(raw_refresh_token)
            raw_token_obj.blacklist()
        except Exception:
            pass

        res = Response({"success": "Logout successfully"}, status=200)

        domain = get_cookie_domain(request)
        # Correctly delete access token cookie
        res.delete_cookie(
            key="access_token",
            path="/",
            domain=domain,
        )
        # Correctly delete refresh token cookie
        res.delete_cookie(
            key="refresh_token",
            path="/",
            domain=domain,
        )
        return res
