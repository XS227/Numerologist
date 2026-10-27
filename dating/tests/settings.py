"""Isolated in-memory settings. Never loads a server .env or production DB."""
from pathlib import Path
SECRET_KEY = "dating-tests-only-not-a-production-secret"
DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
ROOT_URLCONF = "dating.tests.urls"
INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes",
                  "django.contrib.sessions", "dating.apps.DatingConfig"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
TIME_ZONE = "Europe/Oslo"
LANGUAGE_CODE = "nb"
MIDDLEWARE = ["django.contrib.sessions.middleware.SessionMiddleware",
              "django.middleware.csrf.CsrfViewMiddleware",
              "django.contrib.auth.middleware.AuthenticationMiddleware"]
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates",
              "DIRS": [str(Path(__file__).resolve().parents[2] / "tall_project" / "templates")],
              "APP_DIRS": True, "OPTIONS": {"context_processors": [
                  "django.template.context_processors.request",
                  "django.contrib.auth.context_processors.auth"]}}]
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EARLY_PREVIEW_ENABLED = True
EARLY_PREVIEW_CODE = "227"
