import os

from .base import *  # noqa: F403

DEBUG = True

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# django-cors-headers
common_index = MIDDLEWARE.index("django.middleware.common.CommonMiddleware")  # noqa: F405
MIDDLEWARE.insert(common_index, "corsheaders.middleware.CorsMiddleware")  # noqa: F405

FRONTEND_DOMAINS = [
    domain.strip()
    for domain in os.getenv("FRONTEND_DOMAINS", "http://localhost:3000").split(",")
]
CORS_ALLOWED_ORIGINS = FRONTEND_DOMAINS  # Allow JS fetch from another origin
CSRF_TRUSTED_ORIGINS = FRONTEND_DOMAINS  # Allow CSRF-protected form submission or fetch
