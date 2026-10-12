"""Server-side preview access, shared by Django and nginx's auth subrequest."""
import secrets

from django.conf import settings
from django.core import signing
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

COOKIE = "nl_early_preview"
SALT = "numerologist.early-preview.v1"
MAX_AGE = 7 * 24 * 60 * 60


def enabled():
    return settings.EARLY_PREVIEW_ENABLED


def allowed(request):
    try:
        value = signing.loads(request.COOKIES.get(COOKIE, ""), salt=SALT, max_age=MAX_AGE)
        return value == settings.EARLY_PREVIEW_CODE
    except signing.BadSignature:
        return False


def private(response):
    response["X-Robots-Tag"] = "noindex, nofollow, noarchive"
    response["Cache-Control"] = "private, no-store, max-age=0"
    return response


def return_path(request):
    target = request.POST.get("next") or request.GET.get("next") or request.headers.get("X-Preview-Return", "/")
    # Only local relative paths; never bounce back into the gate itself.
    if (not target.startswith("/") or target.startswith("//")
            or not url_has_allowed_host_and_scheme(target, allowed_hosts=set())
            or target.split("?", 1)[0].startswith("/early-preview")):
        return "/"
    return target


@never_cache
@csrf_protect
def preview(request):
    target = return_path(request)
    if not enabled() or allowed(request):
        return private(HttpResponseRedirect(target))
    error = False
    if request.method == "POST":
        code = request.POST.get("preview_code", "").strip()
        if secrets.compare_digest(code, settings.EARLY_PREVIEW_CODE):
            response = HttpResponseRedirect(target)
            response.set_cookie(COOKIE, signing.dumps(code, salt=SALT), max_age=MAX_AGE,
                                secure=request.is_secure(), httponly=True, samesite="Lax", path="/")
            return private(response)
        error = True
    return private(render(request, "early_preview.html", {"next": target, "error": error}))


@never_cache
def preview_auth(request):
    return private(HttpResponse(status=204 if not enabled() or allowed(request) else 401))


class EarlyPreviewMiddleware:
    """Protect Django too, including direct requests to its upstream."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not enabled():
            return self.get_response(request)
        if request.path not in {"/early-preview/", "/early-preview/auth/", "/healthz/"} and not allowed(request):
            if request.method not in {"GET", "HEAD"}:
                return private(HttpResponse("Early preview code required", status=403))
            return private(render(request, "early_preview.html", {
                "next": request.get_full_path(), "error": False,
            }))
        return private(self.get_response(request))
