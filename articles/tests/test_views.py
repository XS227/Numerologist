"""Tests for the article views module."""

from __future__ import annotations

from types import SimpleNamespace
from unittest import mock

from django.test import SimpleTestCase

from articles import views


class LoadAIAnalysisHookTests(SimpleTestCase):
    def test_returns_none_when_module_missing(self) -> None:
        """If the optional module is absent the hook should be ``None``."""

        with mock.patch("articles.views.find_spec", return_value=None):
            self.assertIsNone(views._load_ai_analysis_hook())

    def test_returns_callable_when_module_available(self) -> None:
        """When the module exists, the callable from the module is returned."""

        fake_callable = object()
        with mock.patch("articles.views.find_spec", return_value=object()), mock.patch(
            "articles.views.import_module",
            return_value=SimpleNamespace(ai_analyze_content=fake_callable),
        ):
            self.assertIs(views._load_ai_analysis_hook(), fake_callable)

    def test_returns_none_when_import_raises(self) -> None:
        """Import errors should not bubble up from the optional hook loader."""

        with mock.patch("articles.views.find_spec", return_value=object()), mock.patch(
            "articles.views.import_module", side_effect=ImportError
        ):
            self.assertIsNone(views._load_ai_analysis_hook())
