"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

env = os.getenv("DJANGO_ENVIRONMENT", "development")

if env == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")


application = get_wsgi_application()

print(f"[wsgi.py] DJANGO_ENVIRONMENT = {env}")
print(f"[wsgi.py] DJANGO_SETTINGS_MODULE = {os.environ['DJANGO_SETTINGS_MODULE']}")
