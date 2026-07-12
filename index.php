<?php
declare(strict_types=1);

// ── Language ────────────────────────────────────────────────────────────────
if (isset($_GET['lang'])) {
    $l = (string) $_GET['lang'];
    if (in_array($l, ['no', 'en'], true)) {
        setcookie('nl_lang', $l, [
            'expires'  => time() + 31_536_000,
            'path'     => '/',
            'samesite' => 'Lax',
            'secure'   => true,
        ]);
    }
    header('Location: /');
    exit;
}
$lang = $_COOKIE['nl_lang'] ?? 'no';
if (!in_array($lang, ['no', 'en'], true)) $lang = 'no';
$no = ($lang === 'no');

// Payment/packages are paused for now — the pricing grid and its "order"
// CTAs are hidden until this is switched back on. Nothing here is deleted.
const SHOW_PRICING = false;

// ── Today's number ──────────────────────────────────────────────────────────
function daily_reduce(int $n): int
{
    static $m = [11, 22, 33];
    while ($n > 9 && !in_array($n, $m, true)) {
        $n = (int) array_sum(array_map('intval', str_split((string) $n)));
    }
    return $n;
}

$tz       = new DateTimeZone('Europe/Oslo');
$now      = new DateTimeImmutable('now', $tz);
$todayNum = daily_reduce(
    (int) array_sum(array_map('intval', str_split($now->format('dmY'))))
);

$noMon = ['januar','februar','mars','april','mai','juni','juli','august','september','oktober','november','desember'];
$enMon = ['January','February','March','April','May','June','July','August','September','October','November','December'];
$mi    = (int) $now->format('n') - 1;
$dateLabel = $no
    ? $now->format('j') . '. ' . $noMon[$mi] . ' ' . $now->format('Y')
    : $enMon[$mi] . ' ' . $now->format('j') . ', ' . $now->format('Y');

// ── Number data ─────────────────────────────────────────────────────────────
$numData = [
    'no' => [
        1  => ['Tall 1',        'Nye begynnelser · Initiativ · Lederskap'],
        2  => ['Tall 2',        'Samarbeid · Sensitivitet · Balanse'],
        3  => ['Tall 3',        'Kreativitet · Glede · Selvuttrykk'],
        4  => ['Tall 4',        'Stabilitet · Struktur · Pålitelighet'],
        5  => ['Tall 5',        'Frihet · Forandring · Eventyr'],
        6  => ['Tall 6',        'Omsorg · Ansvar · Harmoni'],
        7  => ['Tall 7',        'Analyse · Intuisjon · Indre søken'],
        8  => ['Tall 8',        'Makt · Overflod · Materiell mestring'],
        9  => ['Tall 9',        'Medfølelse · Fullføring · Visdom'],
        11 => ['Mestertall 11', 'Inspirasjon · Intuisjon · Åndelig oppvåkning'],
        22 => ['Mestertall 22', 'Visjonær bygging · Kollektivt bidrag'],
        33 => ['Mestertall 33', 'Healing · Undervisning · Kosmisk tjeneste'],
    ],
    'en' => [
        1  => ['Number 1',  'New beginnings · Initiative · Leadership'],
        2  => ['Number 2',  'Cooperation · Sensitivity · Balance'],
        3  => ['Number 3',  'Creativity · Joy · Self-expression'],
        4  => ['Number 4',  'Stability · Structure · Reliability'],
        5  => ['Number 5',  'Freedom · Change · Adventure'],
        6  => ['Number 6',  'Care · Responsibility · Harmony'],
        7  => ['Number 7',  'Analysis · Intuition · Inner seeking'],
        8  => ['Number 8',  'Power · Abundance · Material mastery'],
        9  => ['Number 9',  'Compassion · Completion · Wisdom'],
        11 => ['Master 11', 'Inspiration · Intuition · Spiritual awakening'],
        22 => ['Master 22', 'Visionary building · Collective contribution'],
        33 => ['Master 33', 'Healing · Teaching · Cosmic service'],
    ],
];
[$todayTitle, $todayEssence] = $numData[$lang][$todayNum] ?? $numData[$lang][1];

// ── Calculator (PHP fallback for no-JS) ─────────────────────────────────────
require_once __DIR__ . '/includes/data.php';
$calcResult = null;
$calcError  = null;
$calcName   = '';
$calcDate   = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $calcName = trim((string) ($_POST['full_name'] ?? ''));
    $calcDate = (string) ($_POST['birth_date'] ?? '');
    if ($calcName === '' || $calcDate === '') {
        $calcError = $no
            ? 'Fyll inn fullt navn og fødselsdato.'
            : 'Please enter your full name and date of birth.';
    } else {
        $calcResult = calculate_numerology($calcName, $calcDate);
    }
}

