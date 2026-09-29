"""Navigation and static page definitions for the Numerologist site."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

from django.utils.translation import gettext_lazy as _


@dataclass(frozen=True)
class StaticPage:
    """Represents a static content page rendered from a template."""

    slug: str
    title: str
    template_name: str
    description: str = ""
    canonical_override: str = ""
    noindex: bool = False


@dataclass(frozen=True)
class NavigationItem:
    """Navigation structure with optional nested children."""

    slug: str
    title: str
    children: Tuple["NavigationItem", ...] = ()


STATIC_PAGES: Dict[str, StaticPage] = {
    page.slug: page
    for page in (
        StaticPage(
            "discover-numerology",
            _("Discover Numerology"),
            "pages/discover-numerology.html",
            description=_(
                "An introduction to numerology with Åse Steinsland: the Pythagorean roots of the "
                "method, how each digit is interpreted, and where to find the reference charts."
            ),
        ),
        StaticPage(
            "calculators",
            _("Calculator suite"),
            "pages/calculators.html",
            description=_(
                "Free numerology calculators for your life path, destiny, and name numbers, "
                "with a plain-language explanation of what each result means."
            ),
        ),
        StaticPage(
            "ase-edition",
            _("ÅSE Edition — Complete Numerology Reading"),
            "pages/ase-edition.html",
            description=_(
                "One complete numerology engine that combines Åse Steinsland's calculators into a guided, personal reading."
            ),
        ),
        StaticPage(
            "pythagoras-legacy",
            _("Pythagoras' Legacy"),
            "pages/pythagoras-legacy.html",
            description=_(
                "How Pythagorean number theory became the historical foundation for modern "
                "numerology, and what that lineage means for Åse's method today."
            ),
        ),
        StaticPage(
            "general-interpretation",
            _("General Interpretation of Numbers"),
            "pages/general-interpretation.html",
            description=_(
                "A general guide to what each core number from 1-9 and the master numbers "
                "represent in numerology, before you calculate your own."
            ),
        ),
        StaticPage(
            "calculation-methods-overview",
            _("Calculation Methods Overview"),
            "pages/calculation-methods-overview.html",
            description=_(
                "An overview of the calculation methods behind life path, destiny, and name "
                "numbers, so you understand the maths before trusting the result."
            ),
        ),
        StaticPage(
            "letter-value-chart",
            _("Letter Value Chart"),
            "pages/letter-value-chart.html",
            description=_(
                "The Pythagorean letter-to-number chart used to calculate name, vowel, and "
                "consonant numbers, with guidance on how to apply it correctly."
            ),
        ),
        StaticPage(
            "personal-insights",
            _("Personal Insights"),
            "pages/personal-insights.html",
            description=_(
                "How personal numerology insights — destiny, name, and life-stage numbers — "
                "fit together into one coherent reading of your path."
            ),
        ),
        StaticPage(
            "compute-life-path-number",
            _("Compute Your Life Path Number"),
            "pages/compute-life-path-number.html",
            description=_(
                "How to calculate your life path number from your birth date, and what it "
                "reveals about your lifetime rhythm and lessons."
            ),
        ),
        StaticPage(
            "compute-destiny-number",
            _("Compute Your Destiny Number"),
            "pages/compute-destiny-number.html",
            description=_(
                "How to calculate your destiny number from your full birth name, and what it "
                "reveals about your long-term direction and purpose."
            ),
        ),
        StaticPage(
            "compute-name-vowel-consonant",
            _("Compute Name, Vowel & Consonant Numbers"),
            "pages/compute-name-vowel-consonant.html",
            description=_(
                "How to calculate your name, vowel (soul urge), and consonant numbers, and "
                "what each one says about your inner motivation versus outer expression."
            ),
        ),
        StaticPage(
            "current-name-number",
            _("Current Name Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate the numerology number of the full name you use today with Åse Steinsland's per-name-part method."),
        ),
        StaticPage(
            "current-vowel-number",
            _("Current Vowel Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate the vowel number in your current name, including Åse Steinsland's master-number and Norwegian-letter rules."),
        ),
        StaticPage(
            "birthday-number",
            _("Birthday Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Find your Birthday Number from the day of the month you were born, kept as a number from 1 to 31."),
        ),
        StaticPage(
            "cornerstone-number",
            _("Cornerstone Calculator"),
            "pages/ase-calculator.html",
            description=_("Find the Cornerstone in your numerology profile from the first letter of your full birth name."),
        ),
        StaticPage(
            "life-path-name-bridge",
            _("Life Path / Name Number Bridge Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate the Bridge Number between your Name Number and Destiny or Life Path Number using Åse Steinsland's method."),
        ),
        StaticPage(
            "vowel-consonant-bridge",
            _("Vowel / Consonant Bridge Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate the bridge between your birth-name vowel and consonant numbers using Åse Steinsland's method."),
        ),
        StaticPage(
            "balance-number",
            _("Balance Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate your Balance Number from the initials in your full birth name."),
        ),
        StaticPage(
            "address-number",
            _("Address Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate the numerology number connected to your street address using Åse Steinsland's method."),
        ),
        StaticPage(
            "karmic-debt-number",
            _("Karmic Debt Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Check whether the compound numbers 13/4, 14/5, 16/7, or 19/1 appear among your core numerology numbers."),
        ),
        StaticPage(
            "karmic-lesson",
            _("Karmic Lesson Calculator"),
            "pages/ase-calculator.html",
            description=_("Find missing 1–9 values in your birth name and compare them with your core numbers to calculate karmic lessons."),
        ),
        StaticPage(
            "health-profile-number",
            _("Numerological Health Profile"),
            "pages/ase-calculator.html",
            description=_("Calculate the two 1–9 numbers Åse uses for the numerological health-profile section, based on Name and Destiny numbers."),
        ),
        StaticPage(
            "personal-year-number",
            _("Personal Year Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate your Personal Year number from birth day, birth month, and the selected calendar year."),
        ),
        StaticPage(
            "personal-month-number",
            _("Personal Month Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate your Personal Month number from your Personal Year and the selected month."),
        ),
        StaticPage(
            "physical-transit-number",
            _("Physical Transit Calculator"),
            "pages/ase-calculator.html",
            description=_("Find the active Physical Transit letter and number for any age from the first name in your birth name."),
        ),
        StaticPage(
            "mental-transit-number",
            _("Mental Transit Calculator"),
            "pages/ase-calculator.html",
            description=_("Find the active Mental Transit letter and number for any age from the middle-name portion of your birth name."),
        ),
        StaticPage(
            "spiritual-transit-number",
            _("Spiritual Transit Calculator"),
            "pages/ase-calculator.html",
            description=_("Find the active Spiritual Transit letter and number for a selected age from the surname portion of your birth name."),
        ),
        StaticPage(
            "essence-number",
            _("Essence Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Combine the active physical, mental and spiritual name transits to calculate the Essence Number for a selected age."),
        ),
        StaticPage(
            "pinnacle-cycles",
            _("Four Pinnacle Cycles Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate the four long-term development stages, or Pinnacles, from your birth date using Åse Steinsland's method."),
        ),
        StaticPage(
            "life-cycles",
            _("Three Life Cycles Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate the three long life periods from your birth month, birth day and birth year."),
        ),
        StaticPage(
            "maturity-number",
            _("Maturity / Realization Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate the Maturity or Realization Number from the sum of your Name Number and Destiny Number."),
        ),
        StaticPage(
            "challenge-numbers",
            _("Four Challenge Numbers Calculator"),
            "pages/ase-calculator.html",
            description=_("Calculate the four Challenge Numbers from the numerical differences between birth month, day and year."),
        ),
        StaticPage(
            "lucky-number",
            _("Lucky Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Find the Lucky Number used in Åse's method; it follows the same birth-date calculation as the Destiny Number."),
        ),
        StaticPage(
            "telephone-number",
            _("Telephone Number Calculator"),
            "pages/ase-calculator.html",
            description=_("Reduce a telephone number to its 1–9 numerology value and compare it with your core numbers."),
        ),
        StaticPage(
            "partner-profile",
            _("Compatibility / Partner Profile"),
            "pages/ase-calculator.html",
            description=_("Compare two people's Name and Destiny numbers with Åse Steinsland's personal-relationship and work compatibility charts."),
        ),
        StaticPage(
            "lifes-fourth-stage",
            _("Life's 4th Development Stage"),
            "pages/lifes-fourth-stage.html",
            description=_(
                "What the fourth pinnacle stage of life represents in numerology, and how to "
                "recognise when you have entered it."
            ),
        ),
        StaticPage(
            "realization-number",
            _("Realization Number — Your Ultimate Aim"),
            "pages/realization-number.html",
            description=_(
                "How to calculate your realization number, the numerology figure linked to "
                "your ultimate life aim and sense of fulfilment."
            ),
        ),
        StaticPage(
            "pythagoras-arrows",
            _("Pythagoras' Arrows"),
            "pages/pythagoras-arrows.html",
            description=_(
                "How Pythagoras' Arrows (the numerology grid built from your birth date) "
                "reveal patterns of strength and missing lessons in your chart."
            ),
        ),
        StaticPage(
            "same-number-meaning",
            _("Do You See the Same Number?"),
            "pages/same-number-meaning.html",
            description=_(
                "What it means in numerology when you keep noticing the same repeating "
                "number, such as 11:11, 222, or 333."
            ),
        ),
        StaticPage(
            "resources",
            _("Resources"),
            "pages/resources.html",
            description=_(
                "Free analyses, projects, references, and media coverage from Åse Steinsland's "
                "numerology practice, gathered in one place."
            ),
        ),
        StaticPage(
            "projects-lab",
            _("Projects Lab"),
            "pages/projects-lab.html",
            description=_(
                "Experimental and research projects from the Numerologist studio, connecting "
                "numerology with data, culture, and technology."
            ),
        ),
        StaticPage(
            "arecibo-line",
            _("Arecibo Line"),
            "pages/arecibo-line.html",
            description=_(
                "The Arecibo Line project: exploring number symbolism through the lens of the "
                "1974 Arecibo message and its numerical structure."
            ),
        ),
        StaticPage(
            "free-analyses",
            _("Free Analyses"),
            "pages/free-analyses.html",
            description=_(
                "What you get from a free introductory numerology analysis with Åse Steinsland, "
                "and how to request one."
            ),
        ),
        StaticPage(
            "blog-articles",
            _("Blog / Articles"),
            "pages/blog-articles.html",
            description=_(
                "Articles and long-form writing on numerology, symbolism, and number meaning "
                "from Åse Steinsland's Numerologist studio."
            ),
        ),
        StaticPage(
            "references",
            _("References"),
            "pages/references.html",
            description=_(
                "Sources, methods, and reference material behind Åse Steinsland's numerology "
                "practice."
            ),
        ),
        StaticPage(
            "numerologist-in-media",
            _("Numerologist in the Media"),
            "pages/numerologist-in-media.html",
            description=_(
                "Press coverage and media appearances featuring numerologist Åse Steinsland."
            ),
        ),
        StaticPage(
            "quranian-numerology",
            _("Quranian Numerology"),
            "pages/quranian-numerology.html",
            description=_(
                "How numerical patterns are studied in Quranic tradition, and how this "
                "compares with Pythagorean numerology."
            ),
        ),
        StaticPage(
            "quranic-analysis",
            _("Quranic Analysis"),
            "pages/quranian-numerology.html",
            description=_(
                "A closer analytical look at numerical patterns in Quranic tradition — see "
                "Quranian Numerology for the full overview."
            ),
            canonical_override="https://numerologist.setai.no/quranian-numerology/",
            noindex=True,
        ),
        StaticPage(
            "guidance-support",
            _("Guidance & Support"),
            "pages/guidance-support.html",
            description=_(
                "How to get personal guidance and support from Åse Steinsland: about the firm, "
                "telephone sessions, and contact options."
            ),
        ),
        StaticPage(
            "ase-steinsland",
            "Åse Karin Steinsland",
            "pages/ase-steinsland.html",
            description=(
                "Møt Åse Karin Steinsland – numerolog og livsveileder ved Bergen, "
                "personlige analyser siden 1997. Telefonveiledning: 952 73 772."
            ),
        ),
        StaticPage(
            "telephone-guidance",
            _("Telephone Guidance"),
            "pages/telephone-guidance.html",
            description=_(
                "How telephone numerology guidance sessions with Åse Steinsland work, and what "
                "to expect from a call."
            ),
        ),
        StaticPage(
            "contact-qa",
            _("Contact / Q&A"),
            "pages/contact-qa.html",
            description=_(
                "Contact details and answers to common questions about booking a numerology "
                "reading with Åse Steinsland."
            ),
        ),
        StaticPage(
            "legal",
            _("Legal"),
            "pages/legal.html",
            description=_(
                "Legal information for the Numerologist studio, including terms and privacy "
                "policy references."
            ),
            noindex=True,
        ),
        StaticPage(
            "terms-conditions",
            _("Terms & Conditions"),
            "pages/terms-conditions.html",
            description=_(
                "Terms and conditions for bookings and services provided by the Numerologist "
                "studio."
            ),
            noindex=True,
        ),
        StaticPage(
            "privacy-policy",
            _("Privacy Policy"),
            "pages/privacy-policy.html",
            description=_(
                "How the Numerologist studio collects, uses, and protects personal data "
                "submitted through the site."
            ),
            noindex=True,
        ),
    )
}


NAVIGATION: Tuple[NavigationItem, ...] = (
    NavigationItem("calculators", _("Calculator suite")),
    NavigationItem(
        slug="discover-numerology",
        title=_("Discover Numerology"),
        children=(
            NavigationItem("pythagoras-legacy", _("Pythagoras' Legacy")),
            NavigationItem(
                "general-interpretation", _("General Interpretation of Numbers")
            ),
            NavigationItem(
                "calculation-methods-overview", _("Calculation Methods Overview")
            ),
            NavigationItem("letter-value-chart", _("Letter Value Chart")),
        ),
    ),
    NavigationItem(
        slug="personal-insights",
        title=_("Personal Insights"),
        children=(
            NavigationItem("compute-life-path-number", _("Compute Your Life Path Number")),
            NavigationItem("compute-destiny-number", _("Compute Your Destiny Number")),
            NavigationItem(
                "compute-name-vowel-consonant",
                _("Compute Name, Vowel & Consonant Numbers"),
            ),
            NavigationItem("lifes-fourth-stage", _("Life's 4th Development Stage")),
            NavigationItem(
                "realization-number", _("Realization Number — Your Ultimate Aim")
            ),
            NavigationItem("pythagoras-arrows", _("Pythagoras' Arrows")),
            NavigationItem("same-number-meaning", _("Do You See the Same Number?")),
        ),
    ),
    NavigationItem(
        slug="resources",
        title=_("Resources"),
        children=(
            NavigationItem("free-analyses", _("Free Analyses")),
            NavigationItem("projects-lab", _("Projects Lab")),
            NavigationItem("arecibo-line", _("Arecibo Line")),
            NavigationItem("blog-articles", _("Blog / Articles")),
            NavigationItem("references", _("References")),
            NavigationItem("numerologist-in-media", _("Numerologist in the Media")),
            NavigationItem("quranian-numerology", _("Quranian Numerology")),
            NavigationItem("quranic-analysis", _("Quranic Analysis")),
        ),
    ),
    NavigationItem(
        slug="guidance-support",
        title=_("Guidance & Support"),
        children=(
            NavigationItem("ase-steinsland", "Åse Karin Steinsland"),
            NavigationItem("telephone-guidance", _("Telephone Guidance")),
            NavigationItem("contact-qa", _("Contact / Q&A")),
        ),
    ),
    NavigationItem(
        slug="legal",
        title=_("Legal"),
        children=(
            NavigationItem("terms-conditions", _("Terms & Conditions")),
            NavigationItem("privacy-policy", _("Privacy Policy")),
        ),
    ),
)


def iter_navigation() -> Iterable[NavigationItem]:
    """Helper used in templates and other consumers."""

    return NAVIGATION
