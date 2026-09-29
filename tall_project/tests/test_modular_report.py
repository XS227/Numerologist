from datetime import date

from django.test import SimpleTestCase

from members.future_report import build_future_report
from members.modular_report import build_modular_report
from members.report_engine import calculate_profile


class ModularReportTests(SimpleTestCase):
    def setUp(self):
        self.data = {
            "birth_name": "Kari Elise Nordmann",
            "current_name": "Kari Nordmann",
            "birth_date": "1984-01-15",
            "address": "Storgata 8, Oslo",
            "phone": "+47 952 73 772",
        }
        self.profile = calculate_profile(self.data)

    def test_report_engine_exposes_add_on_calculations(self):
        self.assertIn("current_vowel", self.profile)
        self.assertIn("cornerstone", self.profile)
        self.assertIn("life_name_bridge", self.profile)
        self.assertIn("vowel_consonant_bridge", self.profile)
        self.assertIn("balance", self.profile)
        self.assertIn("karmic_debts", self.profile)
        self.assertIn("karmic_lessons", self.profile)

    def test_only_selected_modules_are_returned(self):
        config = {
            "modules": ["cornerstone", "pinnacles", "essence"],
            "future_months": 3,
            "human_review": False,
        }
        report = build_modular_report(self.data, self.profile, config, language="no")
        self.assertEqual([row["id"] for row in report["modules"]], config["modules"])
        self.assertEqual(len(report["core"]), 5)
        self.assertEqual(report["future_months"], 3)

    def test_selected_future_length_controls_timeline(self):
        config = {"modules": [], "future_months": 3, "human_review": False}
        report = build_future_report(
            self.data,
            self.profile,
            language="no",
            start=date(2026, 9, 1),
            months=config["future_months"],
        )
        self.assertEqual(len(report["timeline"]), 3)

    def test_partner_module_builds_second_core_profile(self):
        config = {
            "modules": ["partner"],
            "future_months": 0,
            "human_review": False,
            "partner_name": "Ola Nordmann",
            "partner_date": "1982-06-08",
        }
        report = build_modular_report(self.data, self.profile, config, language="no")
        self.assertIsNotNone(report["partner_profile"])
        self.assertEqual(report["partner_name"], "Ola Nordmann")
