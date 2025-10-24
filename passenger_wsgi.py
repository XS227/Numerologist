"""WSGI entrypoint for Passenger deployments."""

import os
import sys
from importlib import import_module
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR / "tall_project"

for candidate in (BASE_DIR, PROJECT_DIR):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tall_project.settings")

get_wsgi_application = import_module("django.core.wsgi").get_wsgi_application
application = get_wsgi_application()

__all__ = ["application"]
