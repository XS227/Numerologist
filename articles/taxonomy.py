"""Åse Steinsland archive taxonomy for the Numerologist article library.

The original Nummerologens Verden allows one article to belong to several
subject categories. Keep that many-to-many structure here even though the
Article database model itself remains intentionally small.
"""
from __future__ import annotations

CATEGORY_ORDER = [
    "Astronomiske ressurser", "Fraktaler og tall", "Hellig geometri",
    "Helse og tall", "Horoskop og prognoser", "Inspirasjon & selvhjelp",
    "Karmiske tall", "Kjente personers tall", "Kongelige og tall",
    "Kornsirkler", "Lyd og frekvenser", "Mestertall 11", "Mestertall 22",
    "Mestertall 33", "Numerologi og bedrifter", "Numerologi og navn",
    "PI 3,14 og 22/7", "Spesielle tall og datoer", "Statistikk",
    "Synkroniteter", "Tall og kjærlighet", "Tall-Horoskop", "Tallet 12",
    "Tallet 13", "Tallet 666", "Tallet 7", "Tallkrim",
]

ARTICLE_META = {
    "ser-du-samme-tall": {"original_date":"2026-07-22","categories":["Horoskop og prognoser","Inspirasjon & selvhjelp","Mestertall 11","Mestertall 22","Mestertall 33","Tall-Horoskop"]},
    "navn-navnedeterminisme": {"original_date":"2026-05-24","categories":["Numerologi og navn"]},
    "barn-og-navn": {"original_date":"2026-04-05","categories":["Inspirasjon & selvhjelp","Numerologi og navn"]},
    "tallet-4-skilpadden-og-haren": {"original_date":"2026-03-01","categories":["Inspirasjon & selvhjelp"]},
    "11-11-enigmaet": {"original_date":"2025-11-11","categories":["Mestertall 11","Mestertall 22","Mestertall 33"]},
    "mirakel-historier-og-tall": {"original_date":"2025-10-15","categories":["Helse og tall","Mestertall 11","Synkroniteter","Tallet 7","Tallkrim"]},
    "snasamannens-tall": {"original_date":"2025-09-30","categories":["Helse og tall","Kjente personers tall","Mestertall 11","Tallet 7"]},
    "gro-helen-torum-numerologi": {"original_date":"2025-07-21","categories":["Kjente personers tall","Mestertall 11","Mestertall 22","Numerologi og navn","Tallet 7"]},
    "anne-mette-rosting-tallene": {"original_date":"2025-05-15","categories":["Helse og tall","Inspirasjon & selvhjelp","Kjente personers tall","Mestertall 11","Numerologi og navn","Tallet 7"]},
    "tall-og-kompatibilitet": {"original_date":"2025-02-14","categories":["Tall og kjærlighet"]},
    "sissel-grana-tallene": {"original_date":"2024-08-20","categories":["Helse og tall","Kjente personers tall","Mestertall 11","Numerologi og navn","Tallet 7"]},
    "marion-dampier-jeans-33": {"original_date":"2024-07-13","categories":["Kjente personers tall","Mestertall 22","Mestertall 33"]},
    "valentinsdagens-tall": {"original_date":"2024-02-14","categories":["Spesielle tall og datoer","Tall og kjærlighet"]},
    "nikola-tesla-dekodet": {"original_date":"2023-05-10","categories":["Mestertall 11","Numerologi og navn","Tallet 7"]},
    "tallet-9-fibonacci-gylne-snitt": {"original_date":"2021-12-28","categories":["Hellig geometri"]},
    "hostjevndogn-tid-for-takknemlighet": {"original_date":"2026-09-22","categories":["Hellig geometri"]},
    "rune-spadom-avdekk-underbevissthetens-visdom": {"original_date":"2026-09-01","categories":["Horoskop og prognoser","Inspirasjon & selvhjelp"]},
    "sol-og-maneformorkelser-mellom-ar-1994-og-2030": {"original_date":"2026-07-27","categories":["Astronomiske ressurser","Spesielle tall og datoer","Synkroniteter"]},
    "solfeggio-universets-helbredende-lydfrekvenser": {"original_date":"2026-06-23","categories":["Helse og tall","Lyd og frekvenser"]},
    "primstaven-vaerspadommer-for-den-forste-vinterdagen": {"original_date":"2025-10-25","categories":["Inspirasjon & selvhjelp"]},
}

def meta_for(slug: str) -> dict:
    return ARTICLE_META.get(slug, {"original_date": "", "categories": []})

def slugs_for_category(category: str) -> list[str]:
    return [slug for slug, meta in ARTICLE_META.items() if category in meta["categories"]]

def active_categories() -> list[str]:
    used = {cat for meta in ARTICLE_META.values() for cat in meta["categories"]}
    return [cat for cat in CATEGORY_ORDER if cat in used]

def attach_meta(article) -> None:
    meta = meta_for(article.slug)
    article.ase_original_date = meta.get("original_date", "")
    article.categories = meta.get("categories", [])
    article.is_ase_archive = article.slug in ARTICLE_META

