from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def set_csrf_token(request):
    token = get_token(request)
    print("[DEBUG] CSRF token sent:", token)
    return JsonResponse({"detail": "CSRF cookie set"})
