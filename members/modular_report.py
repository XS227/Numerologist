from __future__ import annotations

from typing import Any

from .report_engine import calculate_profile

CORE = [
    ("name", {"no": "Navnetall / Expression", "en": "Name / Expression", "fa": "عدد نام / بیان"}, "expression"),
    ("vowel", {"no": "Vokaltall / Heart’s Desire", "en": "Vowel / Heart’s Desire", "fa": "عدد حروف صدادار / خواسته قلبی"}, "soul"),
    ("consonant", {"no": "Konsonanttall / Personality", "en": "Consonant / Personality", "fa": "عدد حروف بی‌صدا / شخصیت"}, "personality"),
    ("life_path", {"no": "Skjebnetall / Life Path", "en": "Destiny / Life Path", "fa": "عدد سرنوشت / مسیر زندگی"}, "life"),
    ("birthday", {"no": "Fødselsdagstall", "en": "Birthday Number", "fa": "عدد روز تولد"}, "birthday"),
]

MODULES = {
    "current_name": ({"no": "Nåværende navnetall", "en": "Current Name Number", "fa": "عدد نام فعلی"}, "/current-name-number/"),
    "current_vowel": ({"no": "Nåværende vokaltall", "en": "Current Vowel Number", "fa": "عدد حروف صدادار نام فعلی"}, "/current-vowel-number/"),
    "cornerstone": ({"no": "Hjørnestein / første bokstav", "en": "Cornerstone / First Letter", "fa": "سنگ بنا / حرف اول"}, "/cornerstone-number/"),
    "life_name_bridge": ({"no": "Livsvei–navn bro", "en": "Life Path–Name Bridge", "fa": "پل مسیر زندگی و نام"}, "/life-path-name-bridge/"),
    "vowel_consonant_bridge": ({"no": "Vokal–konsonant bro", "en": "Vowel–Consonant Bridge", "fa": "پل صدادار و بی‌صدا"}, "/vowel-consonant-bridge/"),
    "balance": ({"no": "Balansetall", "en": "Balance Number", "fa": "عدد تعادل"}, "/balance-number/"),
    "karmic_debt": ({"no": "Karmiske gjeldstall", "en": "Karmic Debt Numbers", "fa": "اعداد بدهی کارمایی"}, "/karmic-debt-number/"),
    "karmic_lesson": ({"no": "Karmiske læringstall", "en": "Karmic Lessons", "fa": "درس‌های کارمایی"}, "/karmic-lesson/"),
    "health_profile": ({"no": "Symbolsk helseprofil", "en": "Symbolic Health Profile", "fa": "پروفایل نمادین سلامت"}, "/health-profile-number/"),
    "pinnacles": ({"no": "Fire utviklingstrinn", "en": "Four Pinnacle Cycles", "fa": "چهار چرخه اوج"}, "/pinnacle-cycles/"),
    "life_cycles": ({"no": "Tre livsperioder", "en": "Three Life Cycles", "fa": "سه چرخه زندگی"}, "/life-cycles/"),
    "maturity": ({"no": "Realiseringstall / Maturity", "en": "Maturity / Realization Number", "fa": "عدد بلوغ / تحقق"}, "/maturity-number/"),
    "challenges": ({"no": "Fire utfordringstall", "en": "Four Challenge Numbers", "fa": "چهار عدد چالش"}, "/challenge-numbers/"),
    "personal_year": ({"no": "Personlig år – nå", "en": "Personal Year – Now", "fa": "سال شخصی – اکنون"}, "/personal-year-number/"),
    "personal_month": ({"no": "Personlig måned – nå", "en": "Personal Month – Now", "fa": "ماه شخصی – اکنون"}, "/personal-month-number/"),
    "physical_transit": ({"no": "Fysisk transitt", "en": "Physical Transit", "fa": "ترانزیت فیزیکی"}, "/physical-transit-number/"),
    "mental_transit": ({"no": "Mental transitt", "en": "Mental Transit", "fa": "ترانزیت ذهنی"}, "/mental-transit-number/"),
    "spiritual_transit": ({"no": "Spirituell transitt", "en": "Spiritual Transit", "fa": "ترانزیت معنوی"}, "/spiritual-transit-number/"),
    "essence": ({"no": "Essenstall – nå", "en": "Essence Number – Now", "fa": "عدد اسنس – اکنون"}, "/essence-number/"),
    "address": ({"no": "Adressetall", "en": "Address Number", "fa": "عدد نشانی"}, "/address-number/"),
    "telephone": ({"no": "Telefonnummer", "en": "Telephone Number", "fa": "عدد تلفن"}, "/telephone-number/"),
    "lucky": ({"no": "Lykketall", "en": "Lucky Number", "fa": "عدد شانس"}, "/lucky-number/"),
    "partner": ({"no": "Partner / relasjonsanalyse", "en": "Partner / Relationship Analysis", "fa": "تحلیل شریک / رابطه"}, "/partner-profile/"),
}

