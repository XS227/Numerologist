import os
import sys
from importlib import import_module
from pathlib import Path


def _ensure_project_on_path() -> None:
    base_dir = Path(__file__).resolve().parent
    candidates = (base_dir, base_dir / "tall_project")

    for candidate in candidates:
        candidate_str = str(candidate)
        if candidate_str not in sys.path:
            sys.path.insert(0, candidate_str)


_ensure_project_on_path()

def _ensure_project_on_path() -> None:
    base_dir = Path(__file__).resolve().parent
    candidates = (base_dir, base_dir / "tall_project")

    for candidate in candidates:
        candidate_str = str(candidate)
        if candidate_str not in sys.path:
            sys.path.insert(0, candidate_str)


get_wsgi_application = import_module("django.core.wsgi").get_wsgi_application
_ensure_project_on_path()
from django.core.wsgi import get_wsgi_application


get_wsgi_application = import_module("django.core.wsgi").get_wsgi_application
def _ensure_project_on_path() -> None:
    base_dir = Path(__file__).resolve().parent
    if str(base_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))


_ensure_project_on_path()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tall_project.settings")

application = get_wsgi_application()
