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
        "navn-og-numerologi",
        "massenes-visdom-og-gruppebevissthet",
    ),
    2: (
        "tall-og-kompatibilitet",
        "valentinsdagens-tall",
        "numerological-reflection-on-mahsa-amini-and-bita-azizi",
        "nikola-tesla-dekodet",
        "barn-og-navn",
        "navn-og-numerologi",
    ),
    3: (
        "elon-musk-numerologi-16-7",
        "navn-og-numerologi",
        "creative-research-practice-for-numerology",
        "solfeggio-universets-helbredende-lydfrekvenser",
        "luciadagen-13-lys-og-333",
        "universets-lyd-og-mantraet-om",
    ),
    4: (
        "tallet-4-skilpadden-og-haren",
        "de-fire-leveregler",
        "kortstokken-som-kalender-52-4-13-365",
        "sommersolverv-arets-lyseste-dogn",
        "hostjevndogn-tid-for-takknemlighet",
        "barn-og-navn",
    ),
    5: (
        "amy-winehouse-og-tallet-14",
        "tina-turner-41-5",
        "valentinsdagens-tall",
        "rune-spadom-avdekk-underbevissthetens-visdom",
        "primstaven-vaerspadommer-for-den-forste-vinterdagen",
        "tall-og-kompatibilitet",
    ),
    6: (
        "marion-dampier-jeans-33",
        "master-number-33",
        "tallene-i-koranen",
        "barn-og-navn",
        "valentinsdagens-tall",
        "mirakel-historier-og-tall",
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
        "massenes-visdom-og-gruppebevissthet",
        "creative-research-practice-for-numerology",
    ),
    9: (
        "tallet-9-fibonacci-gylne-snitt",
        "de-9-innsikter-synkroniteter",
        "sissel-grana-tallene",
        "solfeggio-universets-helbredende-lydfrekvenser",
        "hva-avslorer-tallene-i-shahnameh",
        "mirakel-historier-og-tall",
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
        "creative-research-practice-for-numerology",
    ),
    33: (
        "master-number-33",
        "marion-dampier-jeans-33",
        "sissel-grana-tallene",
        "mirakel-historier-og-tall",
        "jesus-tall-888-og-11",
        "barn-og-navn",
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
