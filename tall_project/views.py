from __future__ import annotations

import json

from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import LiteCalculatorForm
from .language_policy import site_language
from .navigation import STATIC_PAGES
from .number_profiles import PROFILES_EN, get_profile, meta_description
from .number_story import get_story_titles
from .related_articles import get_related_article_map, get_related_articles


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

# English profiles, kept under the old name for existing imports; the page
# itself renders the visitor's language via number_profiles.get_profile().
NUMBER_INTERPRETATIONS = PROFILES_EN


# The calculation bug (flat letter/digit summing instead of per-name-part
# reduction) is fixed — see intake/forms.py IntakeForm._reduce_name /
# _life_path. Re-activated behind a 3-digit access code (LiteCalculatorForm)
# while it's tried out with a small group before a full public launch.
CALCULATOR_PAUSED = False


def home(request: HttpRequest) -> HttpResponse:
    from articles.models import Article
    from articles.thumbnails import get_thumbnail

    form = LiteCalculatorForm(request.POST or None)
    result = None
    home_result_numbers = ()
    home_related_articles = []
    if not CALCULATOR_PAUSED and request.method == "POST" and form.is_valid():
        result = form.calculate()
        home_result_numbers = tuple(dict.fromkeys(
            value for value in result.values()
            if value in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33)
        ))
        related_map = get_related_article_map(home_result_numbers, limit=2)
        seen_slugs = set()
        for number in home_result_numbers:
            for article in related_map.get(number, []):
                if article.slug in seen_slugs:
                    continue
                seen_slugs.add(article.slug)
                home_related_articles.append(article)
                if len(home_related_articles) >= 6:
                    break
            if len(home_related_articles) >= 6:
                break
    latest_articles = list(Article.objects.all()[:3])
    for article in latest_articles:
        article.thumb = get_thumbnail(article.slug, article.title)
    context = {
        "form": form,
        "result": result,
        "calculator_paused": CALCULATOR_PAUSED,
        "latest_articles": latest_articles,
        "home_result_numbers": home_result_numbers,
        "home_related_articles": home_related_articles,
    }
    return render(request, "pages/home.html", context)


def related_articles_api(_request: HttpRequest, number: int) -> JsonResponse:
    if number not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33):
        return JsonResponse({"number": number, "articles": []})
    articles = get_related_articles(number, limit=3)
    return JsonResponse({
        "number": number,
        "articles": [
            {"title": article.title, "url": article.get_absolute_url()}
            for article in articles
        ],
    })


def number_detail(request: HttpRequest, number: int) -> HttpResponse:
    language = getattr(request, "LANGUAGE_CODE", "en")
    try:
        profile = get_profile(number, language)
    except KeyError as exc:
        raise Http404 from exc

    canonical_url = _canonical(request)
    description = meta_description(profile, language)
    faq = profile.get("faq", [])
    structured_data = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "inLanguage": {"nb": "nb-NO", "fa": "fa-IR"}.get(language, "en"),
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faq
            ],
        },
        ensure_ascii=False,
    ) if faq else _webpage_schema(profile["title"], description, canonical_url)
    sequence = [n for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33) if n in NUMBER_INTERPRETATIONS]
    position = sequence.index(number) if number in sequence else None
    prev_number = sequence[position - 1] if position else None
    next_number = sequence[position + 1] if position is not None and position + 1 < len(sequence) else None
    related_articles = get_related_articles(number, limit=8)
    context = {
        "number": number,
        "profile": profile,
        "meta_description": description,
        "canonical_url": canonical_url,
        "structured_data": structured_data,
        "prev_number": prev_number,
        "next_number": next_number,
        "story": get_story_titles(number, language),
        "hero_image": f"journey/images/number-{number}-{({1:'strengths',2:'strengths',3:'strengths',4:'practical',5:'strengths',6:'practical',7:'guidance',8:'challenges',9:'strengths',11:'strengths',22:'strengths',33:'guidance'}.get(number, 'strengths'))}-photo.webp",
        "page_title": profile["title"],
        "related_articles": related_articles,
        "related_articles_mid": related_articles[:3],
        "related_articles_more": related_articles[3:],
        "related_copy": ({
            "nb": {
                "eyebrow": "Relaterte artikler",
                "mid_title": f"Les videre om tallet {number}",
                "mid_text": "Fordyp deg i artikler som utforsker de samme mønstrene, menneskene og symbolene.",
                "more_title": f"Flere perspektiver på {number}",
                "open": "Åpne artikkel",
            },
            "fa": {
                "eyebrow": "مقاله‌های مرتبط",
                "mid_title": f"مطالعه بیشتر درباره عدد {number}",
                "mid_text": "مقاله‌هایی را بخوانید که الگوها، شخصیت‌ها و نمادهای مرتبط را عمیق‌تر بررسی می‌کنند.",
                "more_title": f"دیدگاه‌های بیشتر درباره {number}",
                "open": "باز کردن مقاله",
            },
        }.get(language, {
            "eyebrow": "Related articles",
            "mid_title": f"Read further about number {number}",
            "mid_text": "Explore articles that deepen the same patterns, people, and symbols.",
            "more_title": f"More perspectives on {number}",
            "open": "Open article",
        })),
    }
    return render(request, "pages/number-detail.html", context)