DESCRIPTIONS = {
    "no": {
        "current_name": "Viser hvordan navnet du bruker i dag legger et nytt lag over fødselsnavnet.",
        "current_vowel": "Leser vokalene i nåværende navn som et mer aktuelt indre motivasjonslag.",
        "cornerstone": "Første bokstav i fødselsnavnet brukes som et tilleggssymbol for hvordan du møter muligheter og hindringer.",
        "life_name_bridge": "Viser avstanden mellom livsretningen og navnets uttrykk, og hvor de to lagene må bygges sammen.",
        "vowel_consonant_bridge": "Viser avstanden mellom det indre ønsket og det ytre uttrykket andre først møter.",
        "balance": "Bygger på initialene i fødselsnavnet og brukes som et symbolsk råd for pressede situasjoner.",
        "karmic_debt": "Ser etter sammentallene 13/4, 14/5, 16/7 og 19/1 i de sentrale beregningene.",
        "karmic_lesson": "Viser 1–9-verdier som mangler i navnet og heller ikke er representert blant kjernetallene.",
        "health_profile": "Åses symbolske helseprofil leser navnetallet sammen med livsveien. Dette er ikke en medisinsk vurdering.",
        "pinnacles": "De fire utviklingstrinnene danner et langsomt bakteppe for livets større perioder.",
        "life_cycles": "Tre lange livsperioder fra fødselsmåned, fødselsdag og fødselsår.",
        "maturity": "Navnetall og livsvei kombineres til et realiseringstall som får større betydning med modenhet.",
        "challenges": "Fire utfordringstall viser læringstema som kan komme tilbake i ulike livsfaser.",
        "personal_year": "Det personlige året beskriver det overordnede numerologiske klimaet i kalenderåret.",
        "personal_month": "Den personlige måneden legger en kortere rytme oppå årets hovedtema.",
        "physical_transit": "Aktiv bokstav fra fornavnslaget ved din nåværende alder.",
        "mental_transit": "Aktiv bokstav fra mellomnavnslaget når et slikt lag finnes.",
        "spiritual_transit": "Aktiv bokstav fra etternavnslaget ved din nåværende alder.",
        "essence": "Essenstallet kombinerer de aktive navnetransittene og leses sterkest fra fødselsdag til fødselsdag.",
        "address": "Reduserer adressens tall/tegn til ett symbolsk miljøtall.",
        "telephone": "Reduserer sifrene i telefonnummeret til ett tall som kan sammenlignes med kjernekartet.",
        "lucky": "Følger Åses oversikt og bruker samme fødselsdatobase som livsvei/skjebnetall.",
        "partner": "Legger partnerens kjernekart ved siden av ditt. Relasjonstolkningen skal leses som flere lag, ikke én dom.",
    },
    "en": {},
    "fa": {},
}


def _label(labels: dict[str, str], language: str) -> str:
    return labels.get(language) or labels.get("en") or labels.get("no") or ""


