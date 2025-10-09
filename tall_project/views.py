from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .navigation import STATIC_PAGES

from .forms import LiteCalculatorForm


def home(request: HttpRequest) -> HttpResponse:
    form = LiteCalculatorForm(request.POST or None)
    result = None
    if request.method == "POST" and form.is_valid():
        result = form.calculate()
    context = {
        "form": form,
        "result": result,
    }
    return render(request, "pages/home.html", context)


def static_page(request: HttpRequest, slug: str) -> HttpResponse:
    try:
        page = STATIC_PAGES[slug]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise Http404 from exc
    context = {
        "page": page,
    }
    return render(request, page.template_name, context)
