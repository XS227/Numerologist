"""Narrative chapter titles for the number-detail journeys.

The number profile carries the factual/numerological substance. This module
only supplies page-specific storytelling language so every number has its own
voice instead of repeating generic section headings.
"""
from __future__ import annotations

from .language_policy import site_language

NB = {
    1: {
        "strengths": "Hva eneren setter i gang.",
        "challenges": "Når viljen trenger et motspill.",
        "guidance": "Led først – men inviter andre inn.",
        "practical": "Der eneren trives i arbeid og relasjoner.",
    },
    2: {
        "strengths": "Hva toeren får mennesker til å skape sammen.",
        "challenges": "Når følsomheten trenger tydelige grenser.",
        "guidance": "Beskytt følsomheten uten å lukke deg.",
        "practical": "Der toeren skaper tillit i hverdagen.",
    },
    3: {
        "strengths": "Hva treeren kan uttrykke og åpne.",
        "challenges": "Når kreativiteten trenger retning.",
        "guidance": "Gi stemmen din en form.",
        "practical": "Der treeren får ideer til å leve.",
    },
    4: {
        "strengths": "Hva fireren kan bygge som varer.",
        "challenges": "Når strukturen trenger mer luft.",
        "guidance": "Bygg sakte nok til at det holder.",
        "practical": "Der fireren gjør kaos til struktur.",
    },
    5: {
        "strengths": "Hva femmeren kan sette i bevegelse.",
        "challenges": "Når friheten trenger et anker.",
        "guidance": "Bruk friheten til noe som betyr noe.",
        "practical": "Der femmeren trenger rom til å bevege seg.",
    },
    6: {
        "strengths": "Hva sekseren kan samle og ta vare på.",
        "challenges": "Når omsorgen må inkludere deg selv.",
        "guidance": "La ansvar og varme gå begge veier.",
        "practical": "Der sekseren skaper trygghet og tilhørighet.",
    },
    7: {
        "strengths": "Hva syveren kan avdekke i dybden.",
        "challenges": "Når dybden blir for isolert.",
        "guidance": "Gjør innsikt om til forståelse.",
        "practical": "Der syveren trenger ro til å se klart.",
    },
    8: {
        "strengths": "Hva åtteren kan få til.",
        "challenges": "Når kraft må balanseres med ansvar.",
        "guidance": "Bruk kraften til å skape varig verdi.",
        "practical": "Der åtteren gjør ambisjon til resultater.",
    },
    9: {
        "strengths": "Hva nieren kan fullføre og gi videre.",
        "challenges": "Når det er på tide å gi slipp.",
        "guidance": "Avslutt med verdighet – og frigjør plass.",
        "practical": "Der nieren gjør erfaring om til mening.",
    },
    11: {
        "strengths": "Hva mestertall 11 kan tenne i andre.",
        "challenges": "Når høy sensitivitet trenger jording.",
        "guidance": "Forankre inspirasjonen i hverdagen.",
        "practical": "Der 11 gjør følsomhet til en styrke.",
    },
    22: {
        "strengths": "Hva mestertall 22 kan gjøre virkelig.",
        "challenges": "Når den store visjonen må bli håndterbar.",
        "guidance": "Bryt visjonen ned til neste byggestein.",
        "practical": "Der 22 bygger noe større enn seg selv.",
    },
    33: {
        "strengths": "Hva mestertall 33 kan lære bort og løfte.",
        "challenges": "Når omsorg ikke må bli selvutslettelse.",
        "guidance": "Lær gjennom eksempel – uten å bære alle.",
        "practical": "Der 33 gjør omsorg til veiledning.",
    },
}

