"""Utilities for working with Åse-inspired numerology.

The Åse system maps integers to *vibrations* by repeatedly summing their digits
until a single-digit value emerges. Master frequencies (11, 22, 33) are treated
as stable attractors and therefore are not reduced further.

This module provides helpers for normalising raw inputs (dates, strings,
integers) and converting them into the vibration space used throughout the
Arecibo Line project.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from numbers import Integral
from typing import Iterable, Union

MASTER_NUMBERS = {11, 22, 33}

RawInput = Union[Integral, str, date, datetime, Iterable[int]]


def _digits_from_string(value: str) -> Iterable[int]:
    """Extract numeric digits from ``value``.

    Non-digit characters are ignored, allowing the function to accept formatted
    dates (``"1974-11-16"``), identifiers (``"FRB 121102"``), or textual
    descriptions with embedded numbers.
    """

    for char in re.findall(r"\d", value):
        yield int(char)


def _normalise_raw_input(raw: RawInput) -> Iterable[int]:
    """Yield digits from ``raw`` regardless of its original representation."""

    if isinstance(raw, Integral):
        return map(int, str(abs(int(raw))))
    if isinstance(raw, (date, datetime)):
        return map(int, raw.strftime("%Y%m%d"))
    if isinstance(raw, str):
        return _digits_from_string(raw)
    if isinstance(raw, Iterable):
        digits: list[int] = []
        for value in raw:
            digits.extend(_normalise_raw_input(value))
        return iter(digits)
    raise TypeError(f"Unsupported input type: {type(raw)!r}")


def sum_digits(digits: Iterable[int]) -> int:
    """Return the sum of ``digits`` ensuring each element is a single digit."""

    total = 0
    for digit in digits:
        if digit < 0 or digit > 9:
            raise ValueError("All digits must be between 0 and 9 inclusive.")
        total += digit
    return total


def reduce_to_vibration(raw: RawInput) -> int:
    """Reduce ``raw`` to its Åse vibration.

    Parameters
    ----------
    raw:
        Any mixture of integers, strings, dates, datetimes, or iterables
        containing those types. The function extracts the numeric digits, sums
        them, and repeatedly reduces the sum until a single digit remains, unless
        a master number (11, 22, 33) is encountered.

    Returns
    -------
    int
        The vibration value between 0 and 9 inclusive or a master number.
    """

    digits_iterable = _normalise_raw_input(raw)
    total = sum_digits(digits_iterable)

    while total not in MASTER_NUMBERS and total > 9:
        total = sum_digits(map(int, str(total)))

    return total


__all__ = ["reduce_to_vibration", "sum_digits", "MASTER_NUMBERS"]
