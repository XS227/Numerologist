"""Settings for the Numerologist Django/Wagtail project."""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-change-me")
DEBUG = os.getenv("DEBUG", "False") == "True"

_default_allowed = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()]
ALLOWED_HOSTS = [
    "numerologist.setaei.com",
    "localhost",
    "127.0.0.1",
    *_default_allowed,
]

CSRF_TRUSTED_ORIGINS = ["https://numerologist.setaei.com"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "intake.apps.IntakeConfig",
    "wagtail",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.sites",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "modelcluster",
    "taggit",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "tall_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "tall_project" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "tall_project.context_processors.site_navigation",
            ],
        },
    }
]

WSGI_APPLICATION = "tall_project.wsgi.application"
ASGI_APPLICATION = "tall_project.asgi.application"

DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL.startswith("mysql://"):
    parsed = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username or "",
            "PASSWORD": parsed.password or "",
            "HOST": parsed.hostname or "localhost",
            "PORT": str(parsed.port or 3306),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
elif DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://"):
    parsed = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username or "",
            "PASSWORD": parsed.password or "",
            "HOST": parsed.hostname or "localhost",
            "PORT": str(parsed.port or 5432),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", _("English")),
    ("nb", _("Norwegian Bokmål")),
    ("fa", _("Persian")),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = BASE_DIR / "static_collected"
MEDIA_ROOT = BASE_DIR / "media"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

WAGTAIL_SITE_NAME = "Numerologist"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