# These static pages are *about* the calculator (their whole copy promises
# "learn how to calculate X") but never actually embedded one — visitors
# hit a dead end. Both draw from the same LiteCalculatorForm/four-number
# result the homepage tool produces, so give them the real, working thing
# instead of just describing it.
SLUGS_WITH_CALCULATOR = {
    "compute-name-vowel-consonant",
    "compute-destiny-number",
    "compute-life-path-number",
    "letter-value-chart",
    "calculation-methods-overview",
}

# Which of the widget's four results to visually emphasise on a given
# landing page, since one shared form produces all four at once — a page
# built around a single number still shows the real, honest shared widget,
# just with its own number picked out.
SLUG_CALCULATOR_HIGHLIGHT = {
    "compute-life-path-number": ["life_path"],
    "compute-destiny-number": ["expression"],
    "compute-name-vowel-consonant": ["soul_urge", "personality"],
}

ASE_CALCULATOR_NUMBERS = {
    "current-name-number": 4,
    "current-vowel-number": 5,
    "birthday-number": 7,
    "cornerstone-number": 8,
    "life-path-name-bridge": 10,
    "vowel-consonant-bridge": 11,
    "balance-number": 12,
    "address-number": 13,
    "karmic-debt-number": 13,
    "karmic-lesson": 14,
    "health-profile-number": 15,
    "personal-year-number": 16,
    "personal-month-number": 17,
    "physical-transit-number": 18,
    "mental-transit-number": 19,
    "spiritual-transit-number": 20,
    "essence-number": 21,
    "pinnacle-cycles": 22,
    "life-cycles": 23,
    "maturity-number": 24,
    "challenge-numbers": 25,
    "lucky-number": 27,
    "telephone-number": 28,
}
ASE_CALCULATOR_SLUGS = set(ASE_CALCULATOR_NUMBERS) | {"partner-profile"}

