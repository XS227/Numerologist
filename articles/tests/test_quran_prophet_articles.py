from django.test import TestCase, override_settings


@override_settings(ALLOWED_HOSTS=["testserver"])
class QuranAndProphetArticleTests(TestCase):
    """Both articles are created by migration 0011 and use the journey base."""

    def test_quran_article_renders_with_calculator(self):
        response = self.client.get("/articles/tallene-i-koranen/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="number-journey j-article"')
        self.assertContains(response, 'id="surah-select"')
        self.assertContains(response, "6236 vers")
        self.assertNotContains(response, "{%")

    def test_prophet_article_shows_the_master_number(self):
        response = self.client.get("/articles/profeten-muhammads-tall/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "40 + 8 + 40 + 4 = 92")
        self.assertContains(response, 'class="ja-master">11<', count=2)
        self.assertNotContains(response, "{%")

    def test_both_articles_are_listed(self):
        response = self.client.get("/articles/")
        self.assertContains(response, "/articles/tallene-i-koranen/")
        self.assertContains(response, "/articles/profeten-muhammads-tall/")
