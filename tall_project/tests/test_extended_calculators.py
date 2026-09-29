from __future__ import annotations

from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ALLOWED_HOSTS=["testserver", "localhost"])
class ExtendedCalculatorPagesTests(TestCase):
    NEW_CALCULATORS = (
        "spiritual-transit-number",
        "essence-number",
        "pinnacle-cycles",
        "life-cycles",
        "maturity-number",
        "challenge-numbers",
        "lucky-number",
        "telephone-number",
        "partner-profile",
    )

    def test_new_calculators_render_as_interactive_tools(self) -> None:
        for slug in self.NEW_CALCULATORS:
            with self.subTest(slug=slug):
                response = self.client.get(reverse("static_page", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f'data-calculator="{slug}"')
                self.assertContains(response, 'data-calc-form')

    def test_calculator_catalog_links_new_tools(self) -> None:
        response = self.client.get(reverse("static_page", kwargs={"slug": "calculators"}))
        self.assertEqual(response.status_code, 200)
        for slug in self.NEW_CALCULATORS:
            self.assertContains(response, reverse("static_page", kwargs={"slug": slug}))
