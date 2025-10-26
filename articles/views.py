from __future__ import annotations

from importlib import import_module
from importlib.util import find_spec
from typing import Callable, Optional

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


class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"
    paginate_by = 10


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
        return context