NEW_CALCULATOR_COPY = {
    "no": {
        "spiritual-transit-number": ("Spirituell transitt-kalkulator", "Finn den aktive spirituelle transittbokstaven og tallet for en valgt alder fra etternavnet i fødselsnavnet."),
        "essence-number": ("Essenstall-kalkulator", "Kombiner aktive fysiske, mentale og spirituelle navnetransitter for å finne essenstallet ved en valgt alder."),
        "pinnacle-cycles": ("Fire utviklingstrinn – kalkulator", "Beregn de fire langsiktige utviklingstrinnene fra fødselsdatoen etter Åse Steinslands metode."),
        "life-cycles": ("Tre livsperioder – kalkulator", "Beregn de tre lange livsperiodene fra fødselsmåned, fødselsdag og fødselsår."),
        "maturity-number": ("Realiseringstall – kalkulator", "Beregn realiseringstallet ved å summere navnetallet og skjebnetallet."),
        "challenge-numbers": ("Fire utfordringstall – kalkulator", "Beregn de fire utfordringstallene fra forskjellene mellom redusert fødselsmåned, fødselsdag og fødselsår."),
        "lucky-number": ("Lykketall-kalkulator", "Beregn lykketallet som i Åses oversikt følger samme fødselsdatoberegning som skjebnetallet."),
        "telephone-number": ("Telefonnummer-kalkulator", "Reduser sifrene i et telefonnummer til et numerologisk tall og sammenlign det eventuelt med dine grunntall."),
        "partner-profile": ("Kompatibilitet / partnerprofil", "Sammenlign to personers navnetall og skjebnetall med Åse Steinslands kart for personlige relasjoner og arbeidsforhold."),
    },
    "fa": {
        "spiritual-transit-number": ("محاسبه‌گر ترانزیت معنوی", "حرف و عدد فعال ترانزیت معنوی را برای سن انتخابی از بخش نام خانوادگیِ نام تولد پیدا کنید."),
        "essence-number": ("محاسبه‌گر عدد جوهره", "ترانزیت‌های فعال جسمی، ذهنی و معنوی نام را ترکیب کنید تا عدد جوهره در سن انتخابی به‌دست آید."),
        "pinnacle-cycles": ("محاسبه‌گر چهار مرحله رشد", "چهار مرحله بلندمدت رشد را از تاریخ تولد بر اساس روش Åse Steinsland محاسبه کنید."),
        "life-cycles": ("محاسبه‌گر سه دوره زندگی", "سه دوره بلند زندگی را از ماه، روز و سال تولد محاسبه کنید."),
        "maturity-number": ("محاسبه‌گر عدد تحقق", "عدد تحقق یا بلوغ را از جمع عدد نام و عدد سرنوشت محاسبه کنید."),
        "challenge-numbers": ("محاسبه‌گر چهار عدد چالش", "چهار عدد چالش را از اختلاف میان ماه، روز و سال تولدِ کاهش‌یافته محاسبه کنید."),
        "lucky-number": ("محاسبه‌گر عدد شانس", "عدد شانس را که در روش Åse بر همان پایه تاریخ تولدِ عدد سرنوشت است محاسبه کنید."),
        "telephone-number": ("محاسبه‌گر عدد تلفن", "ارقام شماره تلفن را به یک عدد عددشناسی کاهش دهید و در صورت تمایل با اعداد اصلی خود مقایسه کنید."),
        "partner-profile": ("سازگاری / پروفایل شریک", "عدد نام و عدد سرنوشت دو نفر را با جدول‌های سازگاری Åse برای رابطه شخصی و کاری مقایسه کنید."),
    },
}


