"""Custom template context processors for the Numerologist project."""

from __future__ import annotations

from typing import Dict, Iterable

from django.urls import reverse

from .navigation import NavigationItem, iter_navigation


def _serialise_item(item: NavigationItem) -> Dict[str, object]:
    return {
        "title": item.title,
        "slug": item.slug,
        "url": reverse("static_page", args=[item.slug]),
        "children": tuple(_serialise_item(child) for child in item.children),
    }


def site_navigation(_request) -> Dict[str, Iterable[dict]]:
    """Provide the global navigation structure to all templates."""

    return {
        "site_navigation": tuple(_serialise_item(item) for item in iter_navigation()),
    }
