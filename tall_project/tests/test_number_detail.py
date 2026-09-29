from __future__ import annotations

from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ALLOWED_HOSTS=["testserver", "localhost"])
class NumberDetailViewTests(TestCase):
    def test_number_detail_page_renders_for_single_digits(self) -> None:
        response = self.client.get(reverse("number_detail", kwargs={"number": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Number 1")

    def test_number_detail_page_renders_for_master_numbers(self) -> None:
        response = self.client.get(reverse("number_detail", kwargs={"number": 22}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Master Number 22")

    def test_all_number_pages_use_editorial_template(self) -> None:
        for number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33):
            with self.subTest(number=number):
                response = self.client.get(reverse("number_detail", kwargs={"number": number}))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'class="n-editorial-hero"')
                self.assertContains(response, 'class="n-editorial-overview"')
                self.assertContains(response, f"number-{number}-strengths-photo.webp")