NEW_CALCULATOR_LEARN = {
    "no": {
        "spiritual-transit-number": {
            "what": "Den spirituelle transitten følger etternavnsdelen av fødselsnavnet. Hver bokstav er aktiv i et antall år som tilsvarer bokstavens tallverdi, og gir et tredje tidslag ved siden av fysisk og mental transitt.",
            "read": "Resultatet viser både aktiv bokstav og tallverdi. Tallet forteller også hvor mange år bokstaven er aktiv i denne runden gjennom navnet.",
            "use": "Bruk transitten som et refleksjonslag sammen med personlig år og personlig måned. Den er mest interessant når flere uavhengige deler av tallkartet peker mot samme tema.",
        },
        "essence-number": {
            "what": "Essenstallet kombinerer de aktive fysiske, mentale og spirituelle transittverdiene ved valgt alder. I Åses materiale brukes dette som en årlig påvirkning fra bursdag til bursdag.",
            "read": "De tre aktive transittene vises først hver for seg og summeres deretter. Mestertall beholdes når de oppstår i beregningen, samtidig som grunntallet gir et ekstra tolkningslag.",
            "use": "Sammenlign essenstallet med personlig år, personlig måned og grunntallene dine. Se etter gjentakelser og samspill, ikke en fast spådom.",
        },
        "pinnacle-cycles": {
            "what": "De fire utviklingstrinnene er fire lange livsfaser beregnet fra redusert fødselsdag, måned og år. De viser hvordan utviklingstemaene endrer seg gjennom livet.",
            "read": "Les resultatet som en sekvens på fire tall. Hvert tall har sin egen rolle og periode; mestertall 11 og 22 beholdes når de oppstår.",
            "use": "Bruk utviklingstrinnene som et langsiktig kart og sammenlign aktiv fase med personlig år, transitter og andre grunntall.",
        },
        "life-cycles": {
            "what": "De tre livsperiodene bygger på fødselsmåned, fødselsdag og fødselsår. De representerer en tidlig periode, en produktiv mellomperiode og en senere modningsperiode.",
            "read": "Resultatet viser tre tall med hvert sitt aldersspenn. Les både tallet og overgangen til neste periode; mestertall beholdes i disse langsyklusene.",
            "use": "Bruk periodene for å se den lange rytmen i tallkartet. Sammenlign dem med kortere sykluser for å se hvilke temaer som overlapper.",
        },
        "maturity-number": {
            "what": "Realiseringstallet beregnes ved å legge sammen navnetallet og skjebnetallet. Åse beskriver det som et underliggende mål som blir tydeligere senere i voksenlivet.",
            "read": "Du ser navnetallet og skjebnetallet separat før summen reduseres. Dersom summen blir 11, 22 eller 33, beholdes mestertallet.",
            "use": "Bruk realiseringstallet som et langsiktig perspektiv på hvordan navn og livsvei kan møtes, ikke som en fast fasit på hva du må bli.",
        },
        "challenge-numbers": {
            "what": "De fire utfordringstallene kommer fra forskjellene mellom redusert fødselsmåned, fødselsdag og fødselsår. De brukes som temaer for kvaliteter som kan kreve mer bevisst arbeid.",
            "read": "Les de fire tallene som en serie, ikke som én samlet karakter. Hvert utfordringstall peker på et eget spennings- eller læringstema.",
            "use": "Se etter situasjoner der de samme kvalitetene går igjen. Bruk tallene som refleksjon og sammenlign dem med resten av kartet.",
        },
        "lucky-number": {
            "what": "I Åses kalkulasjonsoversikt følger lykketallet samme fødselsdatoberegning som skjebnetallet. Kalkulatoren viser derfor dette tallet direkte.",
            "read": "Les resultatet gjennom samme grunntolkning som skjebnetallet. Et mestertall beholdes dersom beregningen ender i 11, 22 eller 33.",
            "use": "Bruk lykketallet som en lett numerologisk referanse når du sammenligner tall du møter eller kan velge. Det er ikke en statistisk garanti for flaks.",
        },
        "telephone-number": {
            "what": "Telefonnummeret reduseres ved å summere sifrene du skriver inn og redusere summen til 1–9. Du kan også legge inn navn og fødselsdato for å se direkte talltreff.",
            "read": "Start med telefonnummerets reduserte verdi. Hvis du la inn grunndata, viser kalkulatoren om tallet samsvarer direkte med navnetallet eller skjebnetallet.",
            "use": "Bruk resultatet som et symbolsk sammenligningslag. Et talltreff kan være interessant i numerologi, men er ikke en objektiv garanti for flaks eller resultat.",
        },
        "partner-profile": {
            "what": "Partnerprofilen beregner navnetall og skjebnetall for begge personer og slår dem opp i Åses originale 9×9-kart for personlige relasjoner eller arbeidsforhold.",
            "read": "A betyr svært harmonisk, B god, C mer blandet eller lærende, D krevende, og A/D sterk polaritet. Navnelaget og skjebnelaget vurderes separat.",
            "use": "Bruk begge sammenligningene som samtale- og refleksjonsverktøy. Et forhold består av mer enn ett tall, så resultatet er ikke en dom over om to mennesker passer sammen.",
        },
    },
    "fa": {
        "spiritual-transit-number": {
            "what": "ترانزیت معنوی بخش نام خانوادگیِ نام تولد را دنبال می‌کند. هر حرف به تعداد سال‌های برابر با ارزش عددی خود فعال می‌ماند و در کنار ترانزیت جسمی و ذهنی یک لایه زمانی سوم می‌سازد.",
            "read": "نتیجه هم حرف فعال و هم ارزش عددی آن را نشان می‌دهد. همان عدد مدت فعال‌بودن حرف را در این گردش نام مشخص می‌کند.",
            "use": "این ترانزیت را در کنار سال شخصی و ماه شخصی به‌عنوان ابزار بازتابی بخوانید؛ هم‌زمانی چند لایه مستقل مهم‌تر از یک پیش‌بینی قطعی است.",
        },
        "essence-number": {
            "what": "عدد جوهره، ارزش ترانزیت‌های فعال جسمی، ذهنی و معنوی را در سن انتخابی با هم ترکیب می‌کند و در روش Åse به‌عنوان چرخه‌ای از تولد تا تولد خوانده می‌شود.",
            "read": "سه ترانزیت ابتدا جداگانه نمایش داده می‌شوند و سپس جمع می‌شوند. اگر عدد استاد ظاهر شود حفظ می‌شود و عدد ریشه نیز لایه تکمیلی تفسیر است.",
            "use": "عدد جوهره را با سال شخصی، ماه شخصی و اعداد اصلی مقایسه کنید و به تکرار الگوها توجه کنید، نه به پیش‌بینی ثابت.",
        },
        "pinnacle-cycles": {
            "what": "چهار مرحله رشد، چهار دوره بلند زندگی هستند که از روز، ماه و سال تولدِ کاهش‌یافته محاسبه می‌شوند و تغییر موضوع‌های رشد را در طول زندگی نشان می‌دهند.",
            "read": "نتیجه را به‌صورت توالی چهار عدد بخوانید. هر عدد نقش و دوره خود را دارد و اعداد استاد ۱۱ و ۲۲ در صورت ظهور حفظ می‌شوند.",
            "use": "این مراحل را به‌عنوان نقشه بلندمدت با سال شخصی، ترانزیت‌ها و اعداد اصلی مقایسه کنید.",
        },
        "life-cycles": {
            "what": "سه دوره زندگی از ماه، روز و سال تولد ساخته می‌شوند و دوره آغازین، میانیِ سازنده و دوره پختگیِ بعدی را نشان می‌دهند.",
            "read": "سه عدد همراه با بازه سنی خود نمایش داده می‌شوند. هم عدد و هم گذار به دوره بعدی را بخوانید؛ اعداد استاد در این چرخه‌های بلند حفظ می‌شوند.",
            "use": "از این دوره‌ها برای دیدن ریتم بلندمدت نمودار استفاده کنید و آن‌ها را با چرخه‌های کوتاه‌تر مقایسه کنید.",
        },
        "maturity-number": {
            "what": "عدد تحقق از جمع عدد نام و عدد سرنوشت به‌دست می‌آید و در نوشته‌های Åse به‌عنوان هدفی زیرین توصیف می‌شود که در بزرگسالی روشن‌تر می‌گردد.",
            "read": "عدد نام و سرنوشت جداگانه نشان داده می‌شوند و سپس جمع کاهش می‌یابد. اگر حاصل ۱۱، ۲۲ یا ۳۳ باشد عدد استاد حفظ می‌شود.",
            "use": "این عدد را دیدگاهی بلندمدت برای پیوند میان نام و مسیر زندگی بدانید، نه حکمی قطعی درباره آنچه باید بشوید.",
        },
        "challenge-numbers": {
            "what": "چهار عدد چالش از اختلاف میان ماه، روز و سال تولدِ کاهش‌یافته محاسبه می‌شوند و به موضوع‌هایی اشاره دارند که ممکن است نیازمند توجه آگاهانه بیشتری باشند.",
            "read": "چهار عدد را به‌عنوان یک توالی بخوانید، نه یک امتیاز واحد. هر کدام موضوع تنش یا یادگیری جداگانه‌ای را نشان می‌دهد.",
            "use": "به موقعیت‌هایی توجه کنید که همان کیفیت‌ها تکرار می‌شوند و نتیجه را در کنار بقیه نمودار ببینید.",
        },
        "lucky-number": {
            "what": "در فهرست محاسبات Åse، عدد شانس همان پایه محاسبه تاریخ تولدِ عدد سرنوشت را دارد و این ابزار همان عدد را نشان می‌دهد.",
            "read": "نتیجه را با همان تفسیر پایه عدد سرنوشت بخوانید و اگر حاصل ۱۱، ۲۲ یا ۳۳ باشد عدد استاد را حفظ کنید.",
            "use": "عدد شانس را یک مرجع نمادین سبک بدانید، نه تضمین آماری برای خوش‌شانسی یا نتیجه.",
        },
        "telephone-number": {
            "what": "ارقام شماره تلفنی که وارد می‌کنید با هم جمع و به عدد ۱ تا ۹ کاهش داده می‌شوند. می‌توانید نام و تاریخ تولد را نیز برای بررسی تطابق مستقیم اضافه کنید.",
            "read": "ابتدا عدد کاهش‌یافته تلفن را بخوانید. اگر اطلاعات اصلی را وارد کنید، ابزار تطابق مستقیم با عدد نام یا سرنوشت را نیز نشان می‌دهد.",
            "use": "نتیجه را یک لایه نمادین مقایسه‌ای بدانید؛ تطابق عددی در عددشناسی جالب است اما تضمین عینی برای شانس یا نتیجه نیست.",
        },
        "partner-profile": {
            "what": "پروفایل شریک، عدد نام و عدد سرنوشت هر دو نفر را محاسبه و در جدول‌های اصلی ۹×۹ Åse برای روابط شخصی یا کاری مقایسه می‌کند.",
            "read": "A بسیار هماهنگ، B خوب، C ترکیبی یا آموزشی، D دشوار و A/D قطبیت قوی است. لایه نام و لایه سرنوشت جداگانه سنجیده می‌شوند.",
            "use": "هر دو مقایسه را ابزار گفت‌وگو و بازتاب بدانید. رابطه بیش از یک عدد دارد و نتیجه حکم نهایی درباره مناسب‌بودن دو نفر نیست.",
        },
    },
}

