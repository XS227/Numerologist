"""Curated article relationships for number pages.

The connections are editorial rather than raw digit matching, so the number
pages surface genuinely relevant reading instead of accidental title hits.
"""

from __future__ import annotations

from articles.models import Article
from articles.thumbnails import get_thumbnail

RELATED_ARTICLE_SLUGS: dict[int, tuple[str, ...]] = {
    1: (
        "nikola-tesla-dekodet",
        "elon-musk-numerologi-16-7",
        "navn-navnedeterminisme",
        "creative-research-practice-for-numerology",
    ),
    2: (
        "tall-og-kompatibilitet",
        "valentinsdagens-tall",
        "numerological-reflection-on-mahsa-amini-and-bita-azizi",
        "nikola-tesla-dekodet",
        "barn-og-navn",
    ),
    3: (
        "elon-musk-numerologi-16-7",
        "navn-og-numerologi",
        "creative-research-practice-for-numerology",
        "solfeggio-universets-helbredende-lydfrekvenser",
    ),
    4: (
        "tallet-4-skilpadden-og-haren",
        "hostjevndogn-tid-for-takknemlighet",
        "barn-og-navn",
        "navn-navnedeterminisme",
    ),
    5: (
        "valentinsdagens-tall",
        "rune-spadom-avdekk-underbevissthetens-visdom",
        "primstaven-vaerspadommer-for-den-forste-vinterdagen",
        "tall-og-kompatibilitet",
    ),
    6: (
        "marion-dampier-jeans-33",
        "master-number-33",
        "tallene-i-koranen",
        "valentinsdagens-tall",
    ),
    7: (
        "nikola-tesla-dekodet",
        "sissel-grana-tallene",
        "snasamannens-tall",
        "tallene-i-bibelen",
        "tallene-i-koranen",
        "22-7-riktig-beregning-av-pi",
    ),
    8: (
        "elon-musk-numerologi-16-7",
        "tallene-i-koranen",
        "tall-og-kompatibilitet",
        "hva-avslorer-tallene-i-shahnameh",
    ),
    9: (
        "tallet-9-fibonacci-gylne-snitt",
        "sissel-grana-tallene",
        "solfeggio-universets-helbredende-lydfrekvenser",
        "hva-avslorer-tallene-i-shahnameh",
    ),
    11: (
        "11-11-enigmaet",
        "ser-du-samme-tall",
        "gro-helen-torum-numerologi",
        "anne-mette-rosting-tallene",
        "snasamannens-tall",
        "nikola-tesla-dekodet",
        "profeten-muhammads-tall",
        "jesus-tall-888-og-11",
    ),
    22: (
        "gro-helen-torum-numerologi",
        "22-7-riktig-beregning-av-pi",
        "11-11-enigmaet",
        "ser-du-samme-tall",
        "hva-avslorer-tallene-i-shahnameh",
    ),
    33: (
        "master-number-33",
        "marion-dampier-jeans-33",
        "sissel-grana-tallene",
        "mirakel-historier-og-tall",
        "jesus-tall-888-og-11",
    ),
}


def get_related_articles(number: int, limit: int = 6) -> list[Article]:
    slugs = RELATED_ARTICLE_SLUGS.get(number, ())[:limit]
    if not slugs:
        return []
    by_slug = Article.objects.in_bulk(slugs, field_name="slug")
    result: list[Article] = []
    for slug in slugs:
        article = by_slug.get(slug)
        if not article:
            continue
        article.thumb = get_thumbnail(article.slug, article.title)
        result.append(article)
    return result
