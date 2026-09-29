from __future__ import annotations

import calendar
from datetime import date
from typing import Any

from .report_engine import (
    current_age,
    destiny,
    notation,
    personal_year,
    root_digit,
    transit,
)

MONTH_NAMES = {
    "no": ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "fa": ["ژانویه", "فوریه", "مارس", "آوریل", "مه", "ژوئن", "ژوئیه", "اوت", "سپتامبر", "اکتبر", "نوامبر", "دسامبر"],
}

YEAR_TITLES = {
    "no": {1:"Ny retning",2:"Samarbeid og tålmodighet",3:"Uttrykk og skaperglede",4:"Grunnmur og disiplin",5:"Forandring og bevegelse",6:"Ansvar, nærhet og hjem",7:"Fordypning og indre søken",8:"Resultater og materiell balanse",9:"Avslutning og frigjøring"},
    "en": {1:"A new direction",2:"Cooperation and patience",3:"Expression and creativity",4:"Foundation and discipline",5:"Change and movement",6:"Responsibility, closeness and home",7:"Depth and inner search",8:"Results and material balance",9:"Completion and release"},
    "fa": {1:"مسیر تازه",2:"همکاری و صبوری",3:"بیان و خلاقیت",4:"پایه‌سازی و نظم",5:"تغییر و حرکت",6:"مسئولیت، نزدیکی و خانه",7:"درون‌نگری و جست‌وجوی عمیق",8:"نتیجه و تعادل مادی",9:"پایان و رها کردن"},
}

