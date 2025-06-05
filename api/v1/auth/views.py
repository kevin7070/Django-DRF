from dj_rest_auth.views import UserDetailsView
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from api.v1.auth.serializers import CustomUserDetailsSerializer


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def set_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})


class MyUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer
