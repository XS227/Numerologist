from __future__ import annotations

from typing import Any, Dict

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .constants import INTAKE_EXPLANATIONS
from .forms import IntakeForm
from .profile_numbers import id_vibration, name_vibration

# Short, public-safe one-liners per vibration — consistent with the
# interpretations already used across articles/master-number-33 and
# articles/navn-og-numerologi, so a cross-project caller (e.g. Shahnameh)
# doesn't need its own copy of this text.
VIBRATION_MEANINGS = {
    1: "nybegynnelser, initiativ, viljekraft",
    2: "samarbeid, balanse, diplomati",
    3: "kreativitet, glede, kommunikasjon",
    4: "stabilitet, struktur, byggeren",
    5: "frihet, forandring, eventyrlyst",
    6: "harmoni, ansvar, omsorg",
    7: "innsikt, analyse, åndelig søken",
    8: "makt, ambisjon, materiell manifestasjon",
    9: "fullendelse, medmenneskelighet, visdom",
    11: "mesternummer — intuisjon og innsikt",
    22: "mesternummer — mesterbyggeren",
    33: "mesternummer — den kosmiske læreren",
}


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


@require_GET
def profile_numbers_api(request: HttpRequest) -> JsonResponse:
    """Lightweight numerology numbers for external apps (Shahnameh, ReaLink)
    that only have an ID and/or a name on file — no birth date required.
    Public, read-only, no data stored. See intake/profile_numbers.py.

    GET /api/numbers/profile/?id=<telegram_id or device_id>&name=<full name>
    At least one of id/name must be given.
    """
    raw_id = request.GET.get("id", "").strip()
    raw_name = request.GET.get("name", "").strip()

    if not raw_id and not raw_name:
        response = JsonResponse({"ok": False, "error": "id_or_name_required"}, status=400)
    else:
        numbers = {}
        if raw_id:
            v = id_vibration(raw_id)
            numbers["id_number"] = {"value": v, "meaning": VIBRATION_MEANINGS.get(v, "")}
        if raw_name:
            v = name_vibration(raw_name)
            numbers["name_number"] = {"value": v, "meaning": VIBRATION_MEANINGS.get(v, "")}
        response = JsonResponse({
            "ok": True,
            "numbers": numbers,
            "learn_more_url": "https://numerologist.setai.no/articles/",
        })

    response["Access-Control-Allow-Origin"] = "*"
    return response
