from __future__ import annotations

from django.test import SimpleTestCase, override_settings
from django.urls import reverse


@override_settings(ALLOWED_HOSTS=["testserver", "localhost"])
class NumberDetailViewTests(SimpleTestCase):
    def test_number_detail_page_renders_for_single_digits(self) -> None:
        response = self.client.get(reverse("number_detail", kwargs={"number": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Number 1")

    def test_number_detail_page_renders_for_master_numbers(self) -> None:
        response = self.client.get(reverse("number_detail", kwargs={"number": 22}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Master Number 22")
