from __future__ import annotations

from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from tall_project.forms import LiteCalculatorForm


@override_settings(ALLOWED_HOSTS=["testserver", "localhost"])
class HomeAndStaticPageTests(SimpleTestCase):
    def test_lite_calculator_accepts_split_birth_date(self) -> None:
        form = LiteCalculatorForm(
            data={
                "full_name": "Ada Lovelace",
                "birth_day": "10",
                "birth_month": "12",
                "birth_year": "2000",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.calculate()["life_path"], 6)

    def test_lite_calculator_rejects_invalid_calendar_date(self) -> None:
        form = LiteCalculatorForm(
            data={
                "full_name": "Ada Lovelace",
                "birth_day": "31",
                "birth_month": "2",
                "birth_year": "2025",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("birth_day", form.errors)

    def test_projects_and_quran_pages_are_available(self) -> None:
        for slug in ["projects-lab", "arecibo-line", "quranian-numerology", "quranic-analysis"]:
            with self.subTest(slug=slug):
                response = self.client.get(reverse("static_page", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 200)

    def test_language_switch_endpoint_redirects_back(self) -> None:
        response = self.client.post(
            reverse("set_language"),
            data={"language": "fa", "next": reverse("home")},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("home"))
