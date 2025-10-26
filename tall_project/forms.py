from __future__ import annotations

from django import forms

from intake.forms import LETTER_VALUES, VOWELS, IntakeForm


class LiteCalculatorForm(forms.Form):
    """A minimal numerology calculator for the marketing site."""

    full_name = forms.CharField(
        label="Full name",
        max_length=120,
        help_text="Used to calculate your expression number.",
    )
    birth_date = forms.DateField(
        label="Date of birth",
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="We'll use this to find your life path number.",
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
        self.fields["birth_date"].widget.attrs.setdefault("autocomplete", "bday")

    def clean_full_name(self) -> str:
        value = self.cleaned_data["full_name"].strip()
        parts = [part for part in value.split() if part]
        return " ".join(parts)

    def calculate(self) -> dict[str, int]:
        birth_date = self.cleaned_data["birth_date"]
        full_name = self.cleaned_data["full_name"].upper()
        life_path = IntakeForm._reduce_digits(
            "".join(c for c in birth_date.strftime("%Y%m%d"))
        )
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
