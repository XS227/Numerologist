from __future__ import annotations

from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .constants import INTAKE_EXPLANATIONS
from .forms import IntakeForm


def intake_view(request: HttpRequest) -> HttpResponse:
    result: Dict[str, Any] | None = None
    if request.method == "POST":
        form = IntakeForm(request.POST)
        if form.is_valid():
            profile = form.numerology_profile()
            numbers = [
                {
                    "key": key,
                    "label": key.replace("_", " ").title(),
                    "value": value,
                    "description": INTAKE_EXPLANATIONS.get(key, ""),
                }
                for key, value in profile.as_dict().items()
            ]
            result = {
                "numbers": numbers,
                "focus_area": form.cleaned_data.get("focus_area", ""),
                "notes": form.cleaned_data.get("notes", ""),
                "full_name": form.cleaned_data["full_name"],
                "email": form.cleaned_data["email"],
                "birth_date": form.cleaned_data["birth_date"],
            }
    else:
        form = IntakeForm()
    context = {"form": form, "result": result}
    return render(request, "intake/intake_form.html", context)
