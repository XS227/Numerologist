"""Experimental compatibility index, built on the member-report engine.

The index is an editorial heuristic, not a measured probability of relationship
success. Versioning makes changes to the ranking reviewable.
"""
from datetime import date
from members.report_engine import calculate_profile, personal_year, personal_month, root_digit

VERSION = "numerologist-dating-v1"
WEIGHTS = {"life": 30, "soul": 25, "expression": 20, "maturity": 15, "timing": 10}
FAMILIES = ({1, 5, 7}, {2, 4, 8}, {3, 6, 9})
COMPLEMENTS = {frozenset(pair) for pair in [(1, 2), (2, 6), (3, 5), (4, 6), (7, 9), (8, 9)]}
FRICTION = {frozenset(pair) for pair in [(1, 8), (4, 5), (2, 5), (3, 4), (6, 7)]}


def resonance(a, b):
    """Symmetric lookup with an explicit missing-data result."""
    if not a or not b:
        return None
    a, b = root_digit(a), root_digit(b)
    pair = frozenset((a, b))
    if a == b:
        return 95
    if pair in FRICTION:
        return 45
    if any(a in family and b in family for family in FAMILIES):
        return 85
    return 78 if pair in COMPLEMENTS else 60


def profile(name, birthday, when=None):
    when = when or date.today()
    result = calculate_profile({"birth_name": name, "birth_date": birthday.isoformat()})
    result["personal_year"] = personal_year(birthday.isoformat(), when.year)
    result["personal_month"] = personal_month(birthday.isoformat(), when)
    return result


def compare(left, right, when=None):
    when = when or date.today()
    components = []
    for key, weight in WEIGHTS.items():
        a = left["personal_year"] if key == "timing" else left[key]["kept"]
        b = right["personal_year"] if key == "timing" else right[key]["kept"]
        score = resonance(a, b)
        components.append({"key": key, "a": a, "b": b, "score": score, "weight": weight})
    available = [item for item in components if item["score"] is not None]
    score = round(sum(item["score"] * item["weight"] for item in available) /
                  sum(item["weight"] for item in available)) if available else None
    years = []
    for year in range(when.year, when.year + 3):
        a = personal_year(left["birth_date"], year)
        b = personal_year(right["birth_date"], year)
        years.append({"year": year, "a": a, "b": b, "score": resonance(a, b)})
    months = []
    for offset in range(12):
        index = when.month - 1 + offset
        month = date(when.year + index // 12, index % 12 + 1, 1)
        a = personal_month(left["birth_date"], month)
        b = personal_month(right["birth_date"], month)
        months.append({"date": month, "a": a, "b": b, "score": resonance(a, b)})
    return {"version": VERSION, "score": score, "components": components,
            "years": years, "months": months,
            "relationship_number": root_digit(left["life"]["kept"] + right["life"]["kept"])}
