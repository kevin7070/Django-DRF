import os

from .base import *  # noqa: F403

DEBUG = False

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# django-cors-headers, insert before django.middleware.common
common_index = MIDDLEWARE.index("django.middleware.common.CommonMiddleware")  # noqa: F405
MIDDLEWARE.insert(common_index, "corsheaders.middleware.CorsMiddleware")  # noqa: F405

FRONTEND_DOMAINS = [
    domain.strip()
    for domain in os.getenv("FRONTEND_DOMAINS").split(",")
    if domain.strip()
]
CORS_ALLOWED_ORIGINS = FRONTEND_DOMAINS  # Allow JS fetch from another origin
CSRF_TRUSTED_ORIGINS = FRONTEND_DOMAINS  # Allow CSRF-protected form submission or fetch


# WhiteNoise, insert after django.middleware.security
security_index = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware")  # noqa: F405
MIDDLEWARE.insert(security_index + 1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405
