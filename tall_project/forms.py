from __future__ import annotations

import calendar
from datetime import date

from django import forms
from django.conf import settings

from intake.forms import LETTER_VALUES, VOWELS, IntakeForm


class LiteCalculatorForm(forms.Form):
    """A minimal numerology calculator for the marketing site."""

    full_name = forms.CharField(
        label="Full name",
        max_length=120,
        help_text="Used to calculate your expression number.",
    )
    birth_day = forms.TypedChoiceField(
        label="Birth day",
        coerce=int,
        choices=((day, f"{day:02d}") for day in range(1, 32)),
        help_text="Day",
    )
    birth_month = forms.TypedChoiceField(
        label="Birth month",
        coerce=int,
        choices=((month, calendar.month_name[month]) for month in range(1, 13)),
        help_text="Month",
    )
    birth_year = forms.TypedChoiceField(
        label="Birth year",
        coerce=int,
        choices=((year, year) for year in range(date.today().year, 1899, -1)),
        help_text="Year",
    )
    access_code = forms.CharField(
        label="Access code",
        max_length=3,
        help_text="This calculator is being tried out with a small group first — ask Åse for the current code.",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css_classes} input".strip()
        self.fields["full_name"].widget.attrs.setdefault(
            "placeholder", "e.g. Åse Aurora Setaei"
        )
        self.fields["full_name"].widget.attrs.setdefault("autocomplete", "name")
        self.fields["birth_day"].widget.attrs.setdefault("autocomplete", "bday-day")
        self.fields["birth_month"].widget.attrs.setdefault(
            "autocomplete", "bday-month"
        )
        self.fields["birth_year"].widget.attrs.setdefault("autocomplete", "bday-year")
        self.fields["access_code"].widget.attrs.setdefault("inputmode", "numeric")
        self.fields["access_code"].widget.attrs.setdefault("autocomplete", "off")
        self.fields["access_code"].widget.attrs.setdefault("placeholder", "•••")

    def clean_access_code(self) -> str:
        value = self.cleaned_data["access_code"].strip()
        if value != settings.CALCULATOR_ACCESS_CODE:
            raise forms.ValidationError("That code isn't right — check with Åse and try again.")
        return value

    def clean(self) -> dict[str, object]:
        cleaned_data = super().clean()
        year = cleaned_data.get("birth_year")
        month = cleaned_data.get("birth_month")
        day = cleaned_data.get("birth_day")
        if year is None or month is None or day is None:
            return cleaned_data
        try:
            cleaned_data["birth_date"] = date(year=year, month=month, day=day)
        except ValueError:
            msg = "Please choose a valid date."
            self.add_error("birth_day", msg)
            self.add_error("birth_month", msg)
            self.add_error("birth_year", msg)
        return cleaned_data

    def clean_full_name(self) -> str:
        value = self.cleaned_data["full_name"].strip()
        parts = [part for part in value.split() if part]
        return " ".join(parts)

    def calculate(self) -> dict[str, int]:
        birth_date = self.cleaned_data["birth_date"]
        full_name = self.cleaned_data["full_name"].upper()
        life_path = IntakeForm._life_path(birth_date)
        expression = IntakeForm._reduce_name(full_name)
        soul_urge = IntakeForm._reduce_name(full_name, filter_set=VOWELS)
        personality = IntakeForm._reduce_name(
            full_name, filter_set=set(LETTER_VALUES) - VOWELS
        )
        return {
            "life_path": life_path,
            "expression": expression,
            "soul_urge": soul_urge,
            "personality": personality,
        }
