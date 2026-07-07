from __future__ import annotations

import json

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import LiteCalculatorForm
from .navigation import STATIC_PAGES


def _canonical(request: HttpRequest) -> str:
    return request.build_absolute_uri(request.path)


def _webpage_schema(name: str, description: str, url: str) -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": name,
            "description": description,
            "url": url,
        }
    )

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
        "practical_note": "At work, number 1 thrives in founder, first-hire, or turnaround roles where someone has to go first. In relationships, the growth edge is learning to let a partner lead sometimes, not just support them.",
        "faq": [
            ("What does life path number 1 mean?", "Life path 1 points to a life built around initiative and independent leadership — starting things, not maintaining them."),
            ("Is number 1 a lucky number in numerology?", "Numerology does not treat any number as inherently lucky or unlucky. Number 1 carries a strong leadership signature, which is an asset in some situations and a challenge in others."),
        ],
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
        "practical_note": "At work, number 2 excels in mediation, partnership, and support roles where relationships determine the outcome. The growth edge is voicing a preference before resentment builds, rather than after.",
        "faq": [
            ("What does life path number 2 mean?", "Life path 2 points to a life organised around cooperation, sensitivity, and building trust between people rather than acting alone."),
            ("Is number 2 compatible with number 8?", "2 and 8 can work well together: 2's diplomacy softens 8's drive, while 8 gives 2's ideas structure and momentum — provided both sides respect the other's pace."),
        ],
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
        "practical_note": "At work, number 3 thrives in writing, teaching, performance, and any role built around communication. The growth edge is finishing the unglamorous last 20% of a project once the exciting part is done.",
        "faq": [
            ("What does life path number 3 mean?", "Life path 3 points to a life centred on creative self-expression and communicating ideas in ways that lift other people's mood."),
            ("Why does number 3 struggle to finish projects?", "3's energy is drawn to the exciting, generative phase of a project. Without added structure or an accountability partner, later, repetitive stages can lose its interest."),
        ],
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
        "practical_note": "At work, number 4 is well suited to operations, finance, engineering, and any role that rewards consistency over improvisation. The growth edge is treating an unexpected change as new information, not as a threat to the plan.",
        "faq": [
            ("What does life path number 4 mean?", "Life path 4 points to a life built through steady, practical effort — creating the systems and structures other numbers eventually rely on."),
            ("Is number 4 a difficult life path?", "Not difficult so much as demanding: 4 asks for patience and consistent work rather than quick wins, which can feel slow in a culture that rewards speed."),
        ],
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
        "practical_note": "At work, number 5 does well in sales, travel, media, and roles with genuine variety built in. The growth edge is staying with one commitment long enough to see the payoff, instead of moving on right before it arrives.",
        "faq": [
            ("What does life path number 5 mean?", "Life path 5 points to a life shaped by change, movement, and a wide range of experience rather than one fixed path."),
            ("Why does number 5 get bored so easily?", "5's core drive is variety and stimulation. Without a project big enough to keep exploring within, it will naturally look for the next new thing."),
        ],
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
        "practical_note": "At work, number 6 is drawn to healthcare, education, hospitality, and family-run businesses. The growth edge is asking for help before burnout, not after.",
        "faq": [
            ("What does life path number 6 mean?", "Life path 6 points to a life organised around responsibility for others — family, community, or a team that depends on steady care."),
            ("Why does number 6 feel responsible for everyone?", "6's core drive is harmony and care. Left unchecked, this can turn into over-functioning for people who never actually asked to be rescued."),
        ],
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
        "practical_note": "At work, number 7 fits research, analysis, and specialist expert roles that reward depth over small talk. The growth edge is sharing a half-formed idea out loud instead of waiting until it feels fully proven.",
        "faq": [
            ("What does life path number 7 mean?", "Life path 7 points to a life built around inner investigation — studying, questioning, and trusting what is discovered along the way."),
            ("Why does number 7 need so much time alone?", "7 processes the world internally. Solitude is not avoidance for this number, it is how the analysis and intuition actually get done."),
        ],
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
        "practical_note": "At work, number 8 is well suited to executive, finance, and business-ownership roles where results are measured directly. The growth edge is defining success by more than the numbers on a balance sheet.",
        "faq": [
            ("What does life path number 8 mean?", "Life path 8 points to a life focused on building material and organisational impact — resources, authority, and measurable outcomes."),
            ("Is number 8 only about money?", "No. 8 is about impact and stewardship of resources, which often shows up as financial success but is really about how well responsibility and power are handled."),
        ],
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
        "practical_note": "At work, number 9 gravitates toward humanitarian, creative, and advisory roles with a wider purpose behind them. The growth edge is closing a chapter cleanly instead of dragging it into the next one out of loyalty.",
        "faq": [
            ("What does life path number 9 mean?", "Life path 9 points to a life shaped by endings, compassion, and using accumulated experience in service of something larger than oneself."),
            ("Why does number 9 find it hard to let go?", "9 carries deep loyalty to what it has lived through. The lesson is recognising when holding on stops honouring the past and starts blocking what comes next."),
        ],
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
        "practical_note": "At work, master number 11 often finds a home in coaching, healing arts, design, and any field where sensitivity is an asset rather than a liability. The growth edge is a grounding daily routine, since 11's nervous system runs at a higher voltage than most.",
        "faq": [
            ("What does master number 11 mean?", "Master number 11 is the intuitive, inspirational amplification of number 2 — heightened sensitivity paired with the ability to communicate insight to others."),
            ("Is master number 11 always reduced to 2?", "In most calculation methods 11 is kept as a master number rather than reduced further, because it carries its own distinct, more intense profile."),
        ],
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
        "practical_note": "At work, master number 22 is drawn to large-scale building — institutions, infrastructure, or organisations meant to outlast any one person. The growth edge is breaking an enormous vision into a milestone that can realistically be finished this month.",
        "faq": [
            ("What does master number 22 mean?", "Master number 22 is the visionary-builder amplification of number 4 — the discipline of 4 combined with the capacity to think and build at a much larger scale."),
            ("Why is 22 called the 'master builder' number?", "Because it pairs big-picture vision with the practical follow-through to actually construct something lasting, rather than leaving the idea unrealised."),
        ],
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
        "practical_note": "At work, master number 33 often shows up in teaching, therapy, and community-leadership roles built around other people's growth. The growth edge is receiving support and care as readily as it gives them.",
        "faq": [
            ("What does master number 33 mean?", "Master number 33 is the compassionate-teacher amplification of number 6 — care and responsibility raised to a level focused on healing and guiding others."),
            ("Is master number 33 rare?", "Yes, relative to the other core numbers — it only appears from specific date combinations, which is part of why it is treated as a master number rather than reduced to 6."),
        ],
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

    canonical_url = _canonical(request)
    meta_description = f"{profile['title']} in numerology: {profile['essence']} Strengths, growth edges, and Åse's guidance for this number."
    faq = profile.get("faq", [])
    structured_data = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faq
            ],
        }
    ) if faq else _webpage_schema(profile["title"], meta_description, canonical_url)
    other_numbers = [n for n in NUMBER_INTERPRETATIONS if n != number]
    context = {
        "number": number,
        "profile": profile,
        "meta_description": meta_description,
        "canonical_url": canonical_url,
        "structured_data": structured_data,
        "other_numbers": other_numbers,
        "page_title": profile["title"],
    }
    return render(request, "pages/number-detail.html", context)


def static_page(request: HttpRequest, slug: str) -> HttpResponse:
    try:
        page = STATIC_PAGES[slug]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise Http404 from exc
    canonical_url = page.canonical_override or _canonical(request)
    context = {
        "page": page,
        "meta_description": str(page.description),
        "canonical_url": canonical_url,
        "structured_data": _webpage_schema(str(page.title), str(page.description), canonical_url),
        "noindex": page.noindex,
        "page_title": str(page.title),
    }
    return render(request, page.template_name, context)
