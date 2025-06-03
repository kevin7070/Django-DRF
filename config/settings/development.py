import os
from datetime import timedelta

from .base import *  # noqa: F403

DEBUG = True

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Django serve from IPs or domains
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
]

# Third-party apps
INSTALLED_APPS += [  # noqa: F405
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "guardian",
    "dj_rest_auth",
]

# apps
INSTALLED_APPS += [
    "accounts",
    "api",
]


# django-cors-headers
common_index = MIDDLEWARE.index("django.middleware.common.CommonMiddleware")  # noqa: F405
MIDDLEWARE.insert(common_index, "corsheaders.middleware.CorsMiddleware")  # noqa: F405

FRONTEND_DOMAINS = [
    domain.strip()
    for domain in os.getenv("FRONTEND_DOMAINS", "http://localhost:3000").split(",")
]
CORS_ALLOWED_ORIGINS = FRONTEND_DOMAINS  # Allow JS fetch from another origin
CSRF_TRUSTED_ORIGINS = FRONTEND_DOMAINS  # Allow CSRF-protected form submission or fetch


# Django REST framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",  # cookie-based
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # token-based
    ],
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}


# Django Guardian
AUTHENTICATION_BACKENDS = (
    "accounts.auth.UsernameOrEmailBackend",
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)


# django-rest-auth
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "jwt-auth",
}

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "accounts.serializers.CustomUserSerializer",
}


# Simple JWT
SIMPLE_JWT = {
    "AUTH_COOKIE": "jwt-auth",
    "AUTH_HEADER_TYPES": ("JWT",),
    "SIGNING_KEY": os.getenv("JWT_SIGNING_KEY"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # Add other options as needed
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}


# Templates
TEMPLATES = [  # noqa: F811
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "")],  # noqa: F405
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Tell Django to use my custom User model
AUTH_USER_MODEL = "accounts.User"


# PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "default_db_name"),
        "USER": os.getenv("POSTGRES_USER", "default_username"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "default_mypassword"),
        "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
