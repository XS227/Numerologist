"""Article image paths and typographic fallback treatment."""

from __future__ import annotations

ARTICLE_THUMBNAILS: dict[str, dict[str, str]] = {
    "tallene-i-koranen": {
        "image": "article-tallene-i-koranen.webp",
        "big": "6·7·8",
        "small": "i Koranen",
        "bg": "#f3f0e8",
        "fg": "#102f31",
    },
    "profeten-muhammads-tall": {
        "image": "article-profeten-muhammads-tall.webp",
        "big": "11",
        "small": "Navnet Muhammad",
        "bg": "#123739",
        "fg": "#e2cba2",
    },
    "wow-signalet-og-arecibo-linjen": {
        "image": "wow-hero.webp",
        "big": "WOW",
        "small": "Signalet",
        "bg": "#092426",
        "fg": "#c6a775",
    },
    "hva-avslorer-tallene-i-shahnameh": {
        "image": "article-shahnameh.webp",
        "big": "TALL",
        "small": "i Shahnameh",
        "bg": "#fdf3e3",
        "fg": "#a5691d",
    },
    "navn-og-numerologi": {
        "image": "article-navn-numerologi.webp",
        "big": "NAVN",
        "small": "& numerologi",
        "bg": "#f9f4ff",
        "fg": "#7b56b1",
    },
    "master-number-33": {
        "image": "article-master-33.webp",
        "big": "33",
        "small": "Mesterlærer",
        "bg": "#f4f9ff",
        "fg": "#3a63a6",
    },
    "numerological-reflection-on-mahsa-amini-and-bita-azizi": {
        "image": "article-mahsa-bita.webp",
        "big": "2",
        "small": "Mahsa & Bita",
        "bg": "#f2fbf6",
        "fg": "#3f8f65",
    },
    "creative-research-practice-for-numerology": {
        "image": "article-creative-research.webp",
        "big": "LAB",
        "small": "Kreativ praksis",
        "bg": "#fdf1f5",
        "fg": "#b1467e",
    },
}

_FALLBACK_BG = "#f0f8f3"
_FALLBACK_FG = "#2d8f60"


def get_thumbnail(slug: str, title: str) -> dict[str, str]:
    if slug in ARTICLE_THUMBNAILS:
        return ARTICLE_THUMBNAILS[slug]
    first_word = (title.split() or ["#"])[0].strip("«»\"'?.,").upper()[:8]
    return {"big": first_word or "#", "small": "", "bg": _FALLBACK_BG, "fg": _FALLBACK_FG}
