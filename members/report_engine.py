from __future__ import annotations

import re
from datetime import date
from typing import Any

VALUES = {
    "A": 1, "J": 1, "S": 1, "Ø": 1,
    "B": 2, "K": 2, "T": 2, "Å": 2,
    "C": 3, "L": 3, "U": 3,
    "D": 4, "M": 4, "V": 4,
    "E": 5, "N": 5, "W": 5,
    "F": 6, "O": 6, "X": 6,
    "G": 7, "P": 7, "Y": 7,
    "H": 8, "Q": 8, "Z": 8,
    "I": 9, "R": 9, "Æ": 9,
}
VOWELS = set("AEIOUÆØÅ")
MASTER = {11, 22, 33}


def root_digit(value: int) -> int:
    value = abs(int(value or 0))
    while value > 9:
        value = sum(int(x) for x in str(value))
    return value


def reduce_master(value: int) -> int:
    value = abs(int(value or 0))
    while value > 9 and value not in MASTER:
        value = sum(int(x) for x in str(value))
    return value


def notation(raw: int) -> dict[str, Any]:
    kept = reduce_master(raw)
    root = root_digit(kept)
    return {"raw": raw, "kept": kept, "root": root, "label": f"{raw}/{root}" if raw > 9 else str(root)}


def _words(value: str) -> list[str]:
    return [re.sub(r"[-'’]", "", x) for x in (value or "").upper().split() if x]


def _is_vowel(word: str, index: int) -> bool:
    char = word[index]
    if char in VOWELS:
        return True
    if char != "Y":
        return False
    previous = word[index - 1] if index else ""
    following = word[index + 1] if index + 1 < len(word) else ""
    return not ((index == 0 and following in VOWELS) or previous in VOWELS or following in VOWELS)


def name_calc(value: str, mode: str = "all") -> dict[str, Any]:
    parts = []
    for word in _words(value):
        total = 0
        for index, char in enumerate(word):
            if char not in VALUES:
                continue
            vowel = _is_vowel(word, index)
            if mode == "vowels" and not vowel:
                continue
            if mode == "consonants" and vowel:
                continue
            total += VALUES[char]
        if total:
            parts.append({"word": word, "sum": total, "reduced": reduce_master(total)})
    result = notation(sum(x["reduced"] for x in parts))
    result["parts"] = parts
    return result


def destiny(iso_date: str) -> dict[str, Any] | None:
    try:
        parsed = date.fromisoformat(iso_date)
    except (TypeError, ValueError):
        return None
    day = reduce_master(parsed.day)
    month = reduce_master(parsed.month)
    year = reduce_master(sum(int(x) for x in str(parsed.year)))
    result = notation(day + month + year)
    result.update({"day": parsed.day, "month": parsed.month, "year": parsed.year})
    return result


def birthday_number(iso_date: str) -> int:
    try:
        return date.fromisoformat(iso_date).day
    except (TypeError, ValueError):
        return 0


def personal_year(iso_date: str, year: int) -> int:
    try:
        parsed = date.fromisoformat(iso_date)
    except (TypeError, ValueError):
        return 0
    y = root_digit(sum(int(x) for x in str(year)))
    return root_digit(root_digit(parsed.day) + root_digit(parsed.month) + y)


def personal_month(iso_date: str, when: date | None = None) -> int:
    when = when or date.today()
    return root_digit(personal_year(iso_date, when.year) + root_digit(when.month))


def current_age(iso_date: str, when: date | None = None) -> int:
    when = when or date.today()
    try:
        born = date.fromisoformat(iso_date)
    except (TypeError, ValueError):
        return 0
    age = when.year - born.year - ((when.month, when.day) < (born.month, born.day))
    return max(0, age)


