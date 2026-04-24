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
        'title' => 'Discover Numerology',
        'body' => 'Utforsk grunnprinsippene i numerologi og hvordan tall brukes til å forstå personlighet, livssyklus og potensial.',
    ],
    'calculators' => [
        'title' => 'Calculator Suite',
        'body' => 'Samling av enkle kalkulatorer for livsvei, uttrykkstall og navn-analyse direkte i nettleseren.',
    ],
    'resources' => [
        'title' => 'Resources',
        'body' => 'Ressursside med artikler, referanser og anbefalt lesing for videre fordypning.',
    ],
    'guidance-support' => [
        'title' => 'Guidance & Support',
        'body' => 'Informasjon om veiledning, spørsmål/svar og kontaktmuligheter.',
    ],
    'legal' => [
        'title' => 'Legal',
        'body' => 'Personvern, vilkår og juridisk informasjon for nettstedet.',
    ],
];

$numberInterpretations = [
    1 => ['title' => 'Number 1', 'essence' => 'Lederskap, initiativ og selvstendighet.'],
    2 => ['title' => 'Number 2', 'essence' => 'Samarbeid, balanse og relasjoner.'],
    3 => ['title' => 'Number 3', 'essence' => 'Kreativitet, kommunikasjon og glede.'],
    4 => ['title' => 'Number 4', 'essence' => 'Struktur, disiplin og stabilitet.'],
    5 => ['title' => 'Number 5', 'essence' => 'Frihet, endring og eventyr.'],
    6 => ['title' => 'Number 6', 'essence' => 'Omsorg, ansvar og harmoni.'],
    7 => ['title' => 'Number 7', 'essence' => 'Analyse, intuisjon og indre søken.'],
    8 => ['title' => 'Number 8', 'essence' => 'Makt, resultater og materiell mestring.'],
    9 => ['title' => 'Number 9', 'essence' => 'Medfølelse, fullføring og visdom.'],
    11 => ['title' => 'Master 11', 'essence' => 'Inspirasjon, intuisjon og oppvåkning.'],
    22 => ['title' => 'Master 22', 'essence' => 'Visjon, bygging og kollektivt bidrag.'],
    33 => ['title' => 'Master 33', 'essence' => 'Healing, undervisning og tjeneste.'],
];
