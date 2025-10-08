from datetime import date

from intake.forms import IntakeForm


def test_numerology_profile_core_numbers():
    form = IntakeForm(
        data={
            "full_name": "Ada Lovelace",
            "email": "ada@example.com",
            "birth_date": date(1815, 12, 10),
        }
    )
    assert form.is_valid(), form.errors
    profile = form.numerology_profile().as_dict()
    assert profile["life_path"] == 1
    assert profile["birth_day"] == 1
    assert profile["expression"] == 3
    assert profile["soul_urge"] == 6
    assert profile["personality"] == 6
    assert profile["maturity"] == 4
