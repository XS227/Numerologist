from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/home.html",
        {
            "features": [
                {
                    "title": "Client intake",
                    "description": "Capture personal details, goals, and numerology-ready birth data in minutes.",
                    "href": "/intake/",
                },
                {
                    "title": "Instant numerology core numbers",
                    "description": "Life path, expression, soul urge, personality, and maturity numbers are calculated on submit.",
                    "href": "/intake/",
                },
                {
                    "title": "Wagtail CMS",
                    "description": "Publish articles, host reports, and manage site content via a friendly editor experience.",
                    "href": "/cms/",
                },
            ],
        },
    )
