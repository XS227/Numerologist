from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
