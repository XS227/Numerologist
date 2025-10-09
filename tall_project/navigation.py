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


@dataclass(frozen=True)
class NavigationItem:
    """Navigation structure with optional nested children."""

    slug: str
    title: str
    children: Tuple["NavigationItem", ...] = ()


STATIC_PAGES: Dict[str, StaticPage] = {
    page.slug: page
    for page in (
        StaticPage("discover-numerology", _("Discover Numerology"), "pages/discover-numerology.html"),
        StaticPage("pythagoras-legacy", _("Pythagoras' Legacy"), "pages/pythagoras-legacy.html"),
        StaticPage(
            "general-interpretation",
            _("General Interpretation of Numbers"),
            "pages/general-interpretation.html",
        ),
        StaticPage(
            "calculation-methods-overview",
            _("Calculation Methods Overview"),
            "pages/calculation-methods-overview.html",
        ),
        StaticPage(
            "letter-value-chart",
            _("Letter Value Chart"),
            "pages/letter-value-chart.html",
        ),
        StaticPage("personal-insights", _("Personal Insights"), "pages/personal-insights.html"),
        StaticPage(
            "compute-destiny-number",
            _("Compute Your Destiny Number"),
            "pages/compute-destiny-number.html",
        ),
        StaticPage(
            "compute-name-vowel-consonant",
            _("Compute Name, Vowel & Consonant Numbers"),
            "pages/compute-name-vowel-consonant.html",
        ),
        StaticPage(
            "lifes-fourth-stage",
            _("Life's 4th Development Stage"),
            "pages/lifes-fourth-stage.html",
        ),
        StaticPage(
            "realization-number",
            _("Realization Number — Your Ultimate Aim"),
            "pages/realization-number.html",
        ),
        StaticPage(
            "pythagoras-arrows",
            _("Pythagoras' Arrows"),
            "pages/pythagoras-arrows.html",
        ),
        StaticPage(
            "same-number-meaning",
            _("Do You See the Same Number?"),
            "pages/same-number-meaning.html",
        ),
        StaticPage("resources", _("Resources"), "pages/resources.html"),
        StaticPage("free-analyses", _("Free Analyses"), "pages/free-analyses.html"),
        StaticPage("blog-articles", _("Blog / Articles"), "pages/blog-articles.html"),
        StaticPage("references", _("References"), "pages/references.html"),
        StaticPage(
            "numerologist-in-media",
            _("Numerologist in the Media"),
            "pages/numerologist-in-media.html",
        ),
        StaticPage("guidance-support", _("Guidance & Support"), "pages/guidance-support.html"),
        StaticPage("about-the-firm", _("About the Firm"), "pages/about-the-firm.html"),
        StaticPage("telephone-guidance", _("Telephone Guidance"), "pages/telephone-guidance.html"),
        StaticPage("contact-qa", _("Contact / Q&A"), "pages/contact-qa.html"),
        StaticPage("legal", _("Legal"), "pages/legal.html"),
        StaticPage("terms-conditions", _("Terms & Conditions"), "pages/terms-conditions.html"),
        StaticPage("privacy-policy", _("Privacy Policy"), "pages/privacy-policy.html"),
    )
}


NAVIGATION: Tuple[NavigationItem, ...] = (
    NavigationItem(
        slug="discover-numerology",
        title=_("Discover Numerology"),
        children=(
            NavigationItem("pythagoras-legacy", _("Pythagoras' Legacy")),
            NavigationItem("general-interpretation", _("General Interpretation of Numbers")),
            NavigationItem("calculation-methods-overview", _("Calculation Methods Overview")),
            NavigationItem("letter-value-chart", _("Letter Value Chart")),
        ),
    ),
    NavigationItem(
        slug="personal-insights",
        title=_("Personal Insights"),
        children=(
            NavigationItem("compute-destiny-number", _("Compute Your Destiny Number")),
            NavigationItem("compute-name-vowel-consonant", _("Compute Name, Vowel & Consonant Numbers")),
            NavigationItem("lifes-fourth-stage", _("Life's 4th Development Stage")),
            NavigationItem("realization-number", _("Realization Number — Your Ultimate Aim")),
            NavigationItem("pythagoras-arrows", _("Pythagoras' Arrows")),
            NavigationItem("same-number-meaning", _("Do You See the Same Number?")),
        ),
    ),
    NavigationItem(
        slug="resources",
        title=_("Resources"),
        children=(
            NavigationItem("free-analyses", _("Free Analyses")),
            NavigationItem("blog-articles", _("Blog / Articles")),
            NavigationItem("references", _("References")),
            NavigationItem("numerologist-in-media", _("Numerologist in the Media")),
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