EN = {
    1: {"strengths":"What One sets in motion.","challenges":"When willpower needs a counterweight.","guidance":"Lead first — then invite others in.","practical":"Where One thrives in work and relationships."},
    2: {"strengths":"What Two helps people create together.","challenges":"When sensitivity needs clearer boundaries.","guidance":"Protect your sensitivity without closing down.","practical":"Where Two creates trust in daily life."},
    3: {"strengths":"What Three can express and unlock.","challenges":"When creativity needs direction.","guidance":"Give your voice a form.","practical":"Where Three brings ideas to life."},
    4: {"strengths":"What Four can build to last.","challenges":"When structure needs more air.","guidance":"Build slowly enough for it to hold.","practical":"Where Four turns chaos into structure."},
    5: {"strengths":"What Five can set in motion.","challenges":"When freedom needs an anchor.","guidance":"Use freedom in service of something meaningful.","practical":"Where Five needs room to move."},
    6: {"strengths":"What Six can gather, hold, and care for.","challenges":"When care must include yourself.","guidance":"Let responsibility and warmth move both ways.","practical":"Where Six creates belonging and safety."},
    7: {"strengths":"What Seven can uncover beneath the surface.","challenges":"When depth becomes isolation.","guidance":"Turn insight into understanding.","practical":"Where Seven needs quiet to see clearly."},
    8: {"strengths":"What Eight can make happen.","challenges":"When power must be balanced by responsibility.","guidance":"Use power to create lasting value.","practical":"Where Eight turns ambition into results."},
    9: {"strengths":"What Nine can complete and pass forward.","challenges":"When it is time to let go.","guidance":"Close with dignity — and make space.","practical":"Where Nine turns experience into meaning."},
    11: {"strengths":"What Master Number 11 can ignite in others.","challenges":"When high sensitivity needs grounding.","guidance":"Anchor inspiration in everyday life.","practical":"Where 11 turns sensitivity into strength."},
    22: {"strengths":"What Master Number 22 can make real.","challenges":"When the big vision must become manageable.","guidance":"Break the vision into the next building block.","practical":"Where 22 builds beyond the individual."},
    33: {"strengths":"What Master Number 33 can teach and uplift.","challenges":"When care must not become self-erasure.","guidance":"Teach by example — without carrying everyone.","practical":"Where 33 turns care into guidance."},
}

FA = {
    1: {"strengths":"عدد ۱ چه چیزی را به حرکت درمی‌آورد.","challenges":"وقتی اراده به نیروی متعادل‌کننده نیاز دارد.","guidance":"اول پیش‌قدم شو، بعد دیگران را همراه کن.","practical":"جایی که ۱ در کار و رابطه شکوفا می‌شود."},
    2: {"strengths":"عدد ۲ چه چیزی را میان آدم‌ها می‌سازد.","challenges":"وقتی حساسیت به مرزهای روشن نیاز دارد.","guidance":"از حساسیتت محافظت کن، بدون اینکه بسته شوی.","practical":"جایی که ۲ اعتماد می‌سازد."},
    3: {"strengths":"عدد ۳ چه چیزی را بیان و باز می‌کند.","challenges":"وقتی خلاقیت به جهت نیاز دارد.","guidance":"به صدایت شکل بده.","practical":"جایی که ۳ ایده‌ها را زنده می‌کند."},
    4: {"strengths":"عدد ۴ چه چیزی را ماندگار می‌سازد.","challenges":"وقتی ساختار به انعطاف بیشتری نیاز دارد.","guidance":"آن‌قدر آرام بساز که دوام بیاورد.","practical":"جایی که ۴ آشفتگی را به ساختار بدل می‌کند."},
    5: {"strengths":"عدد ۵ چه چیزی را به حرکت درمی‌آورد.","challenges":"وقتی آزادی به لنگر نیاز دارد.","guidance":"آزادی را در خدمت چیزی معنادار قرار بده.","practical":"جایی که ۵ به فضای حرکت نیاز دارد."},
    6: {"strengths":"عدد ۶ چه چیزی را گرد هم می‌آورد و نگه می‌دارد.","challenges":"وقتی مراقبت باید خودت را هم شامل شود.","guidance":"بگذار مسئولیت و گرما دوطرفه باشد.","practical":"جایی که ۶ امنیت و تعلق می‌سازد."},
    7: {"strengths":"عدد ۷ چه چیزی را در عمق آشکار می‌کند.","challenges":"وقتی عمق به انزوا تبدیل می‌شود.","guidance":"بینش را به فهم تبدیل کن.","practical":"جایی که ۷ برای دیدن روشن به سکوت نیاز دارد."},
    8: {"strengths":"عدد ۸ چه چیزی را می‌تواند محقق کند.","challenges":"وقتی قدرت باید با مسئولیت متعادل شود.","guidance":"قدرت را برای ساختن ارزش ماندگار به کار ببر.","practical":"جایی که ۸ بلندپروازی را به نتیجه تبدیل می‌کند."},
    9: {"strengths":"عدد ۹ چه چیزی را کامل می‌کند و به دیگران می‌سپارد.","challenges":"وقتی زمان رها کردن رسیده است.","guidance":"با وقار پایان بده و فضا باز کن.","practical":"جایی که ۹ تجربه را به معنا تبدیل می‌کند."},
    11: {"strengths":"عدد استاد ۱۱ چه چیزی را در دیگران روشن می‌کند.","challenges":"وقتی حساسیت زیاد به زمین‌گیری نیاز دارد.","guidance":"الهام را در زندگی روزمره ریشه‌دار کن.","practical":"جایی که ۱۱ حساسیت را به توانایی تبدیل می‌کند."},
    22: {"strengths":"عدد استاد ۲۲ چه چیزی را واقعی می‌کند.","challenges":"وقتی چشم‌انداز بزرگ باید قابل مدیریت شود.","guidance":"چشم‌انداز را به گام بعدیِ قابل ساخت تقسیم کن.","practical":"جایی که ۲۲ چیزی بزرگ‌تر از فرد می‌سازد."},
    33: {"strengths":"عدد استاد ۳۳ چه چیزی را آموزش می‌دهد و بالا می‌برد.","challenges":"وقتی مراقبت نباید به فراموش کردن خود تبدیل شود.","guidance":"با الگو بودن آموزش بده، نه با حمل کردن همه.","practical":"جایی که ۳۳ مراقبت را به راهنمایی تبدیل می‌کند."},
}



