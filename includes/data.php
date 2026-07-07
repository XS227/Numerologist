<?php

declare(strict_types=1);

function digit_sum(int $number): int
{
    return array_sum(array_map('intval', str_split((string) $number)));
}

function reduce_number(int $number): int
{
    $masters = [11, 22, 33];
    while ($number > 9 && !in_array($number, $masters, true)) {
        $number = digit_sum($number);
    }

    return $number;
}

function letter_value(string $letter): int
{
    static $map = [
        'A' => 1, 'J' => 1, 'S' => 1,
        'B' => 2, 'K' => 2, 'T' => 2,
        'C' => 3, 'L' => 3, 'U' => 3,
        'D' => 4, 'M' => 4, 'V' => 4,
        'E' => 5, 'N' => 5, 'W' => 5,
        'F' => 6, 'O' => 6, 'X' => 6,
        'G' => 7, 'P' => 7, 'Y' => 7,
        'H' => 8, 'Q' => 8, 'Z' => 8,
        'I' => 9, 'R' => 9,
        'Å' => 1, 'Æ' => 5, 'Ø' => 6,
    ];

    return $map[$letter] ?? 0;
}

function reduce_name(string $name, ?array $filterLetters = null): int
{
    $sum = 0;
    $letters = preg_split('//u', mb_strtoupper($name), -1, PREG_SPLIT_NO_EMPTY);

    foreach ($letters as $letter) {
        if (!preg_match('/\p{L}/u', $letter)) {
            continue;
        }
        if ($filterLetters !== null && !in_array($letter, $filterLetters, true)) {
            continue;
        }
        $sum += letter_value($letter);
    }

    return reduce_number($sum);
}

function calculate_numerology(string $fullName, string $birthDate): array
{
    $dateDigits = preg_replace('/\D/', '', $birthDate) ?? '';
    $lifePath = reduce_number((int) $dateDigits);

    $vowels = ['A', 'E', 'I', 'O', 'U', 'Y', 'Æ', 'Ø', 'Å'];
    $allLetters = array_keys([
        'A'=>1,'B'=>1,'C'=>1,'D'=>1,'E'=>1,'F'=>1,'G'=>1,'H'=>1,'I'=>1,'J'=>1,
        'K'=>1,'L'=>1,'M'=>1,'N'=>1,'O'=>1,'P'=>1,'Q'=>1,'R'=>1,'S'=>1,'T'=>1,
        'U'=>1,'V'=>1,'W'=>1,'X'=>1,'Y'=>1,'Z'=>1,'Æ'=>1,'Ø'=>1,'Å'=>1,
    ]);
    $consonants = array_values(array_diff($allLetters, $vowels));

    return [
        'life_path' => $lifePath,
        'expression' => reduce_name($fullName),
        'soul_urge' => reduce_name($fullName, $vowels),
        'personality' => reduce_name($fullName, $consonants),
    ];
}

$pages = [
    'discover-numerology' => [
        'title'       => 'Hva er numerologi?',
        'title_en'    => 'What is Numerology?',
        'body'        => 'Utforsk grunnprinsippene i numerologi og hvordan tall brukes til å forstå personlighet, livssyklus og potensial.',
        'description' => 'Lær om numerologiens grunnprinsipper og hvordan Åse Steinsland bruker tall til å avdekke personlighet, livssyklus og potensial.',
        'desc_en'     => 'Learn the fundamentals of numerology and how Åse Steinsland uses numbers to reveal personality, life cycles and potential.',
    ],
    'calculators' => [
        'title'       => 'Numerologikalkulatorer',
        'title_en'    => 'Numerology Calculators',
        'body'        => 'Samling av enkle kalkulatorer for livsvei, uttrykkstall og navn-analyse direkte i nettleseren.',
        'description' => 'Beregn ditt livsveitall, uttrykkstall, sjelstall og personlighetstall gratis med Åse Steinslands numerologikalkulatorer.',
        'desc_en'     => 'Calculate your life path, expression, soul urge and personality numbers for free with Åse Steinsland\'s numerology calculators.',
    ],
    'resources' => [
        'title'       => 'Ressurser og lesestoff',
        'title_en'    => 'Resources & Reading',
        'body'        => 'Ressursside med artikler, referanser og anbefalt lesing for videre fordypning.',
        'description' => 'Artikler, referanser og anbefalt lesing for deg som ønsker å fordype deg i numerologi og tallenes visdom.',
        'desc_en'     => 'Articles, references and recommended reading for those who want to explore numerology and the wisdom of numbers.',
    ],
    'guidance-support' => [
        'title'       => 'Veiledning og støtte',
        'title_en'    => 'Guidance & Support',
        'body'        => 'Informasjon om veiledning, spørsmål/svar og kontaktmuligheter.',
        'description' => 'Få personlig numerologisk veiledning fra Åse Steinsland. Kontakt oss for spørsmål eller bestill en konsultasjon.',
        'desc_en'     => 'Get personal numerological guidance from Åse Steinsland. Contact us with questions or book a consultation.',
    ],
    'legal' => [
        'title'       => 'Personvern og vilkår',
        'title_en'    => 'Privacy & Terms',
        'body'        => 'Personvern, vilkår og juridisk informasjon for nettstedet.',
        'description' => 'Personvernpolicy, brukervilkår og juridisk informasjon for numerologist.setai.no.',
        'desc_en'     => 'Privacy policy, terms of use and legal information for numerologist.setai.no.',
        'noindex'     => true,
    ],
];

