"""Lightweight, no-birthdate numerology numbers — for cross-project user
profiles (Shahnameh, ReaLink/SetaLink) that only have an ID and/or a name,
not a birth date on file.

Reuses the exact LETTER_VALUES/MASTER_NUMBERS table from IntakeForm
(intake/forms.py) so a "navnetall" computed here always matches what the
full intake flow would produce for the expression number — just without
requiring birth_date to be present.
"""
from __future__ import annotations

import re

from .forms import LETTER_VALUES, MASTER_NUMBERS

__all__ = ["id_vibration", "name_vibration"]


def _reduce(total: int) -> int:
    while total > 9 and total not in MASTER_NUMBERS:
        total = sum(int(char) for char in str(total))
    return total


def id_vibration(identifier: int | str) -> int:
    """Digit-reduce any identifier (Telegram numeric ID, a device UUID, an
    order number, ...) to its vibration. Non-digit characters are ignored,
    so this works on UUIDs/strings as well as plain integers."""
    digits = [int(c) for c in re.findall(r"\d", str(identifier))]
    if not digits:
        return 0
    return _reduce(sum(digits))


def name_vibration(full_name: str) -> int:
    """Expression-number-equivalent for a name with no birth date on file —
    same letter table and reduction rule IntakeForm.numerology_profile()
    uses for 'expression', just callable standalone."""
    letters = [
        LETTER_VALUES[c]
        for c in full_name.upper()
        if c.isalpha() and c in LETTER_VALUES
    ]
    if not letters:
        return 0
    return _reduce(sum(letters))