def transit(value: str, age: int) -> dict[str, Any] | None:
    letters = [char for char in (value or "").upper() if char in VALUES]
    if not letters:
        return None
    total = sum(VALUES[char] for char in letters)
    position = age % total
    cumulative = 0
    for letter in letters:
        start = cumulative
        end = cumulative + VALUES[letter] - 1
        if start <= position <= end:
            cycle_start = age - position
            return {
                "letter": letter,
                "value": VALUES[letter],
                "start": cycle_start + start,
                "end": cycle_start + end,
                "total": total,
            }
        cumulative += VALUES[letter]
    return None


def pinnacle_cycles(iso_date: str) -> list[dict[str, Any]]:
    life = destiny(iso_date)
    if not life:
        return []
    parsed = date.fromisoformat(iso_date)
    day = reduce_master(parsed.day)
    month = reduce_master(parsed.month)
    year = reduce_master(sum(int(x) for x in str(parsed.year)))
    first = notation(day + month)
    second = notation(year + day)
    third = notation(first["kept"] + second["kept"])
    fourth = notation(year + month)
    return [first, second, third, fourth]


def life_cycles(iso_date: str) -> list[int]:
    try:
        parsed = date.fromisoformat(iso_date)
    except (TypeError, ValueError):
        return []
    return [
        reduce_master(parsed.month),
        reduce_master(parsed.day),
        reduce_master(sum(int(x) for x in str(parsed.year))),
    ]


def challenges(iso_date: str) -> list[int]:
    try:
        parsed = date.fromisoformat(iso_date)
    except (TypeError, ValueError):
        return []
    day = root_digit(parsed.day)
    month = root_digit(parsed.month)
    year = root_digit(sum(int(x) for x in str(parsed.year)))
    c1 = abs(month - day)
    c2 = abs(year - day)
    return [c1, c2, abs(c1 - c2), abs(year - month)]


def digits_number(value: str) -> int:
    digits = [int(x) for x in re.findall(r"\d", value or "")]
    return root_digit(sum(digits)) if digits else 0


def address_number(value: str) -> int:
    match = re.search(r"\d+", value or "")
    if match:
        return root_digit(sum(int(x) for x in match.group()))
    total = sum(VALUES.get(char, 0) for char in (value or "").upper())
    return root_digit(total)


def calculate_profile(data: dict[str, Any]) -> dict[str, Any]:
    birth_name = (data.get("birth_name") or "").strip()
    current_name = (data.get("current_name") or birth_name).strip()
    birth_date = data.get("birth_date") or ""
    birth_parts = _words(birth_name)
    first = birth_parts[0] if birth_parts else ""
    last = birth_parts[-1] if birth_parts else ""
    middle = " ".join(birth_parts[1:-1]) if len(birth_parts) > 2 else ""
    life = destiny(birth_date) or notation(0)
    expression = name_calc(birth_name)
    soul = name_calc(birth_name, "vowels")
    personality = name_calc(birth_name, "consonants")
    current = name_calc(current_name)
    age = current_age(birth_date)
    physical = transit(first, age)
    mental = transit(middle, age) if middle else None
    spiritual = transit(last, age)
    active = [x for x in (physical, mental, spiritual) if x]
    essence = notation(sum(x["value"] for x in active))
    maturity = notation(expression["kept"] + life["kept"])
    return {
        "birth_name": birth_name,
        "current_name": current_name,
        "birth_date": birth_date,
        "age": age,
        "expression": expression,
        "soul": soul,
        "personality": personality,
        "current": current,
        "life": life,
        "birthday": birthday_number(birth_date),
        "personal_year": personal_year(birth_date, date.today().year),
        "personal_month": personal_month(birth_date),
        "physical": physical,
        "mental": mental,
        "spiritual": spiritual,
        "essence": essence,
        "pinnacles": pinnacle_cycles(birth_date),
        "life_cycles": life_cycles(birth_date),
        "challenges": challenges(birth_date),
        "maturity": maturity,
        "phone": digits_number(data.get("phone") or ""),
        "address": address_number(data.get("address") or ""),
    }