// ── Translations ─────────────────────────────────────────────────────────────
$T = $no ? [
    'html_lang'       => 'no',
    'title'           => 'Numerologist – Åse Steinsland | Forstå livet gjennom tallenes energi',
    'meta_desc'       => 'Åse Steinsland er Norges fremste numerolog. Beregn ditt livsveitall, uttrykkstall, sjelstall og personlighetstall gratis, og les mer om hva de betyr for deg.',
    'og_title'        => 'Numerologist – Åse Steinsland',
    'nav_about'       => 'Om numerologi',
    'nav_services'    => 'Tjenester',
    'nav_articles'    => 'Artikler',
    'nav_contact'     => 'Kontakt',
    'nav_cta'         => 'Kontakt Åse',
    'hero_eyebrow'    => 'Norges fremste numerolog',
    'hero_h1_a'       => 'Forstå livet ditt gjennom',
    'hero_h1_b'       => 'tallenes energi',
    'hero_sub'        => 'Åse Steinsland hjelper deg å kartlegge din livssti, dine medfødte styrker og ditt potensial – gjennom en dyptgående numerologisk analyse.',
    'hero_cta1'       => 'Beregn dine tall ↓',
    'hero_cta2'       => 'Møt Åse',
    'hero_trust1'     => '20+ år erfaring',
    'hero_trust2'     => 'Tusenvis av analyser',
    'hero_trust3'     => 'Norsk & internasjonal klientbase',
    'tn_eyebrow'      => 'Daglig universell vibrasjon',
    'tn_badge'        => 'Dagens tall',
    'calc_title'      => 'Beregn dine kjernetal',
    'calc_sub'        => 'Skriv inn fullt navn og fødselsdato for å se dine fire kjernetal øyeblikkelig.',
    'calc_name'       => 'Fullt navn (som ved fødsel)',
    'calc_date'       => 'Fødselsdato',
    'calc_submit'     => 'Beregn nå',
    'calc_lp'         => 'Livsveistall',
    'calc_ex'         => 'Uttrykkstall',
    'calc_su'         => 'Sjelstall',
    'calc_pe'         => 'Personlighet',
    'calc_aside_h'    => 'Hva forteller tallene?',
    'calc_aside_p'    => 'De fire kjernetallene gir et komplett øyeblikksbilde av din numerologiske profil. Livsveistallet er din overordnede livssti. Uttrykkstallet viser din naturlige begavelse. Sjelstallet avslører dine innerste ønsker. Personlighetstallet er det første inntrykket du gir andre.',
    'calc_aside_cta'  => 'Bestill fullstendig analyse →',
    'calc_result_h'     => 'Dette forteller tallene dine',
    'calc_result_intro' => 'Sammen tegner disse fire tallene et bilde av hvem du er:',
    'calc_result_outro' => 'Bruk dette som et utgangspunkt for å bli bedre kjent med deg selv — snakk gjerne med Åse for en dypere personlig gjennomgang.',
    'master_badge'      => '✨ Mestertall oppdaget',
    'number_meanings' => [
        1  => ['essence' => 'initiativ, mot og pionerånd'],
        2  => ['essence' => 'samarbeidsevne, sensitivitet og balanse'],
        3  => ['essence' => 'kreativitet, glede og selvuttrykk'],
        4  => ['essence' => 'stabilitet, struktur og pålitelighet'],
        5  => ['essence' => 'frihet, forandring og eventyrlyst'],
        6  => ['essence' => 'omsorg, ansvar og harmoni'],
        7  => ['essence' => 'analytisk innsikt og indre søken'],
        8  => ['essence' => 'handlekraft, overflod og materiell mestring'],
        9  => ['essence' => 'medfølelse, fullføring og visdom'],
        11 => ['essence' => 'inspirasjon, intuisjon og åndelig oppvåkning',
               'master'  => 'Mestertallet 11 er et av bare tre mestertall i numerologien. Det bærer en forsterket, mer intens vibrasjon enn andre tall, og peker mot en person med usedvanlig intuisjon og evne til å inspirere andre — men også et nervesystem som trenger ekstra ro og jording.'],
        22 => ['essence' => 'visjonær bygging og evnen til å skape noe varig',
               'master'  => 'Mestertallet 22 kalles «mesterbyggeren» og er et av bare tre mestertall i numerologien. Det forener en stor visjon med evnen til faktisk å bygge den — men kan også oppleves som et tungt ansvar å bære.'],
        33 => ['essence' => 'healende kraft, undervisning og kosmisk omsorg',
               'master'  => 'Mestertallet 33 kalles «den kosmiske læreren» og er det sjeldneste av de tre mestertallene. Det peker mot en dyp evne til å helbrede og løfte andre — men krever at du også tar like god vare på deg selv.'],
    ],
    'about_eyebrow'   => 'Om Åse Steinsland',
    'about_h'         => 'Møt Norges fremste numerolog',
    'about_p1'        => 'Med over 20 års dyp erfaring innen numerologi har Åse Steinsland hjulpet tusenvis av mennesker til å forstå seg selv bedre gjennom tallenes visdom.',
    'about_p2'        => 'Hennes metode kombinerer klassisk Pythagoreisk numerologi med moderne psykologisk innsikt, og gir analyser som er like presise som de er personlige.',
    'about_cta'       => 'Les mer om Åse →',
    'cred1' => '20+ år erfaring', 'cred2' => 'Pythagoreisk metode',
    'cred3' => 'Norsk & internasjonal', 'cred4' => 'Mestertallspesialist',
    'srv_eyebrow'  => 'Tjenester',
    'srv_h'        => 'Velg din analyse',
    'srv_sub'      => 'Hver pakke er skreddersydd for din livssituasjon og dine mål.',
    'srv_popular'  => '★ Mest populær',
    'services' => [
        [
            'name'  => 'Grunnpakke',
            'price' => '490',
            'desc'  => 'Perfekt for deg som ønsker en innføring i ditt numerologiske kart.',
            'items' => ['Livsveisanalyse','Uttrykkstall','Sjelstall','Skriftlig rapport (5–8 sider)','E-postveiledning'],
            'cta'   => 'Bestill Grunnpakke',
        ],
        [
            'name'  => 'Fullstendig profil',
            'price' => '990',
            'desc'  => 'En dyptgående analyse av hele ditt numerologiske kart med personlig konsultasjon.',
            'items' => ['Alt i Grunnpakke','Personlighets- og karmatal','Personlige årstall 2025–2027','Pytagoreiske piler','Rapport 15–20 sider','30 min videokonsultasjon'],
            'cta'   => 'Velg Fullstendig profil',
            'featured' => true,
        ],
        [
            'name'  => 'Årsanalyse',
            'price' => '1 490',
            'desc'  => 'Dypdykk i ditt personlige år, månedlige sykluser og timing.',
            'items' => ['Alt i Fullstendig profil','Måned-for-måned analyse','Fokusområder og timing','Prioritert support i 3 mnd','60 min videokonsultasjon'],
            'cta'   => 'Bestill Årsanalyse',
        ],
    ],
    'art_eyebrow' => 'Fra bloggen',
    'art_h'       => 'Siste artikler',
    'art_sub'     => 'Dybdeartikler om tall, mønstre og numerologisk innsikt.',
    'art_all'     => 'Se alle artikler →',
    'art_read'    => 'Les artikkel',
    'testimonials_eyebrow' => 'Referanser',
    'testimonials_h'       => 'Hva kundene sier',
    'testimonials' => [
        [
            'text' => 'Analysen fra Åse fikk meg til å forstå hvorfor jeg alltid har søkt etter frihet. Livsveitallet mitt, 5, beskriver meg som om Åse har kjent meg i årevis.',
            'name' => 'Maria K.',
            'loc'  => 'Oslo',
            'init' => 'MK',
        ],
        [
            'text' => 'Jeg var skeptisk til numerologi, men etter å ha lest rapporten min forstod jeg at dette er et genuint verktøy for selvkunnskap. Absolutt verdt hvert eneste øre.',
            'name' => 'Thomas B.',
            'loc'  => 'Bergen',
            'init' => 'TB',
        ],
        [
            'text' => 'Årsanalysen hjalp meg med timing. Jeg tok store avgjørelser i de periodene Åse pekte ut, og alt gikk mye bedre enn jeg hadde turt å håpe.',
            'name' => 'Layla H.',
            'loc'  => 'Stavanger',
            'init' => 'LH',
        ],
    ],
    'cta_h'       => 'Klar til å utforske ditt tallkart?',
    'cta_sub'     => 'Beregn dine kjernetal gratis, og les mer om hva de forteller om deg.',
    'cta_btn1'    => 'Beregn dine tall gratis',
    'cta_btn2'    => 'Kontakt Åse',
    'footer_tag'  => 'Norges fremste numerolog, basert i Oslo. Vi hjelper deg å forstå deg selv gjennom tallenes visdom.',
    'footer_h1'   => 'Utforsk', 'footer_h2' => 'Informasjon',
    'footer_l1'   => [['Kalkulatorer','/calculators/'],['Om numerologi','/discover-numerology/'],['Møt Åse','/about-the-firm/']],
    'footer_l2'   => [['Om numerologi','/discover-numerology/'],['Kalkulatorer','/calculators/'],['Artikler','/articles/'],['Personvern','/privacy-policy/']],
    'footer_copy' => '© ' . date('Y') . ' Åse Steinsland · Numerologist',
    'footer_ethos'=> 'Der tall og teknologi jobber sammen — den pytagoreiske metoden, beregnet i Python. Riktig beregning, riktig teknologi.',
] : [
    'html_lang'       => 'en',
    'title'           => 'Numerologist – Åse Steinsland | Understand Life Through Numbers',
    'meta_desc'       => 'Åse Steinsland is Norway\'s leading numerologist. Calculate your life path, expression, soul urge, and personality numbers for free, and discover what they reveal about you.',
    'og_title'        => 'Numerologist – Åse Steinsland',
    'nav_about'       => 'About numerology',
    'nav_services'    => 'Services',
    'nav_articles'    => 'Articles',
    'nav_contact'     => 'Contact',
    'nav_cta'         => 'Contact Åse',
    'hero_eyebrow'    => 'Norway\'s leading numerologist',
    'hero_h1_a'       => 'Understand your life through',
    'hero_h1_b'       => 'the energy of numbers',
    'hero_sub'        => 'Åse Steinsland helps you map your life path, innate strengths and potential — through a deep numerological analysis tailored to you.',
    'hero_cta1'       => 'Calculate your numbers ↓',
    'hero_cta2'       => 'Meet Åse',
    'hero_trust1'     => '20+ years experience',
    'hero_trust2'     => 'Thousands of readings',
    'hero_trust3'     => 'Norwegian & international clients',
    'tn_eyebrow'      => 'Universal daily vibration',
    'tn_badge'        => 'Today\'s number',
    'calc_title'      => 'Calculate your core numbers',
    'calc_sub'        => 'Enter your full name and date of birth to instantly see your four core numbers.',
    'calc_name'       => 'Full name (as at birth)',
    'calc_date'       => 'Date of birth',
    'calc_submit'     => 'Calculate now',
    'calc_lp'         => 'Life Path',
    'calc_ex'         => 'Expression',
    'calc_su'         => 'Soul Urge',
    'calc_pe'         => 'Personality',
    'calc_aside_h'    => 'What do the numbers mean?',
    'calc_aside_p'    => 'Your four core numbers give a complete snapshot of your numerological profile. The Life Path is your overarching life theme. The Expression number reveals your natural talents. The Soul Urge shows your innermost desires. The Personality number is the first impression you make on others.',
    'calc_aside_cta'  => 'Order a full analysis →',
    'calc_result_h'     => 'What your numbers reveal',
    'calc_result_intro' => 'Together, these four numbers paint a picture of who you are:',
    'calc_result_outro' => 'Use this as a starting point for getting to know yourself better — talk to Åse for a deeper personal reading.',
    'master_badge'      => '✨ Master number detected',
    'number_meanings' => [
        1  => ['essence' => 'initiative, courage, and pioneering leadership'],
        2  => ['essence' => 'cooperation, sensitivity, and balance'],
        3  => ['essence' => 'creativity, joy, and self-expression'],
        4  => ['essence' => 'stability, structure, and reliability'],
        5  => ['essence' => 'freedom, change, and a spirit of adventure'],
        6  => ['essence' => 'care, responsibility, and harmony'],
        7  => ['essence' => 'analytical insight and inner searching'],
        8  => ['essence' => 'drive, abundance, and material mastery'],
        9  => ['essence' => 'compassion, completion, and wisdom'],
        11 => ['essence' => 'inspiration, intuition, and spiritual awakening',
               'master'  => "Master number 11 is one of only three master numbers in numerology. It carries an amplified, more intense vibration than other numbers, and points to unusual intuition and the ability to inspire others — though it also asks for extra grounding and calm."],
        22 => ['essence' => 'visionary building and the ability to create something lasting',
               'master'  => "Master number 22 is known as the \"master builder\" and is one of only three master numbers in numerology. It combines a big vision with the ability to actually build it — though it can also feel like a heavy responsibility to carry."],
        33 => ['essence' => 'healing power, teaching, and cosmic care',
               'master'  => "Master number 33 is known as the \"cosmic teacher\" and is the rarest of the three master numbers. It points to a deep capacity to heal and uplift others — but asks that you care for yourself just as generously."],
    ],
    'about_eyebrow'   => 'About Åse Steinsland',
    'about_h'         => 'Meet Norway\'s leading numerologist',
    'about_p1'        => 'With over 20 years of deep experience in numerology, Åse Steinsland has helped thousands of people better understand themselves through the wisdom of numbers.',
    'about_p2'        => 'Her method combines classical Pythagorean numerology with modern psychological insight, producing readings that are as precise as they are personal.',
    'about_cta'       => 'Read more about Åse →',
    'cred1' => '20+ years experience', 'cred2' => 'Pythagorean method',
    'cred3' => 'Norwegian & international', 'cred4' => 'Master number specialist',
    'srv_eyebrow'  => 'Services',
    'srv_h'        => 'Choose your analysis',
    'srv_sub'      => 'Each package is tailored to your life situation and goals.',
    'srv_popular'  => '★ Most popular',
    'services' => [
        [
            'name'  => 'Starter',
            'price' => '490',
            'desc'  => 'Perfect if you want an introduction to your numerological chart.',
            'items' => ['Life path analysis','Expression number','Soul urge','Written report (5–8 pages)','Email guidance'],
            'cta'   => 'Order Starter',
        ],
        [
            'name'  => 'Full Profile',
            'price' => '990',
            'desc'  => 'A deep-dive analysis of your complete numerological chart with personal consultation.',
            'items' => ['Everything in Starter','Personality & karma numbers','Personal years 2025–2027','Pythagorean arrows','Report 15–20 pages','30 min video consultation'],
            'cta'   => 'Choose Full Profile',
            'featured' => true,
        ],
        [
            'name'  => 'Year Analysis',
            'price' => '1 490',
            'desc'  => 'Deep dive into your personal year, monthly cycles and optimal timing.',
            'items' => ['Everything in Full Profile','Month-by-month analysis','Focus areas and timing','Priority support for 3 months','60 min video consultation'],
            'cta'   => 'Order Year Analysis',
        ],
    ],
    'art_eyebrow' => 'From the blog',
    'art_h'       => 'Latest articles',
    'art_sub'     => 'In-depth articles on numbers, patterns and numerological insight.',
    'art_all'     => 'See all articles →',
    'art_read'    => 'Read article',
    'testimonials_eyebrow' => 'References',
    'testimonials_h'       => 'What clients say',
    'testimonials' => [
        [
            'text' => 'Åse\'s analysis helped me understand why I have always sought freedom. My life path number 5 describes me as if she has known me for years.',
            'name' => 'Maria K.',
            'loc'  => 'Oslo',
            'init' => 'MK',
        ],
        [
            'text' => 'I was sceptical about numerology, but after reading my report I understood that this is a genuine tool for self-knowledge. Absolutely worth every penny.',
            'name' => 'Thomas B.',
            'loc'  => 'Bergen',
            'init' => 'TB',
        ],
        [
            'text' => 'The year analysis helped me with timing. I made big decisions in the periods Åse highlighted, and everything went far better than I had dared to hope.',
            'name' => 'Layla H.',
            'loc'  => 'Stavanger',
            'init' => 'LH',
        ],
    ],
    'cta_h'       => 'Ready to explore your number chart?',
    'cta_sub'     => 'Calculate your core numbers for free, and discover what they reveal about you.',
    'cta_btn1'    => 'Calculate your numbers free',
    'cta_btn2'    => 'Contact Åse',
    'footer_tag'  => 'Norway\'s leading numerologist, based in Oslo. Helping you understand yourself through the wisdom of numbers.',
    'footer_h1'   => 'Explore', 'footer_h2' => 'Information',
    'footer_l1'   => [['Calculators','/calculators/'],['About numerology','/discover-numerology/'],['Meet Åse','/about-the-firm/']],
    'footer_l2'   => [['About numerology','/discover-numerology/'],['Calculators','/calculators/'],['Articles','/articles/'],['Privacy policy','/privacy-policy/']],
    'footer_copy' => '© ' . date('Y') . ' Åse Steinsland · Numerologist',
    'footer_ethos'=> 'Where numbers and technology work together — the Pythagorean method, computed in Python. Right calculation, right technology.',
];