YEAR_TEXT = {
    "no": {
        1:"Dette er et år som ber om initiativ. Det som har vært uklart kan få en tydeligere retning når du selv tar det første steget. Nye prosjekter, nye roller eller en ny måte å stå i eget liv på kan bli viktige, men styrken ligger i å velge bevisst fremfor å skynde seg.",
        2:"Dette året arbeider mer stille. Relasjoner, samarbeid, timing og følsomhet blir viktigere enn å presse fram raske resultater. Du kommer lengst når du lytter godt, lar ting modnes og bruker diplomati uten å gi fra deg din egen retning.",
        3:"Dette er et år for uttrykk, kontakt og skapende energi. Ord, ideer og mennesker kan åpne dører, og det blir lettere å vise mer av hvem du er. Utfordringen er å samle energien godt nok til at inspirasjon også blir til noe ferdig.",
        4:"Dette året ber deg bygge. Arbeid, detaljer, økonomi, rutiner og praktiske forpliktelser kan kreve mer enn vanlig, men nettopp her ligger muligheten til å skape en grunnmur som varer. Tålmodighet og orden gir mer enn snarveier.",
        5:"Dette er et bevegelig år. Forandringer, nye kontakter, reiser eller uventede vendinger kan gjøre livet mindre forutsigbart. Fleksibilitet er en styrke nå; det viktigste er å skille mellom frihet som utvikler deg og uro som bare sprer energien.",
        6:"Dette året trekker oppmerksomheten mot mennesker du har ansvar for og det livet dere bygger sammen. Familie, hjem, kjærlighet og plikter kan komme nærmere. Du kan gjøre mye godt for andre, men må samtidig passe på at omsorg ikke blir til overansvar.",
        7:"Dette er et år for fordypning. Behovet for ro, kunnskap og større forståelse kan bli sterkere enn behovet for ytre fart. Studier, refleksjon og spesialisering støttes, mens overdreven jakt på resultater lett kan føles tom. Gi det indre arbeidet plass.",
        8:"Dette er et år der arbeid, ansvar, økonomi og resultater blir synlige. Tidligere innsats kan gi avkastning, samtidig som dårlige strukturer blir vanskeligere å overse. Ambisjon er en ressurs, men makt og penger må holdes i riktig forhold til resten av livet.",
        9:"Dette året avslutter en niårig rytme. Noe skal fullføres, forstås eller slippes før neste retning kan bli tydelig. Følelsene kan ligge nærmere overflaten, men det finnes også lettelse i å rydde plass og avslutte det som ikke lenger hører hjemme.",
    },
    "en": {
        1:"This year asks for initiative. What has been unclear can find direction when you take the first step yourself. New projects, roles or a new way of standing in your own life may matter, but the strength lies in choosing consciously rather than rushing.",
        2:"This year works more quietly. Relationships, cooperation, timing and sensitivity matter more than forcing quick results. You move further by listening carefully, allowing things to mature and using diplomacy without surrendering your own direction.",
        3:"This is a year of expression, contact and creative energy. Words, ideas and people can open doors, and it becomes easier to show more of who you are. The challenge is to gather your energy well enough for inspiration to become something finished.",
        4:"This year asks you to build. Work, details, finances, routines and practical commitments may demand more, but this is exactly where a lasting foundation can be created. Patience and order will give more than shortcuts.",
        5:"This is a mobile year. Changes, new contacts, travel or unexpected turns can make life less predictable. Flexibility is a strength now; the task is to distinguish freedom that develops you from restlessness that only scatters your energy.",
        6:"This year draws attention to the people you are responsible for and the life you build together. Family, home, love and duties may move closer. You can do much for others, but care must not turn into carrying everything yourself.",
        7:"This is a year of depth. The need for quiet, knowledge and greater understanding may be stronger than the need for outer speed. Study, reflection and specialization are supported; constant pursuit of visible results can feel empty.",
        8:"This is a year when work, responsibility, money and results become visible. Earlier effort can produce returns, while weak structures become harder to ignore. Ambition is useful, but power and money need to stay in proportion to the rest of life.",
        9:"This year completes a nine-year rhythm. Something is ready to be completed, understood or released before the next direction becomes clear. Feelings may sit closer to the surface, but there can also be relief in making room for what comes next.",
    },
    "fa": {
        1:"این سال از تو می‌خواهد آغازگر باشی. چیزی که مبهم بوده می‌تواند وقتی خودت قدم اول را برمی‌داری جهت روشن‌تری پیدا کند. پروژه، نقش یا شیوه تازه‌ای برای ایستادن روی پای خودت مهم می‌شود، اما قدرت اصلی در انتخاب آگاهانه است نه عجله.",
        2:"این سال آرام‌تر کار می‌کند. رابطه، همکاری، زمان‌بندی و حساسیت از فشار آوردن برای نتیجه سریع مهم‌تر می‌شوند. وقتی خوب گوش می‌دهی، اجازه می‌دهی موضوع‌ها جا بیفتند و با دیپلماسی پیش می‌روی، مسیر بهتر باز می‌شود.",
        3:"سال بیان، ارتباط و انرژی خلاق است. کلمات، ایده‌ها و آدم‌ها می‌توانند درها را باز کنند و نشان دادن بخش بیشتری از خودت آسان‌تر می‌شود. چالش این است که انرژی پراکنده نشود و الهام به نتیجه واقعی برسد.",
        4:"این سال از تو می‌خواهد بسازی. کار، جزئیات، پول، نظم و مسئولیت‌های عملی ممکن است بیشتر شوند، اما همین‌جا فرصت ساختن پایه‌ای محکم وجود دارد. صبر و ترتیب از میانبر نتیجه بیشتری می‌دهند.",
        5:"سال حرکت و تغییر است. آشنایی‌های تازه، سفر یا اتفاق‌های پیش‌بینی‌نشده می‌توانند برنامه‌ها را جابه‌جا کنند. انعطاف قدرت توست؛ فقط باید فرق آزادی سازنده با بی‌قراری و پراکندگی را تشخیص بدهی.",
        6:"توجه این سال به آدم‌هایی می‌رود که نسبت به آن‌ها احساس مسئولیت داری و زندگی‌ای که با آن‌ها می‌سازی. خانواده، خانه، عشق و وظیفه پررنگ‌تر می‌شوند. مراقب باش حمایت از دیگران به به‌دوش‌کشیدن همه چیز تبدیل نشود.",
        7:"این سال برای عمیق شدن است. نیاز به آرامش، دانش و فهم بیشتر ممکن است از سرعت بیرونی مهم‌تر شود. مطالعه، فکر و تخصص گرفتن حمایت می‌شوند. به کار درونی جا بده و از فشار بی‌وقفه برای نتیجه ظاهری کم کن.",
        8:"در این سال کار، مسئولیت، پول و نتیجه‌ها واضح‌تر دیده می‌شوند. تلاش گذشته می‌تواند ثمر بدهد و ساختارهای ضعیف هم خودشان را نشان می‌دهند. جاه‌طلبی مفید است، اما قدرت و پول باید در تعادل با بقیه زندگی بمانند.",
        9:"این سال یک چرخه نه‌ساله را جمع‌بندی می‌کند. چیزی باید تمام، فهمیده یا رها شود تا جهت بعدی روشن‌تر شود. احساسات نزدیک‌ترند، اما در پاک کردن فضا برای مرحله بعد سبک‌شدن هم وجود دارد.",
    },
}

