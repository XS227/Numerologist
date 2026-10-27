# Numerologist Dating Experiment — v1

A dating experiment at `/dating/`, using the existing member-report numerology
engine. Public test calculations require no profile and write nothing to the
database. Real matching requires an authenticated user to create a separate
dating profile, explicitly consent, and choose visibility.

## Experience

- Norwegian, English and Persian, including RTL.
- Name and Gregorian birth date produce life path, soul, expression and maturity.
- Two-person comparisons explain each component, a shared root number, three
  calendar years and the next twelve calendar months.
- Adults can opt into a real pool with alias, city, gender, desired gender,
  relationship intent and mutual age preferences.
- Results are ranked only after both users meet each other's preferences.
- No fictional profiles or implicit use of existing member or order data.
- No private birth names or dates in another member's results.
- Visibility withdrawal removes the profile from matches and direct detail views.
- POST-only deletion removes the dating record; the member account is preserved.
- Messaging, profile photos, identity verification and native APK packaging are
  not implemented in this first web version. The 18+ check uses the entered
  date, not an identity-verification service.

## Calculation contract

`dating.engine.profile` calls `members.report_engine.calculate_profile`;
personal year and month call that same engine. The older intake calculator has
different Nordic letter/Y rules and is deliberately not used here. No changes
are made to either existing engine.

Index version: `numerologist-dating-v1`.

| Component | Weight |
| --- | ---: |
| Life path | 30 |
| Inner needs / soul | 25 |
| Expression | 20 |
| Maturity | 15 |
| Current personal year | 10 |

Compare single-digit roots. Preserve master numbers in the display.
A missing value contributes neither score nor weight. The weighted arithmetic
mean is rounded to a whole-number index. The scale is an editorial experiment,
not a calibrated probability or scientific evidence of compatibility.

Rules in order:

1. Identical roots: 95.
2. Friction pairs (1,8), (4,5), (2,5), (3,4), (6,7): 45.
3. Shared family {1,5,7}, {2,4,8}, {3,6,9}: 85.
4. Complement pairs (1,2), (2,6), (3,5), (4,6), (7,9), (8,9): 78.
5. Other pairs: 60.

All pairs are symmetric. Names containing unsupported letters are rejected with
a request for transliteration, rather than silently dropping part of the name.
Dates are Gregorian. Age is checked on the server.

## Validation

Use a separate virtualenv with Django and the repository dependencies.

```sh
python -m django test dating.tests --settings=dating.tests.settings --noinput -v 1
python -m django makemigrations --check --dry-run --settings=dating.tests.settings
```

The isolated settings use in-memory SQLite, do not read the server .env, and do
not connect to production data. They include the existing early-preview gate in
a dedicated test. No users are created outside the test database.

## Integration and deployment status

This branch registers `dating.apps.DatingConfig`, adds the `/dating/` include
before the root slug handler, and includes the first migration. Preserve the
existing server-side early-preview code gate (227).

**Not deployed.** Work was prepared in a separate worktree during the server
migration; the existing checkout and production services were not edited.

A full-project `manage.py check` on base commit
`66a40008d70541ca978c282021241f2e173878a8` fails before the dating module loads:
`ModuleNotFoundError: No module named 'tall_project.language_policy'`.
The base repository also references `members.academy_i18n`, which is absent.
The full-project boot, existing social login, live routing and browser/device
layout remain unverified. Restore the missing existing source modules from their
authoritative version before merging/deploying; do not replace production
configuration with the isolated test settings.

After the underlying project can pass its normal checks, run its standard
migration/static/deploy workflow on the active target. The hybrid nginx config
must route `/dating/` to Django, with the same early-preview auth gate as other
protected app routes. Avoid serving this path through the PHP catch-all.

Validated on 27 October 2026: 22 isolated Django tests pass; the isolated system
check reports no issues; migration drift check reports no changes. Full-project
and visual browser verification are pending for the reasons above.
