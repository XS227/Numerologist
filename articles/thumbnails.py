"""Article image paths and typographic fallback treatment."""

from __future__ import annotations

ARTICLE_THUMBNAILS: dict[str, dict[str, str]] = {
    "elon-musk-numerologi-16-7": {
        "big": "16/7",
        "small": "X = 6 · xAI = 16/7",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
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
    "ser-du-samme-tall": {
        "image": "article-ase-ser-du-samme-tall.webp",
        "big": "11:11",
        "small": "Synkronitet",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
    "navn-navnedeterminisme": {
        "image": "article-ase-navnedeterminisme.webp",
        "big": "NAVN",
        "small": "Identitet",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
    "barn-og-navn": {
        "image": "article-ase-barn-og-navn.webp",
        "big": "NAVN",
        "small": "Barn & tall",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
    "tallet-4-skilpadden-og-haren": {
        "image": "article-ase-tallet-4-skilpadden-haren.webp",
        "big": "4",
        "small": "Stødig frem",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
    "11-11-enigmaet": {
        "image": "article-ase-11-11-enigmaet.webp",
        "big": "11:11",
        "small": "Mestertallet",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
    "mirakel-historier-og-tall": {
        "image": "article-ase-mirakelhistorier.webp",
        "big": "∞",
        "small": "Synkronitet",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
    "snasamannens-tall": {
        "image": "article-ase-snasamannen.webp",
        "big": "11·7",
        "small": "Joralf Gjerstad",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
    "gro-helen-torum-numerologi": {
        "image": "article-ase-gro-helen-torum.webp",
        "big": "11·22",
        "small": "Mestertall",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
    "anne-mette-rosting-tallene": {
        "image": "article-ase-anne-mette-rosting.webp",
        "big": "11",
        "small": "Muligheter",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
    "tall-og-kompatibilitet": {
        "image": "article-ase-kompatibilitet.webp",
        "big": "2",
        "small": "Kompatibilitet",
        "bg": "#0d2b2c",
        "fg": "#d5b678",
    },
}

_FALLBACK_BG = "#f0f8f3"
_FALLBACK_FG = "#2d8f60"


def get_thumbnail(slug: str, title: str) -> dict[str, str]:
    if slug in ARTICLE_THUMBNAILS:
        return ARTICLE_THUMBNAILS[slug]
    first_word = (title.split() or ["#"])[0].strip("«»\"'?.,").upper()[:8]
    return {"big": first_word or "#", "small": "", "bg": _FALLBACK_BG, "fg": _FALLBACK_FG}
