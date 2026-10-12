"""Standalone regressions: python deploy/verify_early_preview.py."""
import importlib.util
from pathlib import Path
import unittest
import sys

from django.conf import settings

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
if not settings.configured:
    settings.configure(
        SECRET_KEY="test-only-secret-key", EARLY_PREVIEW_ENABLED=True,
        EARLY_PREVIEW_CODE="227", ROOT_URLCONF=__name__, ALLOWED_HOSTS=["testserver"],
        TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [ROOT / "tall_project/templates"]}],
        MIDDLEWARE=["django.middleware.csrf.CsrfViewMiddleware",
                    "tall_project.early_preview.EarlyPreviewMiddleware"],
    )
import django
django.setup()
from django.http import HttpResponse
from django.test import Client, SimpleTestCase, override_settings
from django.urls import path
from tall_project.early_preview import COOKIE, preview, preview_auth

urlpatterns = [path("early-preview/", preview), path("early-preview/auth/", preview_auth),
               path("articles/private/", lambda request: HttpResponse("PRIVATE CONTENT"))]


class GateTests(SimpleTestCase):
    def test_no_content_before_code(self):
        response = self.client.get("/articles/private/?lang=fa")
        self.assertContains(response, "Early preview code")
        self.assertNotContains(response, "PRIVATE CONTENT")
        self.assertContains(response, '/articles/private/?lang=fa')
        self.assertIn("noindex", response["X-Robots-Tag"])

    def test_wrong_and_correct_code(self):
        response = self.client.post("/early-preview/", {"preview_code": "228"})
        self.assertContains(response, "Incorrect code")
        self.assertNotIn(COOKIE, response.cookies)
        self.assertEqual(self.client.get("/early-preview/auth/").status_code, 401)
        response = self.client.post("/early-preview/", {"preview_code": "227", "next": "/articles/private/?lang=fa"}, secure=True)
        self.assertEqual(response["Location"], "/articles/private/?lang=fa")
        self.assertTrue(response.cookies[COOKIE]["httponly"])
        self.assertTrue(response.cookies[COOKIE]["secure"])
        self.assertEqual(self.client.get("/early-preview/auth/").status_code, 204)
        self.assertContains(self.client.get("/articles/private/"), "PRIVATE CONTENT")

    def test_tampered_cookie_and_unsafe_post(self):
        self.client.cookies[COOKIE] = "227"
        self.assertEqual(self.client.get("/early-preview/auth/").status_code, 401)
        self.assertEqual(self.client.post("/articles/private/").status_code, 403)

    def test_no_external_redirect(self):
        for target in ["https://evil.example/", "//evil.example/", "/early-preview/"]:
            client = Client()
            response = client.post("/early-preview/", {"preview_code": "227", "next": target})
            self.assertEqual(response["Location"], "/")

    def test_real_csrf_submission(self):
        client = Client(enforce_csrf_checks=True)
        response = client.get("/articles/private/")
        token = response.cookies["csrftoken"].value
        self.assertEqual(client.post("/early-preview/", {"preview_code": "227"}).status_code, 403)
        self.assertEqual(client.post("/early-preview/", {"preview_code": "227", "csrfmiddlewaretoken": token}).status_code, 302)

    @override_settings(EARLY_PREVIEW_ENABLED=False)
    def test_can_reopen_project(self):
        self.assertContains(self.client.get("/articles/private/"), "PRIVATE CONTENT")


spec = importlib.util.spec_from_file_location("installer", ROOT / "deploy/install_early_preview.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class NginxTests(unittest.TestCase):
    def test_hybrid_gate_and_idempotency(self):
        config = '''# Existing site configuration
server { listen 80; server_name numerologist.setai.no; return 301 https://$host$request_uri; }
server {
 listen 443 ssl; server_name numerologist.setai.no;
 location / { try_files $uri $uri/ /index.php; }
 location /articles/ { proxy_pass http://127.0.0.1:8004; }
 location ~ \\.php$ { fastcgi_pass unix:/run/php/php-fpm.sock; }
}'''
        result = installer.install(config)
        self.assertEqual(result.count(installer.MARKER), 1)
        self.assertIn("auth_request /early-preview/auth/;", result)
        self.assertIn("proxy_pass http://127.0.0.1:8004;", result)
        self.assertEqual(installer.install(result), result)
        self.assertIn("fastcgi_pass unix:/run/php/php-fpm.sock;", result)

    def test_reject_ambiguous_upstreams(self):
        with self.assertRaises(ValueError):
            installer.install("server { server_name numerologist.setai.no; location /a { proxy_pass http://a; } location /b { proxy_pass http://b; } }")


if __name__ == "__main__":
    unittest.main()
