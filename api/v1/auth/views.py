from dj_rest_auth.views import LoginView, LogoutView
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
        original_res.data["user"] = {
            "pk": user.pk,
            "username": user.username,
            "email": user.email,
        }

        # Keep user infor only
        return original_res


class NuxtLogoutView(LogoutView):
    pass
