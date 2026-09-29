from __future__ import annotations

from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ALLOWED_HOSTS=["testserver", "localhost"])
class AseEditionTests(TestCase):
    def test_ase_edition_renders_complete_intake_and_reading_shell(self) -> None:
        response = self.client.get(reverse("static_page", kwargs={"slug": "ase-edition"}))
        self.assertEqual(response.status_code, 200)
        for field in (
            "birthFirst", "birthMiddle", "birthLast", "currentName", "birthDate",
            "analysisDate", "address", "phone", "partnerName", "partnerDate",
            "partnerContext",
        ):
            self.assertContains(response, f'name="{field}"')
        self.assertContains(response, 'data-reading')
        self.assertContains(response, 'data-ledger')
        self.assertContains(response, 'ase-edition.js')
        self.assertContains(response, 'ase-edition.css')

    def test_calculator_library_features_ase_edition(self) -> None:
        response = self.client.get(reverse("static_page", kwargs={"slug": "calculators"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("static_page", kwargs={"slug": "ase-edition"}))
        self.assertContains(response, "ÅSE EDITION")
