from datetime import date

from django.test import SimpleTestCase

from members.future_report import build_future_report
from members.report_engine import calculate_profile


class FutureReportTests(SimpleTestCase):
    def setUp(self):
        self.data = {
            "birth_name": "Kari Elise Nordmann",
            "current_name": "Kari Nordmann",
            "birth_date": "1984-01-15",
            "address": "Storgata 8, Oslo",
            "phone": "+47 952 73 772",
        }
        self.profile = calculate_profile(self.data)

    def test_builds_real_24_month_timeline(self):
        report = build_future_report(
            self.data,
            self.profile,
            language="no",
            start=date(2026, 9, 1),
        )
        self.assertEqual(len(report["timeline"]), 24)
        self.assertEqual((report["timeline"][0]["year"], report["timeline"][0]["month"]), (2026, 9))
        self.assertEqual((report["timeline"][-1]["year"], report["timeline"][-1]["month"]), (2028, 8))
        self.assertEqual([item["year"] for item in report["years"]], [2026, 2027, 2028])

    def test_months_combine_year_essence_and_transits(self):
        report = build_future_report(
            self.data,
            self.profile,
            language="no",
            start=date(2026, 9, 1),
        )
        first = report["timeline"][0]
        self.assertIn("personal_year", first)
        self.assertIn("personal_month", first)
        self.assertIn("essence", first)
        self.assertTrue(first["body"])
        self.assertTrue(all("role" in item for item in first["transits"]))

    def test_all_site_languages_are_supported(self):
        for language in ("no", "en", "fa"):
            with self.subTest(language=language):
                report = build_future_report(
                    self.data,
                    self.profile,
                    language=language,
                    start=date(2026, 9, 1),
                )
                self.assertEqual(len(report["timeline"]), 24)
                self.assertTrue(report["method_intro"])
                self.assertTrue(report["synthesis"])
