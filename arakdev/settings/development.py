from .base import *


DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ROOT_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "test@example.com"

STATIC_URL = "static/"
STATIC_ROOT = ROOT_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = ROOT_DIR / "media"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

