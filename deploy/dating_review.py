"""Render the existing dating app for a stateless SETAEI review.

Uses the same Django views, forms, templates and member-report engine.
PHP owns preview access and CSRF. No accounts or database are opened here.
"""
import json
import os
import secrets
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from django.conf import settings
settings.configure(
    SECRET_KEY=secrets.token_urlsafe(48),
    DEBUG=False,
    ALLOWED_HOSTS=["setai.no", "testserver"],
    INSTALLED_APPS=["django.contrib.auth", "django.contrib.contenttypes", "dating.apps.DatingConfig"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    USE_TZ=True,
    TIME_ZONE="Europe/Oslo",
    LANGUAGE_CODE="nb",
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {"context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth"]}}],
)
import django
django.setup()
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.utils import translation
from dating.copy import COPY
from dating.forms import ProfileForm
from dating.views import experiment, response, decorate_form

NOTICES = {
    "no": ("FORHÅNDSVISNING", "Test dine tall og sammenlign to personer. Registrering og ekte datingprofiler er ikke aktivert ennå."),
    "en": ("PREVIEW", "Try your numbers and compare two people. Registration and real dating profiles are not enabled yet."),
    "fa": ("پیش‌نمایش", "عددهای خودت را ببین و دو نفر را مقایسه کن. ثبت‌نام و پروفایل واقعی هنوز فعال نیست."),
}


def render_page(data):
    lang = data.get("lang", "no")
    if lang not in COPY:
        lang = "no"
    mode = "pair" if data.get("mode") == "pair" else "self"
    view = data.get("view", "")
    factory = RequestFactory()
    fields = data.get("fields")
    if fields is not None:
        allowed = {"you-full_name", "you-birth_date", "other-full_name", "other-birth_date"}
        fields = {key: str(value)[:150] for key, value in fields.items() if key in allowed}
        fields["mode"] = mode
        request = factory.post("/dating/?lang=" + lang, fields)
    else:
        request = factory.get("/dating/", {"lang": lang, "mode": mode})
    request.user = AnonymousUser()
    request.session = {}
    request.LANGUAGE_CODE = lang
    with translation.override("nb" if lang == "no" else lang):
        if view == "profile" and fields is None:
            result = response(request, page="profile",
                              profile_form=decorate_form(ProfileForm(), COPY[lang]),
                              has_profile=False)
        elif view == "matches" and fields is None:
            result = response(request, page="matches", results=[],
                              me=SimpleNamespace(is_visible=True))
        else:
            result = experiment(request)
    html = result.content.decode("utf-8")
    html = html.replace('href="/dating/profile/?lang=', 'href="/dating/?view=profile&amp;lang=')
    html = html.replace('href="/dating/matches/?lang=', 'href="/dating/?view=matches&amp;lang=')
    html = html.replace('href="/min-side/login/?next=/dating/profile/"',
                        'href="/dating/?view=profile&amp;lang=' + lang + '"')
    title, notice = NOTICES[lang]
    banner = ('<aside class="review-banner"><strong>' + title + '</strong><span>'
              + notice + '</span></aside>')
    html = html.replace("<main>", "<main>" + banner, 1)
    html = html.replace("</style>",
        ".review-banner{display:flex;gap:16px;align-items:start;margin:20px 48px 0;"
        "padding:12px 16px;border:1px solid #4b3b43;border-radius:10px;color:#b0a8b9;font-size:12px}"
        ".review-banner strong{color:#f8a77b;font-size:10px;letter-spacing:1px;white-space:nowrap}"
        "@media(max-width:640px){.review-banner{margin:16px 20px 0;display:block}"
        ".review-banner strong{display:block;margin-bottom:5px}}"
        "</style>", 1)
    if view == "profile":
        import re
        html = re.sub(r'<(input|select|button)(?=\s)', r'<\1 disabled', html)
    return html


if __name__ == "__main__":
    if sys.argv[1:] == ["--build"]:
        cache = Path("/var/cache/numerologist-dating-review")
        cache.mkdir(parents=True, exist_ok=True)
        for lang in COPY:
            for view in ("self", "pair", "profile", "matches"):
                page = render_page({"lang": lang, "mode": view,
                                    "view": view if view in {"profile", "matches"} else ""})
                (cache / (lang + "-" + view + ".html")).write_text(page, encoding="utf-8")
        print("Built 12 review pages.")
    else:
        raw = sys.stdin.read(8193)
        if len(raw) > 8192:
            raise ValueError("Input exceeds review limit")
        print(render_page(json.loads(raw)))
