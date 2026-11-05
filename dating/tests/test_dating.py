from datetime import date
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, SimpleTestCase, override_settings
from django.utils import timezone
from members.report_engine import calculate_profile, personal_year
from dating.engine import profile, compare, resonance
from dating.forms import PersonForm
from dating.models import DatingProfile
from dating.views import CONSENT_VERSION
from dating.copy import COPY

WHEN = date(2026, 10, 27)


class EngineTests(SimpleTestCase):
    def test_reuses_existing_member_engine_including_nordic_letters(self):
        for name in ("Åse Østby", "Khabat Setaei", "Yara Young"):
            actual = profile(name, date(1984, 2, 27), WHEN)
            expected = calculate_profile({"birth_name": name, "birth_date": "1984-02-27"})
            for key in ("life", "soul", "expression", "maturity"):
                self.assertEqual(actual[key], expected[key])

    def test_index_is_symmetric_and_bounded(self):
        for a in list(range(1, 10)) + [11, 22, 33]:
            for b in list(range(1, 10)) + [11, 22, 33]:
                self.assertEqual(resonance(a, b), resonance(b, a))
                self.assertTrue(0 <= resonance(a, b) <= 100)

    def test_missing_input_does_not_receive_a_score(self):
        self.assertIsNone(resonance(0, 3))

    def test_compare_is_symmetric(self):
        a, b = profile("Anna Berg", date(1990, 1, 1), WHEN), profile("Jon Mo", date(1988, 4, 12), WHEN)
        self.assertEqual(compare(a, b, WHEN)["score"], compare(b, a, WHEN)["score"])

    def test_calendar_rollover_and_engine_years(self):
        a, b = profile("Anna Berg", date(1990, 1, 1), WHEN), profile("Jon Mo", date(1988, 4, 12), WHEN)
        result = compare(a, b, WHEN)
        self.assertEqual([x["year"] for x in result["years"]], [2026, 2027, 2028])
        self.assertEqual(result["months"][0]["date"], date(2026, 10, 1))
        self.assertEqual(result["months"][-1]["date"], date(2027, 9, 1))
        self.assertEqual(result["years"][1]["a"], personal_year("1990-01-01", 2027))

    def test_all_three_translations_have_same_keys(self):
        for language in ("en", "fa"):
            self.assertEqual(set(COPY["no"]), set(COPY[language]))

    def test_rejects_unsupported_script_and_partial_names(self):
        for name in ("علی", "Anna 李", "123", "Anna2"):
            self.assertFalse(PersonForm({"full_name": name, "birth_date": "1990-01-01"}).is_valid())

    def test_rejects_minors_future_and_invalid_dates(self):
        for birthday in (date.today().isoformat(), "2999-01-01", "2020-02-30"):
            self.assertFalse(PersonForm({"full_name": "Anna Berg", "birth_date": birthday}).is_valid())


class DatingTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="owner")
        self.other = User.objects.create_user(username="candidate")
        common = dict(full_name="Anna Berg", birth_date=date(1990, 1, 1), alias="AliasOne",
                      gender="woman", seeking="any", intent="longterm",
                      min_age=18, max_age=99, consent_version=CONSENT_VERSION,
                      consented_at=timezone.now(), is_visible=True)
        self.me = DatingProfile.objects.create(user=self.user, **common)
        common.update(full_name="Jon Mo", birth_date=date(1988, 4, 12), alias="AliasTwo", gender="man")
        self.candidate = DatingProfile.objects.create(user=self.other, **common)

    def test_public_page_three_languages(self):
        for lang in ("no", "en", "fa"):
            response = self.client.get("/dating/?lang=" + lang)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, COPY[lang]["title"])
            self.assertEqual(response.headers["Cache-Control"], "private, no-store, max-age=0, no-cache, must-revalidate")
        self.assertContains(self.client.get("/dating/?lang=fa"), 'dir="rtl"')

    def test_single_and_pair_calculations_do_not_save_profiles(self):
        before = DatingProfile.objects.count()
        data = {"mode": "self", "you-full_name": "Anna Berg", "you-birth_date": "1990-01-01"}
        self.assertContains(self.client.post("/dating/?lang=no", data), COPY["no"]["your_numbers"])
        data.update(mode="pair", **{"other-full_name": "Jon Mo", "other-birth_date": "1988-04-12"})
        result = self.client.post("/dating/?lang=no", data)
        self.assertEqual(result.status_code, 200)
        self.assertContains(result, COPY["no"]["timeline"])
        self.assertEqual(DatingProfile.objects.count(), before)

    def test_incomplete_pair_reports_errors_without_a_score(self):
        result = self.client.post("/dating/?lang=no", {
            "mode": "pair", "you-full_name": "Anna Berg", "you-birth_date": "1990-01-01"})
        self.assertEqual(result.status_code, 200)
        self.assertNotContains(result, 'class="score-circle"')

    def test_membership_required(self):
        for endpoint in ("matches/", "profile/", "connection/1/"):
            response = self.client.get("/dating/" + endpoint)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/min-side/login/", response.url)

    def test_mutual_match_displays_alias_and_not_private_inputs(self):
        self.client.force_login(self.user)
        result = self.client.get("/dating/matches/?lang=no")
        self.assertContains(result, "AliasTwo")
        self.assertNotContains(result, "Jon Mo")
        self.assertNotContains(result, "1988-04-12")
        detail = self.client.get(f"/dating/connection/{self.candidate.pk}/?lang=no")
        self.assertEqual(detail.status_code, 200)
        self.assertNotContains(detail, "Jon Mo")
        self.assertNotContains(detail, "1988-04-12")

    def test_candidate_withdrawal_removes_match_and_detail(self):
        self.client.force_login(self.user)
        self.candidate.is_visible = False
        self.candidate.save()
        self.assertNotContains(self.client.get("/dating/matches/"), "AliasTwo")
        self.assertEqual(self.client.get(f"/dating/connection/{self.candidate.pk}/").status_code, 404)

    def test_reciprocal_filters_all_apply(self):
        self.client.force_login(self.user)
        for field, value in (("seeking", "woman"), ("min_age", 99), ("intent", "explore"),
                             ("consent_version", "")):
            original = getattr(self.candidate, field)
            setattr(self.candidate, field, value)
            if field == "seeking":
                self.me.gender = "nonbinary"
                self.me.save()
            self.candidate.save()
            self.assertNotContains(self.client.get("/dating/matches/"), "AliasTwo")
            self.assertEqual(self.client.get(f"/dating/connection/{self.candidate.pk}/").status_code, 404)
            setattr(self.candidate, field, original)
            self.candidate.save()

    def test_hidden_owner_cannot_inspect_detail(self):
        self.client.force_login(self.user)
        self.me.is_visible = False
        self.me.save()
        self.assertEqual(self.client.get(f"/dating/connection/{self.candidate.pk}/").status_code, 404)

    def test_minor_or_inactive_candidate_is_excluded(self):
        self.client.force_login(self.user)
        self.candidate.birth_date = date.today()
        self.candidate.save()
        self.assertNotContains(self.client.get("/dating/matches/"), "AliasTwo")
        self.candidate.birth_date = date(1988, 4, 12)
        self.candidate.save()
        self.other.is_active = False
        self.other.save()
        self.assertNotContains(self.client.get("/dating/matches/"), "AliasTwo")
        self.assertEqual(self.client.get(f"/dating/connection/{self.candidate.pk}/").status_code, 404)

    def profile_data(self):
        return {"full_name": "Anna Berg", "birth_date": "1990-01-01", "alias": "NewAlias",
                "gender": "woman", "seeking": "any", "intent": "longterm",
                "min_age": 18, "max_age": 99, "is_visible": "on", "consent": "on"}

    def test_consent_required_and_profile_edit_owned(self):
        self.client.force_login(self.user)
        data = self.profile_data()
        del data["consent"]
        self.client.post("/dating/profile/", data)
        self.me.refresh_from_db()
        self.assertEqual(self.me.alias, "AliasOne")
        data["consent"] = "on"
        response = self.client.post("/dating/profile/", data)
        self.assertEqual(response.status_code, 302)
        self.me.refresh_from_db()
        self.candidate.refresh_from_db()
        self.assertEqual(self.me.alias, "NewAlias")
        self.assertEqual(self.candidate.alias, "AliasTwo")

    def test_invalid_age_preferences_are_rejected(self):
        self.client.force_login(self.user)
        data = self.profile_data()
        data["min_age"], data["max_age"] = 60, 20
        self.assertEqual(self.client.post("/dating/profile/", data).status_code, 200)
        self.me.refresh_from_db()
        self.assertEqual(self.me.min_age, 18)

    def test_delete_post_only_and_keeps_account_and_other_profiles(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get("/dating/delete/").status_code, 405)
        self.assertEqual(self.client.post("/dating/delete/").status_code, 302)
        self.assertFalse(DatingProfile.objects.filter(user=self.user).exists())
        self.assertTrue(DatingProfile.objects.filter(user=self.other).exists())
        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())

    def test_csrf_for_mutations(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        for url, data in (("/dating/delete/", {}), ("/dating/profile/", self.profile_data()),
                          ("/dating/", {"mode": "self"})):
            self.assertEqual(client.post(url, data).status_code, 403)

    @override_settings(MIDDLEWARE=["django.contrib.sessions.middleware.SessionMiddleware",
                        "tall_project.early_preview.EarlyPreviewMiddleware",
                        "django.contrib.auth.middleware.AuthenticationMiddleware"])
    def test_existing_preview_gate_protects_experiment(self):
        response = self.client.get("/dating/")
        self.assertNotContains(response, COPY["no"]["title"])
        self.assertEqual(self.client.post("/dating/", {}).status_code, 403)
