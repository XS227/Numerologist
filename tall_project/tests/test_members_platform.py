from __future__ import annotations

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from pathlib import Path
import sqlite3
import tempfile

from members.catalog import PACKAGE_CATALOG
from members.models import AcademyProgress


@override_settings(ALLOWED_HOSTS=["testserver", "localhost"])
class MembersPlatformTests(TestCase):
    def test_public_academy_and_level_one_render(self) -> None:
        response = self.client.get(reverse("members:academy"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Become a Numerologist")
        self.assertContains(response, "Tallene 1–9")

        level = self.client.get(reverse("members:academy_level", kwargs={"level": 1}))
        self.assertEqual(level.status_code, 200)
        self.assertContains(level, "LEKSE")

    def test_dashboard_requires_login(self) -> None:
        response = self.client.get(reverse("members:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/min-side/login/", response["Location"])

    def test_logged_in_user_gets_academy_progress(self) -> None:
        user = User.objects.create_user(username="member", email="member@example.com")
        self.client.force_login(user)
        response = self.client.get(reverse("members:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AcademyProgress.objects.filter(user=user).count(), 5)
        self.assertEqual(AcademyProgress.objects.get(user=user, level=1).status, "active")
        self.assertEqual(AcademyProgress.objects.get(user=user, level=2).status, "locked")

    def test_completing_level_unlocks_next(self) -> None:
        user = User.objects.create_user(username="student", email="student@example.com")
        self.client.force_login(user)
        self.client.get(reverse("members:dashboard"))
        response = self.client.post(
            reverse("members:academy_level", kwargs={"level": 1}),
            {"action": "complete"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(AcademyProgress.objects.get(user=user, level=1).status, "completed")
        self.assertEqual(AcademyProgress.objects.get(user=user, level=2).status, "active")

    def test_premium_resource_requires_login_and_unlocked_level(self) -> None:
        url = reverse("members:premium_resource", kwargs={"level": 1, "resource_slug": "case-1-9"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        user = User.objects.create_user(username="reader", email="reader@example.com")
        self.client.force_login(user)
        self.client.get(reverse("members:dashboard"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tall 1–9: praktiske case")

    def test_all_package_demos_render(self) -> None:
        for slug, package in PACKAGE_CATALOG.items():
            with self.subTest(slug=slug):
                response = self.client.get(reverse("members:report_demo", kwargs={"package_slug": slug}))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, package["title"])
                self.assertContains(response, "EKSEMPEL")

    @override_settings(
        VIPPS_LOGIN_ENABLED=True,
        VIPPS_LOGIN_CLIENT_ID="client",
        VIPPS_LOGIN_CLIENT_SECRET="secret",
        VIPPS_LOGIN_MSN="msn",
        VIPPS_LOGIN_BASE_URL="https://apitest.vipps.no",
    )
    def test_vipps_login_start_uses_oidc_authorize(self) -> None:
        response = self.client.get(reverse("members:vipps_start"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/access-management-1.0/access/oauth2/auth?", response["Location"])
        self.assertIn("scope=openid+name+phoneNumber+email", response["Location"])

    @override_settings(GOOGLE_CLIENT_ID="", GOOGLE_CLIENT_SECRET="")
    def test_google_login_gracefully_requires_credentials(self) -> None:
        response = self.client.get(reverse("members:google_start"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("members:login"))

    def test_paid_order_appears_on_dashboard_and_opens_report(self) -> None:
        user = User.objects.create_user(username="buyer", email="buyer@example.com")
        from members.models import MemberProfile
        MemberProfile.objects.create(user=user, display_name="Buyer", phone="95273772")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "data").mkdir()
            db = sqlite3.connect(base / "data" / "orders.db")
            db.executescript(
                """
                CREATE TABLE orders (
                  id TEXT PRIMARY KEY, package TEXT, price_ore INTEGER,
                  birth_name TEXT, current_name TEXT, birth_date TEXT, address TEXT,
                  phone TEXT, email TEXT, payment_status TEXT, analysis_status TEXT,
                  created_at TEXT, notes TEXT
                );
                """
            )
            db.execute(
                "INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                ("NUMQA227", "ase227", 22700, "Kari Elise Nordmann",
                 "Kari Nordmann", "1984-01-15", "Storgata 8", "95273772",
                 "buyer@example.com", "paid", "pending", "2026-09-29T00:00:00Z", ""),
            )
            db.commit(); db.close()
            self.client.force_login(user)
            with self.settings(BASE_DIR=base):
                dashboard = self.client.get(reverse("members:dashboard"))
                self.assertContains(dashboard, "ÅSE 227 Edition")
                self.assertContains(dashboard, "Digital klar")
                report = self.client.get(reverse("members:report", kwargs={"order_id": "NUMQA227"}))
                self.assertEqual(report.status_code, 200)
                self.assertContains(report, "ÅSE 227 Edition")
                self.assertContains(report, "lagre PDF")
