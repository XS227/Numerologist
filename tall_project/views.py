from __future__ import annotations

import json

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import LiteCalculatorForm
from .navigation import STATIC_PAGES
from .number_profiles import PROFILES_EN, get_profile, meta_description
from .number_story import get_story_titles
from .related_articles import get_related_articles


def _canonical(request: HttpRequest) -> str:
    return request.build_absolute_uri(request.path)


def _webpage_schema(name: str, description: str, url: str) -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": name,
            "description": description,
            "url": url,
        }
    )

# English profiles, kept under the old name for existing imports; the page
# itself renders the visitor's language via number_profiles.get_profile().
NUMBER_INTERPRETATIONS = PROFILES_EN


# The calculation bug (flat letter/digit summing instead of per-name-part
# reduction) is fixed — see intake/forms.py IntakeForm._reduce_name /
# _life_path. Re-activated behind a 3-digit access code (LiteCalculatorForm)
# while it's tried out with a small group before a full public launch.
CALCULATOR_PAUSED = False


def home(request: HttpRequest) -> HttpResponse:
    from articles.models import Article
    from articles.thumbnails import get_thumbnail

    form = LiteCalculatorForm(request.POST or None)
    result = None
    if not CALCULATOR_PAUSED and request.method == "POST" and form.is_valid():
        result = form.calculate()
    latest_articles = list(Article.objects.all()[:3])
    for article in latest_articles:
        article.thumb = get_thumbnail(article.slug, article.title)
    context = {
        "form": form,
        "result": result,
        "calculator_paused": CALCULATOR_PAUSED,
        "latest_articles": latest_articles,
    }
    return render(request, "pages/home.html", context)


def number_detail(request: HttpRequest, number: int) -> HttpResponse:
    language = getattr(request, "LANGUAGE_CODE", "en")
    try:
        profile = get_profile(number, language)
    except KeyError as exc:
        raise Http404 from exc

    canonical_url = _canonical(request)
    description = meta_description(profile, language)
    faq = profile.get("faq", [])
    structured_data = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "inLanguage": {"nb": "nb-NO", "fa": "fa-IR"}.get(language, "en"),
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faq
            ],
        },
        ensure_ascii=False,
    ) if faq else _webpage_schema(profile["title"], description, canonical_url)
    sequence = [n for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33) if n in NUMBER_INTERPRETATIONS]
    position = sequence.index(number) if number in sequence else None
    prev_number = sequence[position - 1] if position else None
    next_number = sequence[position + 1] if position is not None and position + 1 < len(sequence) else None
    context = {
        "number": number,
        "profile": profile,
        "meta_description": description,
        "canonical_url": canonical_url,
        "structured_data": structured_data,
        "prev_number": prev_number,
        "next_number": next_number,
        "story": get_story_titles(number, language),
        "page_title": profile["title"],
        "related_articles": get_related_articles(number, limit=6),
        "related_articles_mid": get_related_articles(number, limit=3),
        "related_copy": ({
            "nb": {
                "eyebrow": "Relaterte artikler",
                "mid_title": f"Les videre om tallet {number}",
                "mid_text": "Fordyp deg i artikler som utforsker de samme mønstrene, menneskene og symbolene.",
                "more_title": f"Flere perspektiver på {number}",
                "open": "Åpne artikkel",
            },
            "fa": {
                "eyebrow": "مقاله‌های مرتبط",
                "mid_title": f"مطالعه بیشتر درباره عدد {number}",
                "mid_text": "مقاله‌هایی را بخوانید که الگوها، شخصیت‌ها و نمادهای مرتبط را عمیق‌تر بررسی می‌کنند.",
                "more_title": f"دیدگاه‌های بیشتر درباره {number}",
                "open": "باز کردن مقاله",
            },
        }.get(language, {
            "eyebrow": "Related articles",
            "mid_title": f"Read further about number {number}",
            "mid_text": "Explore articles that deepen the same patterns, people, and symbols.",
            "more_title": f"More perspectives on {number}",
            "open": "Open article",
        })),
    }
    return render(request, "pages/number-detail.html", context)


# These static pages are *about* the calculator (their whole copy promises
# "learn how to calculate X") but never actually embedded one — visitors
# hit a dead end. Both draw from the same LiteCalculatorForm/four-number
# result the homepage tool produces, so give them the real, working thing
# instead of just describing it.
SLUGS_WITH_CALCULATOR = {
    "compute-name-vowel-consonant",
    "compute-destiny-number",
    "compute-life-path-number",
    "letter-value-chart",
    "calculation-methods-overview",
}

# Which of the widget's four results to visually emphasise on a given
# landing page, since one shared form produces all four at once — a page
# built around a single number still shows the real, honest shared widget,
# just with its own number picked out.
SLUG_CALCULATOR_HIGHLIGHT = {
    "compute-life-path-number": ["life_path"],
    "compute-destiny-number": ["expression"],
    "compute-name-vowel-consonant": ["soul_urge", "personality"],
}


# Pages that moved; old links and search results keep working (301).
MOVED_PAGES = {
    "about-the-firm": "/ase-steinsland/",
    "quranian-numerology": "/articles/tallene-i-koranen/",
    "quranic-analysis": "/articles/tallene-i-koranen/",
}


def static_page(request: HttpRequest, slug: str) -> HttpResponse:
    if slug in MOVED_PAGES:
        return redirect(MOVED_PAGES[slug], permanent=True)
    try:
        page = STATIC_PAGES[slug]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise Http404 from exc
    canonical_url = page.canonical_override or _canonical(request)
    context = {
        "page": page,
        "meta_description": str(page.description),
        "canonical_url": canonical_url,
        "structured_data": _webpage_schema(str(page.title), str(page.description), canonical_url),
        "noindex": page.noindex,
        "page_title": str(page.title),
    }
    if slug == "discover-numerology":
        from .journey import journey_content
        context["journey"] = journey_content(getattr(request, "LANGUAGE_CODE", "en"))
    from .learning import ase_content, learning_content

    language = getattr(request, "LANGUAGE_CODE", "en")
    if slug in {
        "discover-numerology", "general-interpretation", "letter-value-chart",
        "compute-destiny-number", "compute-life-path-number", "pythagoras-legacy",
        "compute-name-vowel-consonant", "calculation-methods-overview",
    }:
        context["ase"] = ase_content(language)
    if slug in {
        "general-interpretation", "letter-value-chart",
        "compute-destiny-number", "compute-life-path-number", "pythagoras-legacy",
        "compute-name-vowel-consonant", "calculation-methods-overview",
    }:
        context["lesson"] = learning_content(slug, language)
    if slug in SLUGS_WITH_CALCULATOR:
        form = LiteCalculatorForm(request.POST or None)
        result = None
        if not CALCULATOR_PAUSED and request.method == "POST" and form.is_valid():
            result = form.calculate()
        context["calculator_form"] = form
        context["calculator_result"] = result
        context["calculator_paused"] = CALCULATOR_PAUSED
        context["calculator_highlight"] = SLUG_CALCULATOR_HIGHLIGHT.get(slug, [])
    return render(request, page.template_name, context)