MONTH_TITLES = {
    "no": {1:"Start og initiativ",2:"Takt og samarbeid",3:"Uttrykk og kontakt",4:"Orden og arbeid",5:"Bevegelse og skifte",6:"Ansvar og nærhet",7:"Ro og innsikt",8:"Resultat og balanse",9:"Fullføring og slipp"},
    "en": {1:"Start and initiative",2:"Tact and cooperation",3:"Expression and contact",4:"Order and work",5:"Movement and change",6:"Responsibility and closeness",7:"Quiet and insight",8:"Results and balance",9:"Completion and release"},
    "fa": {1:"شروع و ابتکار",2:"همکاری و ظرافت",3:"بیان و ارتباط",4:"نظم و کار",5:"حرکت و تغییر",6:"مسئولیت و نزدیکی",7:"آرامش و بینش",8:"نتیجه و تعادل",9:"تکمیل و رها کردن"},
}

MONTH_TEXT = {
    "no": {
        1:"Energien vender fremover. Dette er en god måned for å begynne, ta et tydelig initiativ og sette noe i bevegelse. Pass bare på at utålmodighet ikke får deg til å bestemme før du har sett hele bildet.",
        2:"Tempoet blir mykere og mer avhengig av andre. Samarbeid, samtaler og små nyanser betyr mye. Du kan få mer gjennomslag ved å lytte og forhandle enn ved å presse.",
        3:"Kontakten med andre blir viktigere. Kreativitet, ord, humor og synlighet får mer plass, og det kan bli lettere å formidle det du tenker. Samle ideene så de ikke bare blir gode begynnelser.",
        4:"Måneden ber om orden. Rutiner, detaljer, avtaler og praktisk arbeid trenger oppmerksomhet. Det kan kjennes langsomt, men godt håndverk nå gjør resten av perioden lettere.",
        5:"Det kommer mer bevegelse inn. Planer kan endre seg raskt, og du får mest ut av måneden når du kan justere kurs uten å miste retningen. Nye mennesker eller miljøer kan gi friske impulser.",
        6:"Relasjoner, hjem og ansvar kommer nærmere. Noen kan trenge mer av deg, samtidig som du selv trenger varme og stabilitet. Hjelp der det er riktig, men la andre eie sitt eget ansvar.",
        7:"Dette er en mer innadvendt måned. Du kan trenge stillhet, fordypning og tid til å forstå hva som egentlig foregår. Ikke forveksle lavere ytre tempo med stillstand; mye kan falle på plass under overflaten.",
        8:"Arbeid, penger, myndighet og resultater står tydeligere. Det er en måned for å ta ansvar, rydde opp og stå for verdien av det du gjør. Samtidig bør du unngå å gjøre enhver situasjon til en kamp om kontroll.",
        9:"Noe nærmer seg en avslutning. Det er lettere å se hva du har vokst fra, og det kan være nødvendig å rydde, fullføre eller gi slipp. Ikke fyll tomrommet for raskt; avslutningen har sin egen verdi.",
    },
    "en": {
        1:"The energy turns forward. This is a good month to begin, take a clear initiative and set something in motion. Guard against impatience making the decision before you have seen the whole picture.",
        2:"The pace softens and becomes more dependent on others. Cooperation, conversations and small nuances matter. You may gain more through listening and negotiation than through pressure.",
        3:"Contact with others becomes important. Creativity, words, humor and visibility have more room, making it easier to communicate what you think. Gather the ideas so they become more than good beginnings.",
        4:"The month asks for order. Routines, details, agreements and practical work need attention. It may feel slow, but careful work now makes the rest of the period easier.",
        5:"More movement enters the picture. Plans can change quickly, and you gain most by adjusting course without losing direction. New people or environments can bring fresh impulses.",
        6:"Relationships, home and responsibility move closer. Someone may need more from you while you need warmth and stability yourself. Help where it is right, but let others carry their own responsibilities.",
        7:"This is a more inward month. You may need quiet, study and time to understand what is really happening. Do not confuse a slower outer pace with stagnation; much can settle beneath the surface.",
        8:"Work, money, authority and results stand out more clearly. It is a month to take responsibility, put affairs in order and stand by the value of what you do. Avoid turning every situation into a struggle for control.",
        9:"Something approaches completion. It becomes easier to see what you have outgrown, and it may be necessary to clear, finish or release. Do not fill the empty space too quickly; completion has a value of its own.",
    },
    "fa": {
        1:"انرژی رو به جلو می‌رود. ماه خوبی برای شروع، تصمیم روشن و به‌حرکت‌درآوردن یک موضوع است. فقط نگذار عجله باعث شود قبل از دیدن تصویر کامل تصمیم بگیری.",
        2:"سرعت آرام‌تر می‌شود و نقش دیگران بیشتر است. همکاری، گفت‌وگو و ظرافت‌های کوچک اهمیت دارند. با گوش‌دادن و مذاکره معمولاً بیشتر از فشار آوردن پیش می‌روی.",
        3:"ارتباط با دیگران پررنگ‌تر می‌شود. خلاقیت، کلمات، شوخ‌طبعی و دیده‌شدن جا باز می‌کنند. ایده‌ها را جمع کن تا فقط شروع‌های خوب باقی نمانند.",
        4:"این ماه نظم می‌خواهد. برنامه روزانه، جزئیات، قراردادها و کار عملی نیاز به توجه دارند. شاید سرعت کم باشد، اما کار دقیق امروز ادامه مسیر را آسان‌تر می‌کند.",
        5:"حرکت بیشتری وارد زندگی می‌شود. برنامه‌ها ممکن است سریع عوض شوند و بهترین نتیجه زمانی است که بدون گم‌کردن جهت، مسیر را تنظیم کنی. آدم‌ها یا محیط‌های تازه می‌توانند الهام بدهند.",
        6:"رابطه، خانه و مسئولیت نزدیک‌تر می‌شوند. ممکن است کسی بیشتر به تو نیاز داشته باشد و خودت هم به گرما و ثبات احتیاج داشته باشی. کمک کن، اما مسئولیت دیگران را به جای آن‌ها حمل نکن.",
        7:"ماه درون‌گراتری است. شاید به سکوت، مطالعه و زمان برای فهمیدن آنچه واقعاً جریان دارد نیاز داشته باشی. کم‌شدن سرعت بیرونی به معنی توقف نیست؛ چیزهای زیادی زیر سطح جا می‌افتند.",
        8:"کار، پول، اختیار و نتیجه‌ها واضح‌تر می‌شوند. وقت مسئولیت‌پذیری، مرتب‌کردن امور و ایستادن پای ارزش کاری است که انجام می‌دهی. هر موقعیت را به جنگ کنترل تبدیل نکن.",
        9:"چیزی به پایان نزدیک می‌شود. راحت‌تر می‌بینی چه چیزی دیگر متعلق به مرحله فعلی نیست و ممکن است لازم باشد تمامش کنی یا رهایش کنی. جای خالی را خیلی زود پر نکن؛ پایان هم ارزش خودش را دارد.",
    },
}

