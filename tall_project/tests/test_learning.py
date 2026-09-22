from datetime import date

from django.test import SimpleTestCase, override_settings

from intake.forms import LETTER_VALUES, VOWELS, IntakeForm
from tall_project.learning import learning_content


@override_settings(ALLOWED_HOSTS=["testserver"])
class LearningTests(SimpleTestCase):
    def test_lessons_render_in_both_languages_with_shared_footer(self):
        for language in ["en", "no"]:
            self.client.cookies["nl_lang"] = language
            for slug in [
                "discover-numerology",
                "general-interpretation",
                "letter-value-chart",
                "compute-destiny-number",
                "compute-life-path-number",
                "compute-name-vowel-consonant",
                "calculation-methods-overview",
                "pythagoras-legacy",
            ]:
                response = self.client.get("/" + slug + "/")
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'class="l-footer"', count=1)
                self.assertContains(response, "Åse Karin Steinsland")
                self.assertNotContains(response, "{#")

    def test_published_examples_and_master_number_boundaries(self):
        self.assertEqual(IntakeForm._reduce_name("ADA LOVELACE"), 9)
        self.assertEqual(IntakeForm._reduce_name("ROBERT"), 33)
        self.assertEqual(IntakeForm._reduce_name("ØY ÅSE"), 11)
        self.assertEqual(IntakeForm._reduce_name("ØY ÅSE", VOWELS), 1)
        self.assertEqual(IntakeForm._life_path(date(2000, 1, 11)), 5)
        self.assertEqual(IntakeForm._life_path(date(1990, 7, 29)), 1)
        self.assertEqual(IntakeForm._reduce_name("ANNA", VOWELS), 2)
        self.assertEqual(IntakeForm._reduce_name("ANNA", set(LETTER_VALUES) - VOWELS), 1)
        self.assertEqual(IntakeForm._reduce_name("OLA NILSEN"), 2)
        for value in [11, 22, 33]:
            self.assertEqual(IntakeForm._reduce_digits(str(value)), value)

    def test_chart_is_derived_from_the_calculator(self):
        rows = learning_content("letter-value-chart", "nb")["chart"]
        for letter, value in LETTER_VALUES.items():
            self.assertIn(letter, rows[value - 1]["letters"].split(" · "))
        self.assertEqual([LETTER_VALUES[c] for c in "ÅÆØ"], [1, 5, 6])

    def test_about_page_moved_and_nav_has_numbers_menu(self):
        response = self.client.get("/about-the-firm/")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/ase-steinsland/")
        response = self.client.get("/ase-steinsland/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="tel:+4795273772"')
        self.assertNotContains(response, "contact-ase.php")
        self.assertContains(response, 'class="l-numbers"', count=1)
        self.assertNotContains(response, 'href="/#tjenester"')
