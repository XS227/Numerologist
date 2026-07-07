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
            "compute-destiny-number",
            _("Compute Your Destiny Number"),
            "pages/compute-destiny-number.html",
            description=_(
                "How to calculate your destiny number from your birth date, and what it "
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
            "about-the-firm",
            _("About the Firm"),
            "pages/about-the-firm.html",
            description=_(
                "Om Åse Karin Steinsland: bakgrunn, metode og telefonveiledning, med "
                "kontaktskjema for å komme i kontakt direkte."
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
            NavigationItem("about-the-firm", _("About the Firm")),
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