HERO = {
    "no": {
        1: "Motet til å gå først.",
        2: "Styrken i å skape sammen.",
        3: "Gleden i å uttrykke det som vil frem.",
        4: "Kunsten å bygge noe som varer.",
        5: "Friheten til å bevege og forandre.",
        6: "Omsorg som skaper trygghet og skjønnhet.",
        7: "Dybden som finner det andre overser.",
        8: "Kraft, balanse og varige resultater.",
        9: "Visdommen i å fullføre og gi videre.",
        11: "Intuisjon som tenner lys i andre.",
        22: "Visjonen som kan bli virkelig.",
        33: "Omsorg som blir til læring og løft.",
    },
    "en": {
        1: "The courage to go first.",
        2: "The strength of creating together.",
        3: "The joy of expressing what wants to emerge.",
        4: "The art of building something that lasts.",
        5: "The freedom to move and transform.",
        6: "Care that creates beauty and belonging.",
        7: "Depth that notices what others miss.",
        8: "Power, balance, and lasting results.",
        9: "The wisdom to complete and pass forward.",
        11: "Intuition that lights something in others.",
        22: "The vision that can become real.",
        33: "Care transformed into teaching and uplift.",
    },
    "fa": {
        1: "شجاعتِ اولین قدم را برداشتن.",
        2: "قدرتِ ساختن در کنار یکدیگر.",
        3: "شادیِ بیان آنچه می‌خواهد آشکار شود.",
        4: "هنرِ ساختن چیزی ماندگار.",
        5: "آزادیِ حرکت و دگرگونی.",
        6: "مراقبتی که زیبایی و تعلق می‌سازد.",
        7: "عمقی که آنچه دیگران نمی‌بینند کشف می‌کند.",
        8: "قدرت، تعادل و نتیجه‌های ماندگار.",
        9: "خردِ کامل کردن و واگذار کردن.",
        11: "شهودی که در دیگران نور روشن می‌کند.",
        22: "چشم‌اندازی که می‌تواند واقعی شود.",
        33: "مراقبتی که به آموزش و تعالی تبدیل می‌شود.",
    },
}

TITLES = {"no": NB, "en": EN, "fa": FA}

def get_story_titles(number: int, language: str | None) -> dict:
    lang = site_language(language)
    story = dict(TITLES.get(lang, EN).get(number, EN[number]))
    story["hero"] = HERO.get(lang, HERO["en"]).get(number, HERO["en"][number])
    return story