ESSENCE_TEXT = {
    "no": {1:"selvstendighet og initiativ",2:"følsomhet og samarbeid",3:"uttrykk og skaperglede",4:"arbeid, orden og grunnmur",5:"forandring og frihet",6:"ansvar, kjærlighet og omsorg",7:"fordypning, kunnskap og indre søken",8:"ambisjon, resultat og materiell mestring",9:"medfølelse, avslutning og et større perspektiv"},
    "en": {1:"independence and initiative",2:"sensitivity and cooperation",3:"expression and creativity",4:"work, order and foundation",5:"change and freedom",6:"responsibility, love and care",7:"depth, knowledge and inner search",8:"ambition, results and material mastery",9:"compassion, completion and a wider perspective"},
    "fa": {1:"استقلال و ابتکار",2:"حساسیت و همکاری",3:"بیان و خلاقیت",4:"کار، نظم و پایه‌سازی",5:"تغییر و آزادی",6:"مسئولیت، عشق و مراقبت",7:"عمق، دانش و جست‌وجوی درونی",8:"جاه‌طلبی، نتیجه و مهارت مادی",9:"همدلی، پایان و نگاه گسترده‌تر"},
}


def _lang(value: str) -> str:
    return value if value in {"no", "en", "fa"} else "en"


def _add_months(start: date, offset: int) -> date:
    year = start.year + (start.month - 1 + offset) // 12
    month = (start.month - 1 + offset) % 12 + 1
    return date(year, month, 1)


