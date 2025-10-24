from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from django import forms

MASTER_NUMBERS = {11, 22, 33}
LETTER_VALUES = {
    "A": 1,
    "J": 1,
    "S": 1,
    "B": 2,
    "K": 2,
    "T": 2,
    "C": 3,
    "L": 3,
    "U": 3,
    "D": 4,
    "M": 4,
    "V": 4,
    "E": 5,
    "N": 5,
    "W": 5,
    "F": 6,
    "O": 6,
    "X": 6,
    "G": 7,
    "P": 7,
    "Y": 7,
    "H": 8,
    "Q": 8,
    "Z": 8,
    "I": 9,
    "R": 9,
}
VOWELS = {"A", "E", "I", "O", "U"}


@dataclass
class NumerologyResult:
    life_path: int
    expression: int
    soul_urge: int
    personality: int
    birth_day: int
    maturity: int

    def as_dict(self) -> Dict[str, int]:
        return {
            "life_path": self.life_path,
            "expression": self.expression,
            "soul_urge": self.soul_urge,
            "personality": self.personality,
            "birth_day": self.birth_day,
            "maturity": self.maturity,
        }


class IntakeForm(forms.Form):
    full_name = forms.CharField(
        label="Full name",
        help_text="Used for expression, soul urge, and personality numbers.",
        max_length=120,
    )
    email = forms.EmailField(label="Email")
    birth_date = forms.DateField(
        label="Date of birth",
        help_text="Life path, birth day, and maturity numbers come from here.",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    focus_area = forms.CharField(
        label="Primary focus",
        required=False,
        help_text="What does the client want clarity on?",
    )
    notes = forms.CharField(
        label="Session notes",
        widget=forms.Textarea(attrs={"rows": 4}),
        required=False,
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css_classes} input".strip()
        self.fields["notes"].widget.attrs.setdefault(
            "placeholder", "Notes to revisit during the session…"
        )
        self.fields["focus_area"].widget.attrs.setdefault(
            "placeholder", "Career change, relationships, life path tune-up…"
        )

    def clean_full_name(self) -> str:
        value = self.cleaned_data["full_name"]
        parts = [part for part in value.split() if part]
        return " ".join(parts)

    def numerology_profile(self) -> NumerologyResult:
        birth_date = self.cleaned_data["birth_date"]
        full_name = self.cleaned_data["full_name"].upper()
        life_path = self._reduce_digits(
            "".join(c for c in birth_date.strftime("%Y%m%d"))
        )
        birth_day = self._reduce_digits(str(birth_date.day))
        expression = self._reduce_name(full_name)
        soul_urge = self._reduce_name(full_name, filter_set=VOWELS)
        personality = self._reduce_name(
            full_name, filter_set=set(LETTER_VALUES) - VOWELS
        )
        maturity = self._reduce_digits(str(life_path + expression))
        return NumerologyResult(
            life_path=life_path,
            expression=expression,
            soul_urge=soul_urge,
            personality=personality,
            birth_day=birth_day,
            maturity=maturity,
        )

    @staticmethod
    def _reduce_digits(digits: str) -> int:
        total = sum(int(char) for char in digits if char.isdigit())
        while total > 9 and total not in MASTER_NUMBERS:
            total = sum(int(char) for char in str(total))
        return total

    @classmethod
    def _reduce_name(cls, value: str, filter_set: set[str] | None = None) -> int:
        letters = [
            LETTER_VALUES[char]
            for char in value
            if char.isalpha()
            and char in LETTER_VALUES
            and (filter_set is None or char in filter_set)
        ]
        if not letters:
            return 0
        total = sum(letters)
        return cls._reduce_digits(str(total))
