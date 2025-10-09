from django.test import SimpleTestCase

from intake.forms import IntakeForm


class IntakeFormTests(SimpleTestCase):
    def test_numerology_profile_core_numbers(self) -> None:
        """The numerology profile should return the expected core numbers."""

        form = IntakeForm(
            data={
                "full_name": "Ada Lovelace",
                "email": "ada@example.com",
                # ``DateField`` expects an ISO formatted string when binding form data.
                "birth_date": "1815-12-10",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        profile = form.numerology_profile().as_dict()

        self.assertEqual(profile["life_path"], 1)
        self.assertEqual(profile["birth_day"], 1)
        self.assertEqual(profile["expression"], 9)
        self.assertEqual(profile["soul_urge"], 1)
        self.assertEqual(profile["personality"], 8)
        self.assertEqual(profile["maturity"], 1)

    def test_clean_full_name_normalizes_whitespace(self) -> None:
        form = IntakeForm(
            data={
                "full_name": "  Ada   Byron   Lovelace  ",
                "email": "ada@example.com",
                "birth_date": "1815-12-10",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["full_name"], "Ada Byron Lovelace")