def _name_parts(name: str) -> tuple[str, str, str]:
    words = [word for word in (name or "").strip().split() if word]
    if not words:
        return "", "", ""
    return words[0], " ".join(words[1:-1]) if len(words) > 2 else "", words[-1] if len(words) > 1 else ""


def _essence_for_age(name: str, age: int) -> dict[str, Any]:
    first, middle, last = _name_parts(name)
    candidates = (
        ("physical", transit(first, age) if first else None),
        ("mental", transit(middle, age) if middle else None),
        ("spiritual", transit(last, age) if last else None),
    )
    active = [{"role": role, **item} for role, item in candidates if item]
    result = notation(sum(item["value"] for item in active))
    result["transits"] = active
    return result


def _active_pinnacle(birth_date: str, age: int, pinnacles: list[dict[str, Any]]) -> dict[str, Any]:
    life = destiny(birth_date)
    root = life["root"] if life else 0
    first_end = max(0, 36 - root)
    bounds = [
        (0, first_end),
        (first_end + 1, first_end + 9),
        (first_end + 10, first_end + 18),
        (first_end + 19, None),
    ]
    for index, (start, end) in enumerate(bounds):
        if end is None or start <= age <= end:
            value = pinnacles[index] if index < len(pinnacles) else notation(0)
            return {"index": index + 1, "start": start, "end": end, "value": value}
    return {"index": 4, "start": first_end + 19, "end": None, "value": pinnacles[-1] if pinnacles else notation(0)}


