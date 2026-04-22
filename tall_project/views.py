from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import LiteCalculatorForm
from .navigation import STATIC_PAGES

NUMBER_INTERPRETATIONS = {
    1: {
        "title": "Number 1",
        "essence": "Initiative, courage, and pioneering leadership.",
        "strengths": [
            "Steps forward quickly when a new path appears.",
            "Builds confidence in others through decisive action.",
            "Brings originality and a healthy competitive spark.",
        ],
        "challenges": [
            "Can feel isolated when carrying everything alone.",
            "May become impatient with slower collaborators.",
            "Needs to balance self-reliance with humility.",
        ],
        "ase_guidance": "Åse teaches 1-energy to lead with warmth: begin bravely, then invite others into the vision.",
    },
    2: {
        "title": "Number 2",
        "essence": "Harmony, listening, and relational intelligence.",
        "strengths": [
            "Creates calm in emotionally charged moments.",
            "Notices subtle details other people miss.",
            "Builds trust through diplomacy and consistency.",
        ],
        "challenges": [
            "Can over-adapt and silence personal needs.",
            "May hesitate too long before making a decision.",
            "Absorbs surrounding moods and stress.",
        ],
        "ase_guidance": "In Åse's method, number 2 grows strongest when sensitivity is paired with clear boundaries.",
    },
    3: {
        "title": "Number 3",
        "essence": "Expression, creativity, and joyful communication.",
        "strengths": [
            "Turns ideas into stories that inspire action.",
            "Brings optimism and social ease to groups.",
            "Learns quickly through art, language, and play.",
        ],
        "challenges": [
            "Can scatter attention across too many projects.",
            "May hide deeper feelings behind humor.",
            "Needs rhythm and discipline to finish what it starts.",
        ],
        "ase_guidance": "Åse often frames 3-energy as a healing voice: speak honestly, create often, and let joy be practical.",
    },
    4: {
        "title": "Number 4",
        "essence": "Structure, responsibility, and grounded progress.",
        "strengths": [
            "Creates systems that make big goals achievable.",
            "Shows loyalty, reliability, and practical wisdom.",
            "Thrives when building long-term foundations.",
        ],
        "challenges": [
            "Can become rigid when plans change unexpectedly.",
            "May overwork and forget rest cycles.",
            "Sometimes resists experimentation.",
        ],
        "ase_guidance": "Åse describes 4 as sacred architecture: discipline is powerful when softened with flexibility.",
    },
    5: {
        "title": "Number 5",
        "essence": "Freedom, movement, and life-force curiosity.",
        "strengths": [
            "Adapts quickly in changing environments.",
            "Brings adventure and fresh perspective.",
            "Connects diverse people and ideas.",
        ],
        "challenges": [
            "Can chase stimulation instead of depth.",
            "May struggle with repetitive routines.",
            "Needs mindful pacing to avoid burnout.",
        ],
        "ase_guidance": "In Åse's guidance, number 5 is healthiest when freedom is directed toward meaningful purpose.",
    },
    6: {
        "title": "Number 6",
        "essence": "Care, harmony, and heart-led service.",
        "strengths": [
            "Nurtures homes, teams, and communities.",
            "Holds strong values around responsibility and fairness.",
            "Brings beauty and emotional warmth into daily life.",
        ],
        "challenges": [
            "Can over-function and carry others' burdens.",
            "May become perfectionistic in relationships.",
            "Needs space for personal creativity and rest.",
        ],
        "ase_guidance": "Åse's teaching for 6 is simple: caring is sacred, but self-care is part of the same vow.",
    },
    7: {
        "title": "Number 7",
        "essence": "Inner wisdom, analysis, and spiritual depth.",
        "strengths": [
            "Observes patterns beneath surface events.",
            "Combines intuition with careful investigation.",
            "Values truth, study, and contemplative practice.",
        ],
        "challenges": [
            "Can withdraw emotionally when overwhelmed.",
            "May become overly skeptical or self-critical.",
            "Needs trust to share insights with others.",
        ],
        "ase_guidance": "Åse presents 7 as the seeker's path: question deeply, then translate insight into lived wisdom.",
    },
    8: {
        "title": "Number 8",
        "essence": "Authority, impact, and material stewardship.",
        "strengths": [
            "Leads with strategic focus and resilience.",
            "Manages resources with strong executive energy.",
            "Transforms vision into measurable outcomes.",
        ],
        "challenges": [
            "Can equate worth with productivity.",
            "May become controlling under pressure.",
            "Needs heart-centered balance in power dynamics.",
        ],
        "ase_guidance": "In Åse's lens, 8 is ethical leadership: success should support both personal and collective wellbeing.",
    },
    9: {
        "title": "Number 9",
        "essence": "Compassion, completion, and universal perspective.",
        "strengths": [
            "Holds empathy for many kinds of people.",
            "Transforms life lessons into service and guidance.",
            "Sees the bigger humanitarian picture.",
        ],
        "challenges": [
            "Can cling to past chapters out of loyalty.",
            "May feel emotionally heavy from collective concerns.",
            "Needs clear endings to begin the next cycle.",
        ],
        "ase_guidance": "Åse describes 9 as wise release: honor what was, forgive what hurts, and bless what comes next.",
    },
    11: {
        "title": "Master Number 11",
        "essence": "Illumination, intuition, and inspired communication.",
        "strengths": [
            "Acts as a bridge between insight and expression.",
            "Perceives symbolic meaning with unusual clarity.",
            "Inspires others through authentic presence.",
        ],
        "challenges": [
            "Can feel nervous-system overload from high sensitivity.",
            "May swing between confidence and self-doubt.",
            "Needs grounding rituals for steady channeling.",
        ],
        "ase_guidance": "Åse teaches 11 to ground inspiration in routine so spiritual insight becomes practical help.",
    },
    22: {
        "title": "Master Number 22",
        "essence": "Visionary building, mastery, and collective contribution.",
        "strengths": [
            "Turns large ideas into tangible structures.",
            "Balances strategy with service-minded purpose.",
            "Sustains long-term missions with discipline.",
        ],
        "challenges": [
            "Can become overwhelmed by responsibility.",
            "May fear failure when stakes feel high.",
            "Needs collaborative support to avoid isolation.",
        ],
        "ase_guidance": "In Åse's approach, 22 asks for stepwise execution: sacred vision becomes real through practical milestones.",
    },
    33: {
        "title": "Master Number 33",
        "essence": "Compassionate teaching, healing, and elevated service.",
        "strengths": [
            "Leads through empathy and moral clarity.",
            "Supports others' growth with patience and devotion.",
            "Combines creative expression with spiritual care.",
        ],
        "challenges": [
            "Can over-give and neglect personal limits.",
            "May carry unrealistic expectations of perfection.",
            "Needs regular restoration and community reciprocity.",
        ],
        "ase_guidance": "Åse frames 33 as loving mastery: teach by example, but never abandon your own healing path.",
    },
}


def home(request: HttpRequest) -> HttpResponse:
    form = LiteCalculatorForm(request.POST or None)
    result = None
    if request.method == "POST" and form.is_valid():
        result = form.calculate()
    context = {
        "form": form,
        "result": result,
    }
    return render(request, "pages/home.html", context)


def number_detail(request: HttpRequest, number: int) -> HttpResponse:
    try:
        profile = NUMBER_INTERPRETATIONS[number]
    except KeyError as exc:
        raise Http404 from exc

    context = {
        "number": number,
        "profile": profile,
    }
    return render(request, "pages/number-detail.html", context)


def static_page(request: HttpRequest, slug: str) -> HttpResponse:
    try:
        page = STATIC_PAGES[slug]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise Http404 from exc
    context = {
        "page": page,
    }
    return render(request, page.template_name, context)
