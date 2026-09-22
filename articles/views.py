from __future__ import annotations

import json
import re
from importlib import import_module
from importlib.util import find_spec
from typing import Callable, Optional

from django.utils.html import strip_tags
from django.utils.text import slugify
from django.views.generic import DetailView, ListView

from .models import Article
from .thumbnails import get_thumbnail


def _load_ai_analysis_hook() -> Optional[Callable[[str], str]]:
    module_name = "some_module"
    if find_spec(module_name) is None:
        return None
    try:
        module = import_module(module_name)
    except ImportError:
        return None
    return getattr(module, "ai_analyze_content", None)


AI_ANALYZE_CONTENT = _load_ai_analysis_hook()


def _meta_description(html_content: str, limit: int = 160) -> str:
    text = re.sub(r"\s+", " ", strip_tags(html_content)).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0] + "…"


class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for article in context["articles"]:
            article.thumb = get_thumbnail(article.slug, article.title)
        canonical_url = self.request.build_absolute_uri(self.request.path)
        description = (
            "Articles and long-form writing on numerology, symbolism, and number "
            "meaning from Åse Steinsland's Numerologist studio."
        )
        context["meta_description"] = description
        context["canonical_url"] = canonical_url
        context["page_title"] = "Numerologist Articles"
        context["structured_data"] = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "CollectionPage",
                "name": "Numerologist Articles",
                "description": description,
                "url": canonical_url,
            }
        )
        return context


# Slugs that get a bespoke visual template instead of the generic prose
# layout (e.g. side-by-side comparison dashboards). The article text itself
# is never touched — only how it's framed.
CUSTOM_ARTICLE_TEMPLATES = {
    "numerological-reflection-on-mahsa-amini-and-bita-azizi": "articles/detail_mahsa_bita.html",
    "navn-og-numerologi": "articles/detail_navn_numerologi.html",
    "creative-research-practice-for-numerology": "articles/detail_creative_research.html",
    "master-number-33": "articles/detail_master33.html",
    "hva-avslorer-tallene-i-shahnameh": "articles/detail_shahnameh.html",
    "wow-signalet-og-arecibo-linjen": "articles/detail_wow_signal.html",
}

# Slugs that render via the illustrated "journey" system (tall_project/journey.py's
# pattern: hero + scroll-parallax chapters) instead of the chapter-reader — these
# skip the normal chapters/lead split entirely, the whole page IS the content.
JOURNEY_ARTICLE_SLUGS = {"wow-signalet-og-arecibo-linjen"}

# Per-chapter icon key + a verbatim pull-quote (a real sentence lifted
# straight from that chapter's own text, not new copy) so the long-form
# reading further down the page isn't one unbroken wall of prose. Order
# must match the article's actual <h2> order.
MAHSA_BITA_CHAPTERS_META = [
    (
        "intro",
        "Numerology here is a reflective lens, illuminating connections and "
        "spiritual themes within these two young women’s legacies.",
    ),
    (
        "profiles",
        "Mahsa’s outer impression (4) was grounded and unshowy; "
        "Bita’s (11) was quietly luminous.",
    ),
    (
        "abjad",
        "Mahsa symbolizing a moonlight of wisdom and Bita symbolizing an "
        "unmatched strength.",
    ),
    (
        "dates",
        "From initiation (1) and building (4) to introspection (7) and "
        "completion (9).",
    ),
    (
        "synchronicities",
        "Two lives – the victim and the driver – were forever altered, "
        "bound by that fateful moment.",
    ),
    (
        "place",
        "Tehran, a city that imposed restrictions which ultimately claimed "
        "Mahsa’s life, versus Asker, a place of relative freedom where Bita "
        "lost her life to a moment of youthful excess.",
    ),
    (
        "conclusion",
        "Even in chaos, there is cosmic order; even in grief, there is "
        "spiritual growth.",
    ),
]


# Per-slug chapter metadata (icon key + verbatim pull-quote per position).
# Only the Mahsa/Bita piece has curated quotes today; other articles just
# get the generic split (numbered badge, default icon, no quote) below.
CHAPTER_META_BY_SLUG = {
    "numerological-reflection-on-mahsa-amini-and-bita-azizi": MAHSA_BITA_CHAPTERS_META,
}


def _split_into_chapters(
    content: str, meta: list[tuple[str, str]] | None = None
) -> tuple[str, list[dict]]:
    """Split <h2>-delimited article HTML into (lead, chapters). ``lead`` is
    whatever precedes the first <h2> (often an opening paragraph) and must
    still be rendered — it's not a chapter itself. When ``meta`` (a list of
    (icon_key, verbatim_quote) tuples) is given, pairs each chapter with its
    entry by position; otherwise every chapter gets the generic default icon
    and no quote. Falls back gracefully if the article's structure ever
    changes and the counts stop lining up."""
    parts = re.split(r"<h2>(.*?)</h2>", content)
    lead = parts[0].strip()
    chapters = []
    # parts = [before-first-h2, title0, body0, title1, body1, ...]
    for i in range(1, len(parts), 2):
        title = parts[i]
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        index = (i - 1) // 2
        icon, quote = ("default", None)
        if meta and index < len(meta):
            icon, quote = meta[index]
        chapters.append(
            {
                "number": index + 1,
                "id": slugify(title, allow_unicode=True) or f"chapter-{index + 1}",
                "title": title,
                "body": body,
                "icon": icon,
                "quote": quote,
            }
        )
    return lead, chapters


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = "article"

    def get_template_names(self):
        return [CUSTOM_ARTICLE_TEMPLATES.get(self.object.slug, "articles/detail.html")]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content = self.object.content
        analysis = None
        if AI_ANALYZE_CONTENT is not None:
            try:
                analysis = AI_ANALYZE_CONTENT(content)
            except Exception:  # pragma: no cover - best effort integration
                analysis = None
        context["ai_analysis"] = analysis

        if self.object.slug in JOURNEY_ARTICLE_SLUGS:
            from .wow_journey import wow_journey_content

            context["journey"] = wow_journey_content(getattr(self.request, "LANGUAGE_CODE", "en"))
        else:
            # Only worth chaptering + a table of contents when there's enough
            # structure to justify it; short/heading-less pieces stay plain prose.
            meta = CHAPTER_META_BY_SLUG.get(self.object.slug)
            lead, chapters = _split_into_chapters(content, meta)
            if len(chapters) >= 2:
                context["chapters"] = chapters
                context["chapters_lead"] = lead

        canonical_url = self.request.build_absolute_uri(self.request.path)
        description = _meta_description(content)
        context["meta_description"] = description
        context["canonical_url"] = canonical_url
        context["page_title"] = self.object.title
        context["structured_data"] = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "BlogPosting",
                "headline": self.object.title,
                "description": description,
                "author": {"@type": "Person", "name": self.object.author},
                "datePublished": self.object.published.isoformat(),
                "url": canonical_url,
                "mainEntityOfPage": {"@type": "WebPage", "@id": canonical_url},
            }
        )
        return context