def _interaction(language: str, year_number: int, month_number: int) -> str:
    if year_number == month_number:
        return {
            "no":"Måneden gjentar årets tall, så hovedtemaet blir mer konsentrert og vanskeligere å overse.",
            "en":"The month repeats the year number, concentrating the main theme and making it harder to overlook.",
            "fa":"عدد ماه با عدد سال تکرار می‌شود، بنابراین موضوع اصلی متمرکزتر و واضح‌تر احساس می‌شود.",
        }[language]
    if year_number in {1, 5, 8} and month_number in {1, 5, 8}:
        return {
            "no":"Både år og måned trekker mot handling og bevegelse; bruk kraften målrettet, ikke impulsivt.",
            "en":"Both year and month lean toward action and movement; use the force deliberately rather than impulsively.",
            "fa":"هم سال و هم ماه به سمت عمل و حرکت می‌روند؛ این نیرو را هدفمند استفاده کن، نه عجولانه.",
        }[language]
    if year_number in {2, 6, 9} and month_number in {2, 6, 9}:
        return {
            "no":"Relasjoner og følelsesmessige prioriteringer får ekstra tyngde fordi både år og måned peker mot mennesker, ansvar eller avslutning.",
            "en":"Relationships and emotional priorities gain extra weight because both year and month point toward people, responsibility or completion.",
            "fa":"رابطه‌ها و اولویت‌های احساسی پررنگ‌تر می‌شوند، چون هم سال و هم ماه به آدم‌ها، مسئولیت یا جمع‌بندی اشاره دارند.",
        }[language]
    if year_number in {4, 7} and month_number in {4, 7}:
        return {
            "no":"Dette er en mer konsentrert fase: kvalitet, fordypning og tålmodig arbeid betyr mer enn fart.",
            "en":"This is a more concentrated phase: quality, depth and patient work matter more than speed.",
            "fa":"این مرحله متمرکزتر است؛ کیفیت، عمق و کار صبورانه از سرعت مهم‌ترند.",
        }[language]
    return {
        "no":"Måneden legger et kortere lag oppå årets hovedtema. Les derfor det som skjer nå i lys av den lengre retningen, ikke som en isolert hendelse.",
        "en":"The month adds a shorter layer to the year's main theme. Read what happens now in the light of the longer direction rather than as an isolated event.",
        "fa":"ماه یک لایه کوتاه‌تر روی موضوع اصلی سال می‌گذارد. اتفاق‌های اکنون را در چارچوب مسیر بلندتر ببین، نه به‌صورت جداگانه.",
    }[language]


