"""Root URL configuration for tall_project."""
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import include, path

from tall_project.views import home, static_page


def health_check(_request: HttpRequest) -> HttpResponse:
    return HttpResponse("OK")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("cms/", include("wagtail.admin.urls")),
    path("documents/", include("wagtail.documents.urls")),
    path("intake/", include("intake.urls", namespace="intake")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("healthz/", health_check, name="health_check"),
    path("", home, name="home"),
    path("<slug:slug>/", static_page, name="static_page"),
]
