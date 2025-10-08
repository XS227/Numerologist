import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application


def _ensure_project_on_path() -> None:
    base_dir = Path(__file__).resolve().parent
    if str(base_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))


_ensure_project_on_path()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tall_project.settings")

application = get_wsgi_application()
