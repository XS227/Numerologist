from __future__ import annotations

import json
import re
from importlib import import_module
from importlib.util import find_spec
from typing import Callable, Optional

from django.utils.html import strip_tags
from django.views.generic import DetailView, ListView

from .models import Article


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


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"

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