def _notation(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("label") or value.get("root") or value.get("value") or "—")
    return str(value if value not in (None, "") else "—")


def _transit(value: dict[str, Any] | None) -> str:
    if not value:
        return "—"
    return f"{value.get('letter', '—')} · {value.get('value', '—')}"


def _module_value(module_id: str, profile: dict[str, Any]) -> str:
    if module_id == "current_name":
        return _notation(profile.get("current"))
    if module_id == "current_vowel":
        return _notation(profile.get("current_vowel"))
    if module_id == "cornerstone":
        item = profile.get("cornerstone") or {}
        return f"{item.get('letter', '—')} · {item.get('value', '—')}"
    if module_id == "life_name_bridge":
        return str(profile.get("life_name_bridge", "—"))
    if module_id == "vowel_consonant_bridge":
        return str(profile.get("vowel_consonant_bridge", "—"))
    if module_id == "balance":
        return _notation(profile.get("balance"))
    if module_id == "karmic_debt":
        items = profile.get("karmic_debts") or []
        return " · ".join(_notation(item) for item in items) if items else "Ingen"
    if module_id == "karmic_lesson":
        items = profile.get("karmic_lessons") or []
        return " · ".join(map(str, items)) if items else "Ingen"
    if module_id == "health_profile":
        return f"{profile.get('expression', {}).get('root', '—')} · {profile.get('life', {}).get('root', '—')}"
    if module_id == "pinnacles":
        return " → ".join(_notation(item) for item in profile.get("pinnacles", []))
    if module_id == "life_cycles":
        return " → ".join(map(str, profile.get("life_cycles", [])))
    if module_id == "maturity":
        return _notation(profile.get("maturity"))
    if module_id == "challenges":
        return " · ".join(map(str, profile.get("challenges", [])))
    if module_id == "personal_year":
        return str(profile.get("personal_year", "—"))
    if module_id == "personal_month":
        return str(profile.get("personal_month", "—"))
    if module_id == "physical_transit":
        return _transit(profile.get("physical"))
    if module_id == "mental_transit":
        return _transit(profile.get("mental"))
    if module_id == "spiritual_transit":
        return _transit(profile.get("spiritual"))
    if module_id == "essence":
        return _notation(profile.get("essence"))
    if module_id == "address":
        return str(profile.get("address", "—"))
    if module_id == "telephone":
        return str(profile.get("phone", "—"))
    if module_id == "lucky":
        return _notation(profile.get("life"))
    return "—"


def build_modular_report(
    data: dict[str, Any],
    profile: dict[str, Any],
    config: dict[str, Any],
    *,
    language: str = "no",
) -> dict[str, Any]:
    language = language if language in {"no", "en", "fa"} else "en"
    core_rows = []
    for module_id, labels, key in CORE:
        core_rows.append(
            {
                "id": module_id,
                "title": _label(labels, language),
                "value": _notation(profile.get(key)),
            }
        )

    rows = []
    selected = [item for item in config.get("modules", []) if item in MODULES]
    for module_id in selected:
        labels, url = MODULES[module_id]
        row = {
            "id": module_id,
            "title": _label(labels, language),
            "value": _module_value(module_id, profile),
            "url": url,
            "description": DESCRIPTIONS.get(language, {}).get(module_id)
            or DESCRIPTIONS["no"].get(module_id, ""),
        }
        rows.append(row)

    partner_profile = None
    if "partner" in selected:
        partner_name = str(config.get("partner_name") or "").strip()
        partner_date = str(config.get("partner_date") or "").strip()
        if partner_name and partner_date:
            partner_profile = calculate_profile(
                {
                    "birth_name": partner_name,
                    "current_name": partner_name,
                    "birth_date": partner_date,
                }
            )

    return {
        "core": core_rows,
        "modules": rows,
        "future_months": int(config.get("future_months") or 0),
        "human_review": bool(config.get("human_review")),
        "partner_profile": partner_profile,
        "partner_name": str(config.get("partner_name") or "").strip(),
    }