// Articles data (served by Django at /articles/)
$articles = $no ? [
    [
        'slug'    => 'master-number-33',
        'tag'     => 'Mestertall',
        'title'   => 'Hva betyr det å ha 33 i kartet ditt?',
        'excerpt' => 'En dypere titt på det medfølende, kosmiske lærer-tallet og hva det sier om din livssti.',
        'meta'    => '7 min · 12. nov 2025',
        'svg_bg'  => '#f4f9ff',
        'svg_c1'  => '#dbebff',
        'svg_c2'  => '#c9e3ff',
        'svg_tc'  => '#3a63a6',
        'svg_t'   => '33',
    ],
    [
        'slug'    => 'navn-og-numerologi',
        'tag'     => 'Navn',
        'title'   => 'Navn & numerologi: hvorfor navnet ditt føles «deg»',
        'excerpt' => 'Utforsk hvordan uttrykkstallet fra ditt fulle navn farger personligheten og livsveien.',
        'meta'    => '6 min · 3. nov 2025',
        'svg_bg'  => '#f9f4ff',
        'svg_c1'  => '#ffffff',
        'svg_stroke' => '#d6c4ef',
        'svg_tc'  => '#7b56b1',
        'svg_t'   => 'NAVN',
        'svg_sub' => '1+4+9 = 5',
        'type'    => 'name',
    ],
    [
        'slug'    => 'numerological-reflection-on-mahsa-amini-and-bita-azizi',
        'tag'     => 'Forskning',
        'title'   => 'Numerologisk refleksjon: Mahsa Amini og Bita Azizi',
        'excerpt' => 'En forsiktig numerologisk lesning av to kvinner hvis navn har formet en bevegelse.',
        'meta'    => '5 min · 24. nov 2025',
        'svg_bg'  => '#f2fbf6',
        'svg_c1'  => '#80c8a3',
        'svg_c2'  => '#5ba57f',
        'svg_tc'  => '#3f8f65',
        'svg_t'   => '9',
        'type'    => 'silhouette',
    ],
] : [
    [
        'slug'    => 'master-number-33',
        'tag'     => 'Master numbers',
        'title'   => 'What does it mean to have 33 in your chart?',
        'excerpt' => 'A deeper look at the compassionate, cosmic teacher number and what it says about your life path.',
        'meta'    => '7 min · 12 Nov 2025',
        'svg_bg'  => '#f4f9ff',
        'svg_c1'  => '#dbebff',
        'svg_c2'  => '#c9e3ff',
        'svg_tc'  => '#3a63a6',
        'svg_t'   => '33',
    ],
    [
        'slug'    => 'navn-og-numerologi',
        'tag'     => 'Name',
        'title'   => 'Name & numerology: why your name feels like "you"',
        'excerpt' => 'Explore how the expression number from your full name colours your personality and path.',
        'meta'    => '6 min · 3 Nov 2025',
        'svg_bg'  => '#f9f4ff',
        'svg_c1'  => '#ffffff',
        'svg_stroke' => '#d6c4ef',
        'svg_tc'  => '#7b56b1',
        'svg_t'   => 'NAME',
        'svg_sub' => '1+4+9 = 5',
        'type'    => 'name',
    ],
    [
        'slug'    => 'creative-research-practice-for-numerology',
        'tag'     => 'Research',
        'title'   => 'Building a Creative Research Practice for Numerology',
        'excerpt' => 'How combining intuitive methods with structured inquiry deepens numerological insight.',
        'meta'    => '5 min · 18 Oct 2025',
        'svg_bg'  => '#f2fbf6',
        'svg_c1'  => '#80c8a3',
        'svg_c2'  => '#5ba57f',
        'svg_tc'  => '#3f8f65',
        'svg_t'   => '7',
        'type'    => 'num',
    ],
];