NEW_CALCULATOR_UI = {
    "no": {
        "registered_name": "Fullt registrert fødselsnavn", "age": "Alder som skal utforskes",
        "phone": "Telefonnummer", "phone_note": "Kun sifrene du skriver inn brukes i beregningen.",
        "a_name": "Person A – fullt fødselsnavn", "a_date": "Person A – fødselsdato",
        "b_name": "Person B – fullt fødselsnavn", "b_date": "Person B – fødselsdato",
        "context": "Relasjonstype", "personal": "Personlig relasjon", "work": "Arbeidsforhold",
    },
    "fa": {
        "registered_name": "نام کامل ثبت‌شده هنگام تولد", "age": "سن مورد بررسی",
        "phone": "شماره تلفن", "phone_note": "فقط رقم‌هایی که وارد می‌کنید در محاسبه استفاده می‌شوند.",
        "a_name": "فرد A – نام کامل تولد", "a_date": "فرد A – تاریخ تولد",
        "b_name": "فرد B – نام کامل تولد", "b_date": "فرد B – تاریخ تولد",
        "context": "نوع رابطه", "personal": "رابطه شخصی", "work": "رابطه کاری",
    },
    "en": {
        "registered_name": "Full registered birth name", "age": "Age to explore",
        "phone": "Telephone number", "phone_note": "Only the digits you enter are used in the calculation.",
        "a_name": "Person A — full birth name", "a_date": "Person A — date of birth",
        "b_name": "Person B — full birth name", "b_date": "Person B — date of birth",
        "context": "Relationship context", "personal": "Personal relationship", "work": "Work relationship",
    },
}