$numberInterpretations = [
    1  => [
        'title'       => 'Tall 1 i numerologi – Lederskap og initiativ',
        'title_en'    => 'Number 1 in Numerology – Leadership and Initiative',
        'essence'     => 'Lederskap, initiativ og selvstendighet.',
        'essence_en'  => 'Leadership, initiative and independence.',
        'description' => 'Utforsk tall 1 i numerologien: energien av lederskap, initiativ og nye begynnelser. Hva betyr det å ha 1 som livsveitall?',
        'desc_en'     => 'Explore number 1 in numerology: the energy of leadership, initiative and new beginnings. What does it mean to have 1 as your life path?',
    ],
    2  => [
        'title'       => 'Tall 2 i numerologi – Samarbeid og balanse',
        'title_en'    => 'Number 2 in Numerology – Cooperation and Balance',
        'essence'     => 'Samarbeid, balanse og relasjoner.',
        'essence_en'  => 'Cooperation, balance and relationships.',
        'description' => 'Utforsk tall 2 i numerologien: energien av samarbeid, sensitivitet og relasjonell intelligens. Hva betyr livsveitall 2?',
        'desc_en'     => 'Explore number 2 in numerology: the energy of cooperation, sensitivity and relational intelligence. What does life path 2 mean?',
    ],
    3  => [
        'title'       => 'Tall 3 i numerologi – Kreativitet og selvuttrykk',
        'title_en'    => 'Number 3 in Numerology – Creativity and Self-expression',
        'essence'     => 'Kreativitet, kommunikasjon og glede.',
        'essence_en'  => 'Creativity, communication and joy.',
        'description' => 'Utforsk tall 3 i numerologien: kreativitetens, gledens og selvuttrykkets energi. Hva betyr det å ha 3 i kartet ditt?',
        'desc_en'     => 'Explore number 3 in numerology: the energy of creativity, joy and self-expression. What does it mean to have 3 in your chart?',
    ],
    4  => [
        'title'       => 'Tall 4 i numerologi – Struktur og stabilitet',
        'title_en'    => 'Number 4 in Numerology – Structure and Stability',
        'essence'     => 'Struktur, disiplin og stabilitet.',
        'essence_en'  => 'Structure, discipline and stability.',
        'description' => 'Utforsk tall 4 i numerologien: energien av struktur, pålitelighet og langsiktig bygging. Hva betyr livsveitall 4?',
        'desc_en'     => 'Explore number 4 in numerology: the energy of structure, reliability and long-term building. What does life path 4 mean?',
    ],
    5  => [
        'title'       => 'Tall 5 i numerologi – Frihet og forandring',
        'title_en'    => 'Number 5 in Numerology – Freedom and Change',
        'essence'     => 'Frihet, endring og eventyr.',
        'essence_en'  => 'Freedom, change and adventure.',
        'description' => 'Utforsk tall 5 i numerologien: eventyrlysten, frihetssøkende energi. Hva betyr det å ha 5 som livsveitall?',
        'desc_en'     => 'Explore number 5 in numerology: the adventurous, freedom-seeking energy. What does it mean to have 5 as your life path?',
    ],
    6  => [
        'title'       => 'Tall 6 i numerologi – Omsorg og harmoni',
        'title_en'    => 'Number 6 in Numerology – Care and Harmony',
        'essence'     => 'Omsorg, ansvar og harmoni.',
        'essence_en'  => 'Care, responsibility and harmony.',
        'description' => 'Utforsk tall 6 i numerologien: energien av omsorg, ansvar og hjertets tjeneste. Hva betyr livsveitall 6?',
        'desc_en'     => 'Explore number 6 in numerology: the energy of care, responsibility and heart-centred service. What does life path 6 mean?',
    ],
    7  => [
        'title'       => 'Tall 7 i numerologi – Analyse og indre visdom',
        'title_en'    => 'Number 7 in Numerology – Analysis and Inner Wisdom',
        'essence'     => 'Analyse, intuisjon og indre søken.',
        'essence_en'  => 'Analysis, intuition and inner seeking.',
        'description' => 'Utforsk tall 7 i numerologien: visdomssøkerens energi – analyse, intuisjon og åndelig dybde. Hva betyr livsveitall 7?',
        'desc_en'     => 'Explore number 7 in numerology: the seeker\'s energy of analysis, intuition and spiritual depth. What does life path 7 mean?',
    ],
    8  => [
        'title'       => 'Tall 8 i numerologi – Makt og materiell mestring',
        'title_en'    => 'Number 8 in Numerology – Power and Material Mastery',
        'essence'     => 'Makt, resultater og materiell mestring.',
        'essence_en'  => 'Power, achievement and material mastery.',
        'description' => 'Utforsk tall 8 i numerologien: lederskapets, overflodets og materiell mestringens energi. Hva betyr livsveitall 8?',
        'desc_en'     => 'Explore number 8 in numerology: the energy of leadership, abundance and material mastery. What does life path 8 mean?',
    ],
    9  => [
        'title'       => 'Tall 9 i numerologi – Medfølelse og visdom',
        'title_en'    => 'Number 9 in Numerology – Compassion and Wisdom',
        'essence'     => 'Medfølelse, fullføring og visdom.',
        'essence_en'  => 'Compassion, completion and wisdom.',
        'description' => 'Utforsk tall 9 i numerologien: medfølelsens, fullføringens og universell visdoms energi. Hva betyr livsveitall 9?',
        'desc_en'     => 'Explore number 9 in numerology: the energy of compassion, completion and universal wisdom. What does life path 9 mean?',
    ],
    11 => [
        'title'       => 'Mestertall 11 – Inspirasjon og åndelig intuisjon',
        'title_en'    => 'Master Number 11 – Inspiration and Spiritual Intuition',
        'essence'     => 'Inspirasjon, intuisjon og åndelig oppvåkning.',
        'essence_en'  => 'Inspiration, intuition and spiritual awakening.',
        'description' => 'Utforsk mestertall 11 i numerologien: den åndelige søkeren, inspiratoren og den intuitive lederen. Hva betyr mestertall 11?',
        'desc_en'     => 'Explore master number 11 in numerology: the spiritual seeker, inspirational leader and highly intuitive channel. What does master 11 mean?',
    ],
    22 => [
        'title'       => 'Mestertall 22 – Den store byggerens tall',
        'title_en'    => 'Master Number 22 – The Master Builder',
        'essence'     => 'Visjon, bygging og kollektivt bidrag.',
        'essence_en'  => 'Vision, building and collective contribution.',
        'description' => 'Utforsk mestertall 22 i numerologien: den store byggerens energi – visjonær kraft kombinert med praktisk gjennomføring.',
        'desc_en'     => 'Explore master number 22 in numerology: the master builder\'s energy combining visionary power with practical execution.',
    ],
    33 => [
        'title'       => 'Mestertall 33 – Den kosmiske lærerens tall',
        'title_en'    => 'Master Number 33 – The Cosmic Teacher',
        'essence'     => 'Healing, undervisning og kosmisk tjeneste.',
        'essence_en'  => 'Healing, teaching and cosmic service.',
        'description' => 'Utforsk mestertall 33 i numerologien: den kosmiske læreren og heleren. Det sjeldneste og mest medfølende mestertallet.',
        'desc_en'     => 'Explore master number 33 in numerology: the cosmic teacher and healer. The rarest and most compassionate of the master numbers.',
    ],
];