require_once __DIR__ . '/includes/seo.php';

$canonicalUrl = SITE_URL . '/';
$altNo        = $canonicalUrl;
$altEn        = $canonicalUrl . '?lang=en';

// ── WebSite schema with SearchAction ────────────────────────────────────────
$websiteSchema = [
    '@context'        => 'https://schema.org',
    '@type'           => 'WebSite',
    'name'            => SITE_NAME,
    'url'             => $canonicalUrl,
    'inLanguage'      => $no ? 'nb-NO' : 'en',
    'potentialAction' => [
        '@type'       => 'SearchAction',
        'target'      => [
            '@type'       => 'EntryPoint',
            'urlTemplate' => SITE_URL . '/articles/?q={search_term_string}',
        ],
        'query-input' => 'required name=search_term_string',
    ],
    'author' => [
        '@type'       => 'Person',
        'name'        => 'Åse Steinsland',
        'jobTitle'    => $no ? 'Numerolog' : 'Numerologist',
        'url'         => $canonicalUrl,
        'knowsAbout'  => ['Numerology', 'Pythagorean numerology', 'Life path numbers', 'Master numbers'],
        'nationality' => ['@type' => 'Country', 'name' => 'Norway'],
    ],
];

// ── Service schemas ──────────────────────────────────────────────────────────
$serviceSchemas = [
    [
        '@context'    => 'https://schema.org',
        '@type'       => 'Service',
        'name'        => $no ? 'Grunnpakke – Numerologianalyse' : 'Starter – Numerology Analysis',
        'description' => $no
            ? 'Livsveisanalyse, uttrykkstall og sjelstall med skriftlig rapport og e-postveiledning.'
            : 'Life path, expression and soul urge analysis with written report and email guidance.',
        'url'         => $canonicalUrl . '#tjenester',
        'provider'    => ['@type' => 'Person', 'name' => 'Åse Steinsland', 'url' => $canonicalUrl],
        'offers'      => [
            '@type'         => 'Offer',
            'price'         => '490',
            'priceCurrency' => 'NOK',
            'availability'  => 'https://schema.org/InStock',
        ],
    ],
    [
        '@context'    => 'https://schema.org',
        '@type'       => 'Service',
        'name'        => $no ? 'Fullstendig profil – Numerologianalyse' : 'Full Profile – Numerology Analysis',
        'description' => $no
            ? 'Komplett numerologisk kart med personlighets- og karmatal, årstall, pytagoreiske piler og videokonsultasjon.'
            : 'Complete numerological chart with personality, karma numbers, personal years, Pythagorean arrows and video consultation.',
        'url'         => $canonicalUrl . '#tjenester',
        'provider'    => ['@type' => 'Person', 'name' => 'Åse Steinsland', 'url' => $canonicalUrl],
        'offers'      => [
            '@type'         => 'Offer',
            'price'         => '990',
            'priceCurrency' => 'NOK',
            'availability'  => 'https://schema.org/InStock',
        ],
    ],
    [
        '@context'    => 'https://schema.org',
        '@type'       => 'Service',
        'name'        => $no ? 'Årsanalyse – Personlig numerologisk årsanalyse' : 'Year Analysis – Personal Numerological Year Reading',
        'description' => $no
            ? 'Dybdeanalyse av personlig år, månedlige sykluser og timing med 60 min videokonsultasjon.'
            : 'In-depth analysis of personal year, monthly cycles and timing with 60 min video consultation.',
        'url'         => $canonicalUrl . '#tjenester',
        'provider'    => ['@type' => 'Person', 'name' => 'Åse Steinsland', 'url' => $canonicalUrl],
        'offers'      => [
            '@type'         => 'Offer',
            'price'         => '1490',
            'priceCurrency' => 'NOK',
            'availability'  => 'https://schema.org/InStock',
        ],
    ],
];
?>
<!doctype html>
<html lang="<?= htmlspecialchars($T['html_lang']) ?>">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
<?php seo_head([
    'title'       => $T['title'],
    'description' => $T['meta_desc'],
    'canonical'   => $canonicalUrl,
    'lang'        => $lang,
    'alt_no'      => $altNo,
    'alt_en'      => $altEn,
    'og_type'     => 'website',
    'schema'      => $websiteSchema,
]); ?>
  <script type="application/ld+json">
  <?= json_encode([
      '@context'         => 'https://schema.org',
      '@type'            => 'Organization',
      'name'             => 'Numerologist',
      'url'              => SITE_URL,
      'parentOrganization' => ['@type' => 'Organization', 'name' => 'SetAI', 'url' => 'https://setai.no'],
      'sameAs'           => ['https://setai.no', 'https://shahnameh.setaei.com', 'https://setalink.no', 'https://trustai.no'],
  ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) ?>
  </script>
<?php if (SHOW_PRICING): foreach ($serviceSchemas as $svcSchema): ?>
  <script type="application/ld+json">
  <?= json_encode($svcSchema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) ?>
  </script>
<?php endforeach; endif; ?>
  <!-- Fonts preconnect -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="/assets/home.css">
</head>
<body>

<!-- ═══════════════════════════════════════════════════ NAV -->
<nav class="site-nav" aria-label="<?= $no ? 'Navigasjon' : 'Navigation' ?>">
  <div class="container">
    <div class="nav-inner">
      <a href="/" class="nav-logo">Numero<em>logist</em></a>

      <ul class="nav-links" id="navLinks">
        <li><a href="/discover-numerology/"><?= $T['nav_about'] ?></a></li>
        <li><a href="/#tjenester"><?= $T['nav_services'] ?></a></li>
        <li><a href="/articles/"><?= $T['nav_articles'] ?></a></li>
        <li><a href="/contact-qa/"><?= $T['nav_contact'] ?></a></li>
        <li><a href="/about-the-firm/" class="btn btn-ghost nav-cta"><?= $T['nav_cta'] ?></a></li>
      </ul>

      <div class="nav-right">
        <div class="lang-sw" aria-label="<?= $no ? 'Velg språk' : 'Select language' ?>">
          <a href="/?lang=no" class="<?= $no ? 'active' : '' ?>" hreflang="no" aria-label="Norsk">🇳🇴 NO</a>
          <a href="/?lang=en" class="<?= !$no ? 'active' : '' ?>" hreflang="en" aria-label="English">🇬🇧 EN</a>
        </div>
        <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks"
                aria-label="<?= $no ? 'Åpne meny' : 'Open menu' ?>">☰</button>
      </div>
    </div>
  </div>
</nav>


<!-- ═══════════════════════════════════════════════════ HERO -->
<section class="hero" aria-labelledby="hero-title">
  <!-- Decorative floating numbers -->
  <div class="hero-deco" aria-hidden="true">
    <span class="hero-deco-num" style="font-size:28vw;top:-8%;right:-5%;opacity:.025;">7</span>
    <span class="hero-deco-num" style="font-size:14vw;bottom:5%;left:55%;opacity:.03;">11</span>
    <span class="hero-deco-num" style="font-size:10vw;top:30%;right:20%;opacity:.02;">33</span>
  </div>

  <div class="container">
    <div class="hero-content">
      <div class="hero-eyebrow">
        <span class="hero-dot"></span>
        <?= htmlspecialchars($T['hero_eyebrow']) ?>
      </div>

      <h1 id="hero-title">
        <?= htmlspecialchars($T['hero_h1_a']) ?><br>
        <em><?= htmlspecialchars($T['hero_h1_b']) ?></em>
      </h1>

      <p class="hero-sub"><?= htmlspecialchars($T['hero_sub']) ?></p>

      <div class="hero-ctas">
        <a href="#kalkulator" class="btn btn-primary"><?= htmlspecialchars($T['hero_cta1']) ?></a>
        <a href="/about-the-firm/" class="btn btn-outline-white"><?= htmlspecialchars($T['hero_cta2']) ?></a>
      </div>

      <div class="hero-trust">
        <span><?= htmlspecialchars($T['hero_trust1']) ?></span>
        <span class="hero-trust-sep"></span>
        <span><?= htmlspecialchars($T['hero_trust2']) ?></span>
        <span class="hero-trust-sep"></span>
        <span><?= htmlspecialchars($T['hero_trust3']) ?></span>
      </div>
    </div>
  </div>
</section>


<!-- ═══════════════════════════════════════════════════ TODAY'S NUMBER -->
<div class="todays-num-wrap" aria-label="<?= $T['tn_badge'] ?>">
  <div class="container">
    <div class="todays-num-card">
      <div class="tn-num-display">
        <div class="tn-number"><?= $todayNum ?></div>
        <span class="tn-badge"><?= htmlspecialchars($T['tn_badge']) ?></span>
      </div>
      <div class="tn-info">
        <p class="tn-eyebrow"><?= htmlspecialchars($T['tn_eyebrow']) ?></p>
        <h2 class="tn-title serif"><?= htmlspecialchars($todayTitle) ?></h2>
        <p class="tn-essence"><?= htmlspecialchars($todayEssence) ?></p>
        <p class="tn-date"><?= htmlspecialchars($dateLabel) ?></p>
      </div>
    </div>
  </div>
</div>


<!-- ═══════════════════════════════════════════════════ CALCULATOR -->
<section class="calc-section" id="kalkulator">
  <div class="container">
    <div class="calc-inner">
      <div>
        <span class="section-eyebrow"><?= $no ? 'Gratis verktøy' : 'Free tool' ?></span>
        <h2 class="section-title"><?= htmlspecialchars($T['calc_title']) ?></h2>
        <div class="section-divider"></div>
        <p class="section-sub"><?= htmlspecialchars($T['calc_sub']) ?></p>

        <div class="calc-card">
          <?php if ($calcError): ?>
            <div class="calc-error" role="alert"><?= htmlspecialchars($calcError) ?></div>
          <?php endif; ?>

          <form method="post" class="calc-form" id="calcForm" novalidate>
            <div class="field">
              <label for="full_name"><?= htmlspecialchars($T['calc_name']) ?></label>
              <input type="text" id="full_name" name="full_name"
                     value="<?= htmlspecialchars($calcName) ?>"
                     placeholder="<?= $no ? 'F.eks. Kari Nordmann' : 'E.g. John Smith' ?>"
                     autocomplete="name">
            </div>
            <div class="field">
              <label for="birth_date"><?= htmlspecialchars($T['calc_date']) ?></label>
              <input type="date" id="birth_date" name="birth_date"
                     value="<?= htmlspecialchars($calcDate) ?>"
                     max="<?= date('Y-m-d') ?>">
            </div>
            <button type="submit" class="btn btn-primary btn-full"><?= htmlspecialchars($T['calc_submit']) ?></button>
          </form>

          <div class="results-grid" id="resultsGrid">
            <?php
            $fields = [
              [$T['calc_lp'], $calcResult['life_path']  ?? null],
              [$T['calc_ex'], $calcResult['expression'] ?? null],
              [$T['calc_su'], $calcResult['soul_urge']  ?? null],
              [$T['calc_pe'], $calcResult['personality']?? null],
            ];
            foreach ($fields as [$label, $val]):
            ?>
            <div class="result-card">
              <a class="result-num <?= $val === null ? 'empty' : '' ?>"
                 id="result-<?= strtolower(str_replace(' ','-',$label)) ?>"
                 href="<?= $val !== null ? '/numbers/' . $val . '/' : '#' ?>"
                 style="text-decoration:none;display:block;<?= $val === null ? 'pointer-events:none;cursor:default;' : 'cursor:pointer;' ?>"
                 aria-label="<?= $no ? 'Les mer om tallet' : 'Read more about the number' ?> <?= $val !== null ? $val : '' ?>"
              ><?= $val !== null ? $val : '—' ?></a>
              <span class="result-label"><?= htmlspecialchars($label) ?></span>
            </div>
            <?php endforeach; ?>
          </div>
        </div>
      </div>

      <div>
        <div id="calcAsideDefault">
          <h3 class="section-title" style="font-size:1.7rem"><?= htmlspecialchars($T['calc_aside_h']) ?></h3>
          <div class="section-divider"></div>
          <p class="section-sub" style="margin-bottom:2rem"><?= htmlspecialchars($T['calc_aside_p']) ?></p>
          <a href="/about-the-firm/" class="btn btn-primary"><?= htmlspecialchars($T['about_cta']) ?></a>
        </div>
        <div id="calcAsideResult" hidden>
          <h3 class="section-title" style="font-size:1.7rem"><?= htmlspecialchars($T['calc_result_h']) ?></h3>
          <div class="section-divider"></div>
          <div id="masterCallout" hidden style="background:var(--c-primary-tint,#f2f8f4);border:1.5px solid var(--c-primary,#3cb179);border-radius:12px;padding:1rem 1.25rem;margin-bottom:1.25rem"></div>
          <p class="section-sub" style="margin-bottom:.75rem"><?= htmlspecialchars($T['calc_result_intro']) ?></p>
          <ul id="resultSummary" style="margin:0 0 1.25rem;padding-left:1.1rem;color:var(--c-text-2);line-height:1.7"></ul>
          <p class="section-sub" style="margin-bottom:1.5rem"><?= htmlspecialchars($T['calc_result_outro']) ?></p>
          <a href="/about-the-firm/" class="btn btn-primary"><?= htmlspecialchars($T['about_cta']) ?></a>
        </div>
      </div>
    </div>
  </div>
</section>


<!-- ═══════════════════════════════════════════════════ ABOUT -->
<section class="section about-section" id="om-ase">
  <div class="container">
    <div class="about-grid">
      <div>
        <div class="about-photo" role="img" aria-label="Åse Steinsland – numerolog">
          <div class="about-photo-monogram" aria-hidden="true">Å</div>
        </div>
      </div>
      <div>
        <span class="section-eyebrow"><?= htmlspecialchars($T['about_eyebrow']) ?></span>
        <h2 class="section-title"><?= htmlspecialchars($T['about_h']) ?></h2>
        <div class="section-divider"></div>
        <p class="section-sub" style="margin-bottom:1rem"><?= htmlspecialchars($T['about_p1']) ?></p>
        <p style="color:var(--c-text-2);font-size:1rem;line-height:1.65;max-width:55ch;margin-bottom:1.75rem"><?= htmlspecialchars($T['about_p2']) ?></p>
        <div class="about-credentials">
          <?php foreach (['cred1','cred2','cred3','cred4'] as $k): ?>
            <span class="cred-pill"><?= htmlspecialchars($T[$k]) ?></span>
          <?php endforeach; ?>
        </div>
        <a href="/about-the-firm/" class="btn btn-ghost"><?= htmlspecialchars($T['about_cta']) ?></a>
      </div>
    </div>
  </div>
</section>


<!-- ═══════════════════════════════════════════════════ SERVICES -->
<?php if (SHOW_PRICING): ?>
<section class="services-section" id="tjenester" aria-labelledby="services-title">
  <div class="container">
    <span class="section-eyebrow"><?= htmlspecialchars($T['srv_eyebrow']) ?></span>
    <h2 class="section-title" id="services-title"><?= htmlspecialchars($T['srv_h']) ?></h2>
    <div class="section-divider"></div>
    <p class="section-sub"><?= htmlspecialchars($T['srv_sub']) ?></p>

    <div class="services-grid">
      <?php foreach ($T['services'] as $s): ?>
      <div class="service-card<?= !empty($s['featured']) ? ' featured' : '' ?>">
        <?php if (!empty($s['featured'])): ?>
          <div class="featured-badge"><?= htmlspecialchars($T['srv_popular']) ?></div>
        <?php endif; ?>
        <h3 class="service-name serif"><?= htmlspecialchars($s['name']) ?></h3>
        <div class="service-price"><sup>kr </sup><?= htmlspecialchars($s['price']) ?></div>
        <p class="service-period"><?= $no ? 'per analyse' : 'per reading' ?></p>
        <p class="service-desc"><?= htmlspecialchars($s['desc']) ?></p>
        <ul class="feature-list">
          <?php foreach ($s['items'] as $item): ?>
          <li class="feature-item">
            <span class="check-icon" aria-hidden="true">✓</span>
            <?= htmlspecialchars($item) ?>
          </li>
          <?php endforeach; ?>
        </ul>
        <a href="/intake/" class="btn btn-primary btn-full service-cta"><?= htmlspecialchars($s['cta']) ?></a>
      </div>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?php endif; ?>


<!-- ═══════════════════════════════════════════════════ ARTICLES -->
<section class="section articles-section" id="artikler" aria-labelledby="articles-title">
  <div class="container">
    <div class="section-header-row">
      <div>
        <span class="section-eyebrow"><?= htmlspecialchars($T['art_eyebrow']) ?></span>
        <h2 class="section-title" id="articles-title" style="margin-bottom:0"><?= htmlspecialchars($T['art_h']) ?></h2>
      </div>
      <a href="/articles/" class="view-all"><?= htmlspecialchars($T['art_all']) ?></a>
    </div>

    <div class="articles-grid">
      <?php foreach ($articles as $a): ?>
      <a class="article-card" href="/articles/<?= htmlspecialchars($a['slug']) ?>/"
         aria-label="<?= htmlspecialchars($a['title']) ?>">
        <div class="article-thumb">
          <?php if (($a['type'] ?? '') === 'name'): ?>
            <svg viewBox="0 0 320 180" aria-hidden="true">
              <rect width="320" height="180" fill="<?= $a['svg_bg'] ?>"/>
              <rect x="42" y="32" width="236" height="116" rx="18"
                    fill="<?= $a['svg_c1'] ?>" stroke="<?= $a['svg_stroke'] ?? $a['svg_c1'] ?>"/>
              <text x="64" y="78"  font-size="24" font-family="Inter,sans-serif" fill="<?= $a['svg_tc'] ?>"><?= $a['svg_t'] ?></text>
              <text x="64" y="114" font-size="18" font-family="Inter,sans-serif" fill="<?= $a['svg_tc'] ?>"><?= $a['svg_sub'] ?? '' ?></text>
            </svg>
          <?php elseif (($a['type'] ?? '') === 'silhouette'): ?>
            <svg viewBox="0 0 320 180" aria-hidden="true">
              <rect width="320" height="180" fill="<?= $a['svg_bg'] ?>"/>
              <circle cx="118" cy="64" r="26" fill="<?= $a['svg_c1'] ?>"/>
              <circle cx="198" cy="64" r="26" fill="<?= $a['svg_c2'] ?>"/>
              <path d="M62 166c9-34 34-56 58-56 21 0 41 14 53 37 10-23 29-37 52-37 27 0 50 22 59 56H62z" fill="<?= $a['svg_tc'] ?>"/>
            </svg>
          <?php else: ?>
            <svg viewBox="0 0 320 180" aria-hidden="true">
              <rect width="320" height="180" fill="<?= $a['svg_bg'] ?>"/>
              <circle cx="120" cy="90" r="60" fill="<?= $a['svg_c1'] ?>"/>
              <circle cx="200" cy="90" r="60" fill="<?= $a['svg_c2'] ?? $a['svg_c1'] ?>"/>
              <text x="90" y="108" font-size="60" font-family="Cormorant Garamond,Georgia,serif"
                    font-weight="700" fill="<?= $a['svg_tc'] ?>"><?= htmlspecialchars($a['svg_t']) ?></text>
            </svg>
          <?php endif; ?>
        </div>
        <div class="article-body">
          <span class="article-tag"><?= htmlspecialchars($a['tag']) ?></span>
          <h3 class="article-title"><?= htmlspecialchars($a['title']) ?></h3>
          <p class="article-excerpt"><?= htmlspecialchars($a['excerpt']) ?></p>
          <div class="article-footer">
            <span><?= htmlspecialchars($a['meta']) ?></span>
            <span class="article-read-more"><?= htmlspecialchars($T['art_read']) ?> →</span>
          </div>
        </div>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>


<!-- ═══════════════════════════════════════════════════ TESTIMONIALS -->
<section class="section testimonials-section" aria-labelledby="testimonials-title">
  <div class="container">
    <span class="section-eyebrow"><?= htmlspecialchars($T['testimonials_eyebrow']) ?></span>
    <h2 class="section-title" id="testimonials-title"><?= htmlspecialchars($T['testimonials_h']) ?></h2>
    <div class="section-divider"></div>

    <div class="testimonials-grid">
      <?php foreach ($T['testimonials'] as $tm): ?>
      <div class="testimonial-card">
        <span class="stars" aria-label="5 stars">★★★★★</span>
        <p class="testimonial-text">"<?= htmlspecialchars($tm['text']) ?>"</p>
        <div class="testimonial-author">
          <div class="author-avatar" aria-hidden="true"><?= htmlspecialchars($tm['init']) ?></div>
          <div>
            <div class="author-name"><?= htmlspecialchars($tm['name']) ?></div>
            <div class="author-loc"><?= htmlspecialchars($tm['loc']) ?></div>
          </div>
        </div>
      </div>
      <?php endforeach; ?>
    </div>
  </div>
</section>


<!-- ═══════════════════════════════════════════════════ FINAL CTA -->
<section class="cta-section" aria-labelledby="cta-title">
  <div class="container">
    <h2 id="cta-title"><?= htmlspecialchars($T['cta_h']) ?></h2>
    <p><?= htmlspecialchars($T['cta_sub']) ?></p>
    <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:.9rem">
      <a href="#kalkulator" class="btn btn-primary"><?= htmlspecialchars($T['cta_btn1']) ?></a>
      <a href="/about-the-firm/" class="btn btn-outline-white"><?= htmlspecialchars($T['cta_btn2']) ?></a>
    </div>
  </div>
</section>


<!-- ═══════════════════════════════════════════════════ FOOTER -->
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="/" class="footer-brand">Numerologist</a>
        <p class="footer-tagline"><?= htmlspecialchars($T['footer_tag']) ?></p>
      </div>
      <div class="footer-col">
        <h4><?= htmlspecialchars($T['footer_h1']) ?></h4>
        <ul>
          <?php foreach ($T['footer_l1'] as [$label, $href]): ?>
            <li><a href="<?= htmlspecialchars($href) ?>"><?= htmlspecialchars($label) ?></a></li>
          <?php endforeach; ?>
        </ul>
      </div>
      <div class="footer-col">
        <h4><?= htmlspecialchars($T['footer_h2']) ?></h4>
        <ul>
          <?php foreach ($T['footer_l2'] as [$label, $href]): ?>
            <li><a href="<?= htmlspecialchars($href) ?>"><?= htmlspecialchars($label) ?></a></li>
          <?php endforeach; ?>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span><?= htmlspecialchars($T['footer_copy']) ?><br><small class="footer-ethos"><?= htmlspecialchars($T['footer_ethos']) ?></small></span>
      <div style="display:flex;gap:.75rem;align-items:center">
        <a href="/?lang=no">🇳🇴 Norsk</a>
        <a href="/?lang=en">🇬🇧 English</a>
      </div>
    </div>
  </div>
</footer>


<!-- ═══════════════════════════════════════════════════ JS -->
<script>
(function () {
  'use strict';

  // ── Burger menu ──────────────────────────────────────────────────────────
  var toggle = document.getElementById('navToggle');
  var links  = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? '✕' : '☰';
    });
  }

  // ── Letter map (Pythagorean + Norwegian) ─────────────────────────────────
  var LMAP = {
    A:1,B:2,C:3,D:4,E:5,F:6,G:7,H:8,I:9,
    J:1,K:2,L:3,M:4,N:5,O:6,P:7,Q:8,R:9,
    S:1,T:2,U:3,V:4,W:5,X:6,Y:7,Z:8,
    Å:1,Æ:5,Ø:6
  };
  var VOWELS = {A:1,E:1,I:1,O:1,U:1,Y:1,Æ:1,Ø:1,Å:1};
  var MASTERS = [11,22,33];

  function reduce(n) {
    while (n > 9 && MASTERS.indexOf(n) === -1) {
      n = String(n).split('').reduce(function(s,d){return s+parseInt(d,10);}, 0);
    }
    return n;
  }

  function calcName(name, filter) {
    var letters = name.toUpperCase().replace(/[^A-ZÆØÅ]/g,'').split('');
    var sum = 0;
    letters.forEach(function(c) {
      if (!filter || filter[c]) sum += (LMAP[c] || 0);
    });
    return reduce(sum);
  }

  function calcDate(dateStr) {
    var digits = dateStr.replace(/\D/g,'');
    return reduce(digits.split('').reduce(function(s,d){return s+parseInt(d,10);},0));
  }

  // ── Live calculator ──────────────────────────────────────────────────────
  var nameInput = document.getElementById('full_name');
  var dateInput = document.getElementById('birth_date');
  var resIds    = {
    '<?= $T['calc_lp'] ?>': 'life-path',
    '<?= $T['calc_ex'] ?>': 'expression',
    '<?= $T['calc_su'] ?>': 'soul-urge',
    '<?= $T['calc_pe'] ?>': 'personality'
  };
  var RESULT_LABELS = {
    'life-path':   <?= json_encode($T['calc_lp']) ?>,
    'expression':  <?= json_encode($T['calc_ex']) ?>,
    'soul-urge':   <?= json_encode($T['calc_su']) ?>,
    'personality': <?= json_encode($T['calc_pe']) ?>
  };
  var NUMBER_MEANINGS = <?= json_encode($T['number_meanings'], JSON_UNESCAPED_UNICODE) ?>;
  var MASTER_BADGE_TEXT = <?= json_encode($T['master_badge']) ?>;

  function updateResults() {
    var name = nameInput ? nameInput.value : '';
    var date = dateInput ? dateInput.value : '';
    if (!name || !date) return;

    var consonants = {};
    Object.keys(LMAP).forEach(function(c){ if (!VOWELS[c]) consonants[c] = 1; });

    var results = {
      'life-path':   calcDate(date),
      'expression':  calcName(name, null),
      'soul-urge':   calcName(name, VOWELS),
      'personality': calcName(name, consonants)
    };

    var cards = document.querySelectorAll('#resultsGrid .result-card');
    var keys  = ['life-path','expression','soul-urge','personality'];
    cards.forEach(function(card, i) {
      var numEl = card.querySelector('.result-num');
      if (numEl && keys[i]) {
        var n = results[keys[i]];
        numEl.textContent = n;
        numEl.classList.remove('empty');
        numEl.href = '/numbers/' + n + '/';
        numEl.style.pointerEvents = 'auto';
        numEl.style.cursor = 'pointer';
      }
    });

    renderPersonalizedResult(results, keys);
  }

  function renderPersonalizedResult(results, keys) {
    var summaryEl  = document.getElementById('resultSummary');
    var calloutEl  = document.getElementById('masterCallout');
    var defaultBox = document.getElementById('calcAsideDefault');
    var resultBox  = document.getElementById('calcAsideResult');
    if (!summaryEl || !calloutEl || !defaultBox || !resultBox) return;

    var MASTERS_LOCAL = [11, 22, 33];
    var summaryHtml = '';
    var masterTexts = [];

    keys.forEach(function (key) {
      var n = results[key];
      var meaning = NUMBER_MEANINGS[n];
      if (!meaning) return;
      summaryHtml += '<li><strong>' + RESULT_LABELS[key] + ' ' + n + '</strong> — ' + meaning.essence + '</li>';
      if (MASTERS_LOCAL.indexOf(n) !== -1 && meaning.master && masterTexts.indexOf(meaning.master) === -1) {
        masterTexts.push(meaning.master);
      }
    });

    summaryEl.innerHTML = summaryHtml;

    if (masterTexts.length) {
      calloutEl.innerHTML = '<strong>' + MASTER_BADGE_TEXT + '</strong><p style="margin:.5rem 0 0">' +
        masterTexts.join('</p><p style="margin:.75rem 0 0">') + '</p>';
      calloutEl.hidden = false;
    } else {
      calloutEl.hidden = true;
      calloutEl.innerHTML = '';
    }

    defaultBox.hidden = true;
    resultBox.hidden = false;
  }

  if (nameInput) nameInput.addEventListener('input', updateResults);
  if (dateInput) dateInput.addEventListener('change', updateResults);

  // Prevent full page reload — JS handles it
  var form = document.getElementById('calcForm');
  if (form) {
    form.addEventListener('submit', function(e) {
      var name = nameInput ? nameInput.value.trim() : '';
      var date = dateInput ? dateInput.value : '';
      if (name && date) {
        e.preventDefault();
        updateResults();
      }
    });
  }

  // Trigger if PHP pre-filled values
  if (nameInput && nameInput.value && dateInput && dateInput.value) {
    updateResults();
  }
})();
</script>

</body>
</html>
