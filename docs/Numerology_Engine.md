# Numerology Engine

The Numerologist platform combines traditional Pythagorean numerology with modern UX to provide actionable insights about a person's life path and traits. The core logic lives in `intake/forms.py` and is reused by the marketing site's lightweight calculator (`tall_project/forms.py`).

## Core Calculations

| Number | Description | Source | Implementation Highlights |
| --- | --- | --- | --- |
| **Life Path** | Primary life lessons and direction. | Birth date digits | `IntakeForm._reduce_digits` sums the digits from `YYYYMMDD` and repeatedly reduces the sum until a single digit or master number (11, 22, 33) remains. |
| **Birth Day** | Innate gifts indicated by the day of birth. | Day portion of birth date | Uses the same digit reduction helper as the life path. |
| **Expression** | Natural talents and outward abilities. | Full birth name (letters only) | Each letter is mapped to a numeric value via `LETTER_VALUES` (Pythagorean system). Values are summed and reduced until a single digit or master number. |
| **Soul Urge** | Deep motivations and inner desires. | Vowels from the full name | Applies `_reduce_name` with `filter_set=VOWELS`. |
| **Personality** | How others perceive the individual. | Consonants from the full name | Applies `_reduce_name` with consonants (`LETTER_VALUES - VOWELS`). |
| **Maturity** | Later-in-life synthesis of life path and expression. | Sum of life path and expression numbers | The two values are added and reduced again via `_reduce_digits`. |

All reduction functions respect master numbers, meaning 11, 22, and 33 are preserved instead of being reduced to a single digit.

## Result Model

`NumerologyResult` is a dataclass that stores the six primary numbers and exposes them through `as_dict()` for template rendering or API serialization.

```python
@dataclass
class NumerologyResult:
    life_path: int
    expression: int
    soul_urge: int
    personality: int
    birth_day: int
    maturity: int

    def as_dict(self) -> Dict[str, int]:
        ...
```

The intake view builds a context dictionary that contains both the calculated numbers and supplemental metadata such as session notes and focus area. This allows the template to render a structured summary for practitioners.

## Validation Rules

- **Full name normalisation**: consecutive whitespace is collapsed and casing is uppercased prior to calculation.
- **Birth date**: validated with Django's `DateField` and rendered using an HTML5 date input.
- **Optional session data**: `focus_area` and `notes` fields are optional but provide context for follow-up sessions.

## Extensibility

You can extend the engine by:

1. Adding new constants to `intake/constants.py` for additional interpretations.
2. Extending `NumerologyResult` with more attributes (e.g., personal year cycles) and updating templates accordingly.
3. Creating API serializers that reuse `NumerologyResult.as_dict()` for JSON output.
4. Introducing alternate calculation systems (e.g., Chaldean) by adding new helper functions and exposing them through forms.

Because the numerology helpers are implemented as `@staticmethod` and `@classmethod`, they can be called without instantiating Django form classes, making them easy to unit test or reuse in other contexts such as management commands or background jobs.
