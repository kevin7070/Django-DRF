# urls.py
from django.urls import include, path

# Add dj-rest-auth JWTCookieAuth
urlpatterns = [path("dj-rest-auth/", include("dj_rest_auth.urls"))]