def build_future_report(
    data: dict[str, Any],
    profile: dict[str, Any],
    *,
    language: str = "no",
    start: date | None = None,
    months: int = 24,
) -> dict[str, Any]:
    language = _lang(language)
    start = (start or date.today()).replace(day=1)
    birth_date = str(data.get("birth_date") or "")
    birth_name = str(data.get("birth_name") or "")
    current_name = str(data.get("current_name") or birth_name)
    person = (current_name or birth_name or "Du").split()[0].title()
    try:
        born = date.fromisoformat(birth_date)
    except ValueError:
        born = start

    timeline: list[dict[str, Any]] = []
    years_seen: list[int] = []
    for offset in range(months):
        first_day = _add_months(start, offset)
        reference_day = born.day if first_day.month == born.month else 15
        reference_day = min(reference_day, calendar.monthrange(first_day.year, first_day.month)[1])
        reference = date(first_day.year, first_day.month, reference_day)
        age = current_age(birth_date, reference)
        p_year = personal_year(birth_date, first_day.year)
        p_month = root_digit(p_year + first_day.month)
        essence = _essence_for_age(birth_name, age)
        essence_root = essence["root"]
        transits = essence.get("transits", [])
        if first_day.year not in years_seen:
            years_seen.append(first_day.year)

        essence_phrase = ESSENCE_TEXT[language].get(essence_root, "")
        if language == "no":
            combined = f"{person}, essensen {essence['label']} legger samtidig vekt på {essence_phrase}."
        elif language == "fa":
            combined = f"{person}، اسنس {essence['label']} هم‌زمان روی {essence_phrase} تأکید می‌کند."
        else:
            combined = f"{person}, Essence {essence['label']} simultaneously emphasizes {essence_phrase}."

        timeline.append({
            "index": offset + 1,
            "year": first_day.year,
            "month": first_day.month,
            "month_name": MONTH_NAMES[language][first_day.month - 1],
            "personal_year": p_year,
            "personal_month": p_month,
            "title": MONTH_TITLES[language][p_month],
            "body": f"{MONTH_TEXT[language][p_month]} {_interaction(language, p_year, p_month)} {combined}",
            "age": age,
            "essence": essence,
            "transits": transits,
            "is_birthday_month": first_day.month == born.month,
        })

    year_cards = []
    for year in years_seen:
        number = personal_year(birth_date, year)
        year_cards.append({
            "year": year,
            "number": number,
            "title": YEAR_TITLES[language][number],
            "body": YEAR_TEXT[language][number],
        })

    groups = []
    for year in years_seen:
        groups.append({"year": year, "months": [item for item in timeline if item["year"] == year]})

    current_age_value = current_age(birth_date, start)
    active_pinnacle = _active_pinnacle(birth_date, current_age_value, profile.get("pinnacles", []))
    pinnacle_number = active_pinnacle["value"]["root"]
    long_text = {
        "no": f"Du står nå i utviklingstrinn {active_pinnacle['index']} med tallet {active_pinnacle['value']['label']}. Dette er det langsomme bakteppet. De personlige årene og månedene nedenfor viser hvordan kortere rytmer beveger seg innenfor denne større perioden.",
        "en": f"You are now in Pinnacle {active_pinnacle['index']} with number {active_pinnacle['value']['label']}. This is the slower background. The personal years and months below show how shorter rhythms move within this larger period.",
        "fa": f"اکنون در مرحله رشد {active_pinnacle['index']} با عدد {active_pinnacle['value']['label']} قرار داری. این لایه پس‌زمینه آهسته‌تر است و سال‌ها و ماه‌های شخصی نشان می‌دهند ریتم‌های کوتاه‌تر درون آن چگونه حرکت می‌کنند.",
    }[language]

    if language == "no":
        method_intro = "Personlig år følger kalenderåret fra januar til desember. Essenstallet følger navnets aktive transitter og merkes sterkest fra fødselsdag til fødselsdag. Derfor kan en ekte 24-måneders periode berøre tre forskjellige personlige år når rapporten starter midt i et kalenderår."
        synthesis = f"{person}, perioden begynner med personlig måned {timeline[0]['personal_month']} i personlig år {timeline[0]['personal_year']} og beveger seg gjennom 24 måneder frem til personlig måned {timeline[-1]['personal_month']} i år {timeline[-1]['personal_year']}. Les utviklingen som en fortelling: det langsomme utviklingstrinnet {active_pinnacle['value']['label']} ligger under, mens år, måned og essens skifter tempo og fokus."
    elif language == "fa":
        method_intro = "سال شخصی از ژانویه تا دسامبر با سال تقویمی حرکت می‌کند. اسنس از ترانزیت‌های فعال نام ساخته می‌شود و از تولد تا تولد قوی‌تر احساس می‌شود. به همین دلیل یک دوره واقعی ۲۴ ماهه که وسط سال شروع می‌شود ممکن است سه سال شخصی مختلف را در بر بگیرد."
        synthesis = f"{person}، این دوره با ماه شخصی {timeline[0]['personal_month']} در سال شخصی {timeline[0]['personal_year']} شروع می‌شود و ۲۴ ماه بعد به ماه شخصی {timeline[-1]['personal_month']} در سال {timeline[-1]['personal_year']} می‌رسد. آن را مثل یک داستان بخوان: مرحله بلندمدت {active_pinnacle['value']['label']} در پس‌زمینه است و سال، ماه و اسنس سرعت و تمرکز را تغییر می‌دهند."
    else:
        method_intro = "The Personal Year follows the calendar year from January through December. Essence follows the active name transits and is felt most strongly from birthday to birthday. A true 24-month period can therefore touch three different Personal Years when the report begins part-way through a calendar year."
        synthesis = f"{person}, the period begins with Personal Month {timeline[0]['personal_month']} in Personal Year {timeline[0]['personal_year']} and moves through 24 months to Personal Month {timeline[-1]['personal_month']} in year {timeline[-1]['personal_year']}. Read it as a story: Pinnacle {active_pinnacle['value']['label']} forms the slow background while year, month and Essence change pace and focus."

    return {
        "person": person,
        "start": timeline[0] if timeline else None,
        "end": timeline[-1] if timeline else None,
        "years": year_cards,
        "timeline": timeline,
        "groups": groups,
        "active_pinnacle": active_pinnacle,
        "pinnacle_number": pinnacle_number,
        "method_intro": method_intro,
        "synthesis": synthesis,
    }