# Pages that moved; old links and search results keep working (301).
MOVED_PAGES = {
    "about-the-firm": "/ase-steinsland/",
    "quranian-numerology": "/articles/tallene-i-koranen/",
    "quranic-analysis": "/articles/tallene-i-koranen/",
}


def static_page(request: HttpRequest, slug: str) -> HttpResponse:
    if slug in MOVED_PAGES:
        return redirect(MOVED_PAGES[slug], permanent=True)
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
    if slug == "discover-numerology":
        from .journey import journey_content
        context["journey"] = journey_content(getattr(request, "LANGUAGE_CODE", "en"))
    from .learning import ase_content, learning_content

    language = getattr(request, "LANGUAGE_CODE", "en")
    if slug in {
        "discover-numerology", "general-interpretation", "letter-value-chart",
        "compute-destiny-number", "compute-life-path-number", "pythagoras-legacy",
        "compute-name-vowel-consonant", "calculation-methods-overview",
    }:
        context["ase"] = ase_content(language)
    if slug in {
        "general-interpretation", "letter-value-chart",
        "compute-destiny-number", "compute-life-path-number", "pythagoras-legacy",
        "compute-name-vowel-consonant", "calculation-methods-overview",
    }:
        context["lesson"] = learning_content(slug, language)
    if slug in SLUGS_WITH_CALCULATOR:
        form = LiteCalculatorForm(request.POST or None)
        result = None
        if not CALCULATOR_PAUSED and request.method == "POST" and form.is_valid():
            result = form.calculate()
        context["calculator_form"] = form
        context["calculator_result"] = result
        context["calculator_paused"] = CALCULATOR_PAUSED
        context["calculator_highlight"] = SLUG_CALCULATOR_HIGHLIGHT.get(slug, [])
        if result:
            numbers = tuple(dict.fromkeys(
                value for value in result.values()
                if value in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33)
            ))
            context["calculator_result_numbers"] = numbers
            related_map = get_related_article_map(numbers, limit=2)
            related_articles = []
            seen_slugs = set()
            for number in numbers:
                for article in related_map.get(number, []):
                    if article.slug in seen_slugs:
                        continue
                    seen_slugs.add(article.slug)
                    related_articles.append(article)
                    if len(related_articles) >= 6:
                        break
                if len(related_articles) >= 6:
                    break
            context["calculator_related_articles"] = related_articles
    if slug in ASE_CALCULATOR_SLUGS:
        context["calc_number"] = ASE_CALCULATOR_NUMBERS.get(slug)
        context["calc_label"] = "REL" if slug == "partner-profile" else f"{ASE_CALCULATOR_NUMBERS[slug]:02d}"
        context["calculator_related_map"] = get_related_article_map(limit=3)
        calc_lang = site_language(getattr(request, "LANGUAGE_CODE", "en"))
        localized = NEW_CALCULATOR_COPY.get(calc_lang, {}).get(slug)
        if localized:
            context["calc_title"], context["calc_description"] = localized
        context["calc_ui"] = NEW_CALCULATOR_UI.get(calc_lang, NEW_CALCULATOR_UI["en"])
        context["calc_learn"] = NEW_CALCULATOR_LEARN.get(calc_lang, {}).get(slug, {})
    return render(request, page.template_name, context)
