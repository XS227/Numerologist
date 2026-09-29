<?php

declare(strict_types=1);

/**
 * Modular analysis product configuration.
 *
 * Legacy package IDs remain valid for old orders and direct links. New orders
 * should use the "builder" product and persist the selected configuration.
 */

const ANALYSIS_BASE_PRICE_KR = 227;
const ANALYSIS_DEPTH_CAP_KR = 471;

const ANALYSIS_CORE = [
    'name'        => ['no' => 'Navnetall / Expression', 'en' => 'Name / Expression Number', 'fa' => 'عدد نام / بیان'],
    'vowel'       => ['no' => 'Vokaltall / Heart’s Desire', 'en' => 'Vowel / Heart’s Desire', 'fa' => 'عدد حروف صدادار / خواسته قلبی'],
    'consonant'   => ['no' => 'Konsonanttall / Personality', 'en' => 'Consonant / Personality', 'fa' => 'عدد حروف بی‌صدا / شخصیت'],
    'life_path'   => ['no' => 'Skjebnetall / Life Path', 'en' => 'Destiny / Life Path', 'fa' => 'عدد سرنوشت / مسیر زندگی'],
    'birthday'    => ['no' => 'Fødselsdagstall', 'en' => 'Birthday Number', 'fa' => 'عدد روز تولد'],
];

const ANALYSIS_MODULES = [
    'current_name' => [
        'price' => 39, 'group' => 'identity',
        'no' => 'Nåværende navnetall', 'en' => 'Current Name Number', 'fa' => 'عدد نام فعلی',
        'desc_no' => 'Hvordan navnet du bruker nå justerer uttrykket ditt.',
    ],
    'current_vowel' => [
        'price' => 39, 'group' => 'identity',
        'no' => 'Nåværende vokaltall', 'en' => 'Current Vowel Number', 'fa' => 'عدد حروف صدادار نام فعلی',
        'desc_no' => 'Det indre ønsket i navnet du bruker i dag.',
    ],
    'cornerstone' => [
        'price' => 29, 'group' => 'identity',
        'no' => 'Hjørnestein / første bokstav', 'en' => 'Cornerstone / First Letter', 'fa' => 'سنگ بنا / حرف اول',
        'desc_no' => 'Hvordan du går inn i muligheter og hindringer.',
    ],
    'life_name_bridge' => [
        'price' => 39, 'group' => 'identity',
        'no' => 'Livsvei–navn bro', 'en' => 'Life Path–Name Bridge', 'fa' => 'پل مسیر زندگی و نام',
        'desc_no' => 'Avstanden mellom livsretningen og talentene i navnet.',
    ],
    'vowel_consonant_bridge' => [
        'price' => 39, 'group' => 'identity',
        'no' => 'Vokal–konsonant bro', 'en' => 'Vowel–Consonant Bridge', 'fa' => 'پل صدادار و بی‌صدا',
        'desc_no' => 'Hvordan det indre behovet møter det ytre uttrykket.',
    ],
    'balance' => [
        'price' => 39, 'group' => 'identity',
        'no' => 'Balansetall', 'en' => 'Balance Number', 'fa' => 'عدد تعادل',
        'desc_no' => 'Et symbolsk råd for krevende eller pressede situasjoner.',
    ],
    'karmic_debt' => [
        'price' => 39, 'group' => 'depth',
        'no' => 'Karmiske gjeldstall', 'en' => 'Karmic Debt Numbers', 'fa' => 'اعداد بدهی کارمایی',
        'desc_no' => 'Ser etter de klassiske sammentallene 13, 14, 16 og 19.',
    ],
    'karmic_lesson' => [
        'price' => 39, 'group' => 'depth',
        'no' => 'Karmiske læringstall', 'en' => 'Karmic Lessons', 'fa' => 'درس‌های کارمایی',
        'desc_no' => 'Tall som mangler i navnemønsteret og tolkes som læringsområder.',
    ],
    'health_profile' => [
        'price' => 39, 'group' => 'depth',
        'no' => 'Symbolsk helseprofil', 'en' => 'Symbolic Health Profile', 'fa' => 'پروفایل نمادین سلامت',
        'desc_no' => 'Åses symbolske helseperspektiv fra navn og livsvei – ikke medisinsk diagnostikk.',
    ],
    'pinnacles' => [
        'price' => 49, 'group' => 'cycles',
        'no' => 'Fire utviklingstrinn', 'en' => 'Four Pinnacle Cycles', 'fa' => 'چهار چرخه اوج',
        'desc_no' => 'De fire lange utviklingsperiodene i livet.',
    ],
    'life_cycles' => [
        'price' => 49, 'group' => 'cycles',
        'no' => 'Tre livsperioder', 'en' => 'Three Life Cycles', 'fa' => 'سه چرخه زندگی',
        'desc_no' => 'Åpning, midtperiode og senere livsperiode.',
    ],
    'maturity' => [
        'price' => 39, 'group' => 'cycles',
        'no' => 'Realiseringstall / Maturity', 'en' => 'Maturity / Realization Number', 'fa' => 'عدد بلوغ / تحقق',
        'desc_no' => 'Retningen som blir tydeligere med modenhet.',
    ],
    'challenges' => [
        'price' => 49, 'group' => 'cycles',
        'no' => 'Fire utfordringstall', 'en' => 'Four Challenge Numbers', 'fa' => 'چهار عدد چالش',
        'desc_no' => 'Gjennomgående læringstema i ulike livsfaser.',
    ],
    'personal_year' => [
        'price' => 39, 'group' => 'timing',
        'no' => 'Personlig år – nå', 'en' => 'Personal Year – Now', 'fa' => 'سال شخصی – اکنون',
        'desc_no' => 'Årets overordnede numerologiske klima.',
    ],
    'personal_month' => [
        'price' => 39, 'group' => 'timing',
        'no' => 'Personlig måned – nå', 'en' => 'Personal Month – Now', 'fa' => 'ماه شخصی – اکنون',
        'desc_no' => 'Den kortere rytmen inne i det personlige året.',
    ],
    'physical_transit' => [
        'price' => 39, 'group' => 'timing',
        'no' => 'Fysisk transitt', 'en' => 'Physical Transit', 'fa' => 'ترانزیت فیزیکی',
        'desc_no' => 'Aktiv bokstav fra fornavnet ved valgt alder.',
    ],
    'mental_transit' => [
        'price' => 39, 'group' => 'timing',
        'no' => 'Mental transitt', 'en' => 'Mental Transit', 'fa' => 'ترانزیت ذهنی',
        'desc_no' => 'Aktiv bokstav fra mellomnavnslaget når det finnes.',
    ],
    'spiritual_transit' => [
        'price' => 39, 'group' => 'timing',
        'no' => 'Spirituell transitt', 'en' => 'Spiritual Transit', 'fa' => 'ترانزیت معنوی',
        'desc_no' => 'Aktiv bokstav fra etternavnslaget.',
    ],
    'essence' => [
        'price' => 39, 'group' => 'timing',
        'no' => 'Essenstall – nå', 'en' => 'Essence Number – Now', 'fa' => 'عدد اسنس – اکنون',
        'desc_no' => 'Summen av de aktive navnetransittene.',
    ],
    'address' => [
        'price' => 29, 'group' => 'environment',
        'no' => 'Adressetall', 'en' => 'Address Number', 'fa' => 'عدد نشانی',
        'desc_no' => 'Tallet knyttet til adressen og bomiljøet.',
    ],
    'telephone' => [
        'price' => 29, 'group' => 'environment',
        'no' => 'Telefonnummer', 'en' => 'Telephone Number', 'fa' => 'عدد تلفن',
        'desc_no' => 'Reduksjon av telefonnummeret og sammenheng med kjernekartet.',
    ],
    'lucky' => [
        'price' => 29, 'group' => 'environment',
        'no' => 'Lykketall', 'en' => 'Lucky Number', 'fa' => 'عدد شانس',
        'desc_no' => 'Åses lykketallslag basert på fødselsdatoen.',
    ],
    'partner' => [
        'price' => 249, 'group' => 'relationship', 'outside_cap' => true,
        'no' => 'Partner / relasjonsanalyse', 'en' => 'Partner / Relationship Analysis', 'fa' => 'تحلیل شریک / رابطه',
        'desc_no' => 'Legger et andre tallkart oppå ditt og sammenligner navn og livsvei.',
    ],
];

const ANALYSIS_FUTURE = [
    0  => ['price' => 0,   'no' => 'Ingen fremtidsperiode', 'en' => 'No future period', 'fa' => 'بدون دوره آینده'],
    1  => ['price' => 49,  'no' => '1 måned', 'en' => '1 month', 'fa' => '۱ ماه'],
    3  => ['price' => 99,  'no' => '3 måneder', 'en' => '3 months', 'fa' => '۳ ماه'],
    6  => ['price' => 149, 'no' => '6 måneder', 'en' => '6 months', 'fa' => '۶ ماه'],
    12 => ['price' => 300, 'no' => '1 år', 'en' => '1 year', 'fa' => '۱ سال'],
    24 => ['price' => 400, 'no' => '2 år', 'en' => '2 years', 'fa' => '۲ سال'],
    36 => ['price' => 500, 'no' => '3 år', 'en' => '3 years', 'fa' => '۳ سال'],
];

function analysis_builder_normalize_modules(mixed $value): array
{
    if (!is_array($value)) return [];
    $allowed = array_keys(ANALYSIS_MODULES);
    $clean = [];
    foreach ($value as $module) {
        $module = trim((string) $module);
        if (in_array($module, $allowed, true) && !in_array($module, $clean, true)) {
            $clean[] = $module;
        }
    }
    return $clean;
}

function analysis_builder_future_months(mixed $value): int
{
    $months = (int) $value;
    return array_key_exists($months, ANALYSIS_FUTURE) ? $months : 0;
}

function analysis_builder_price_kr(array $modules, int $futureMonths, bool $humanReview = false): int
{
    $depth = 0;
    $outside = 0;
    foreach (analysis_builder_normalize_modules($modules) as $id) {
        $module = ANALYSIS_MODULES[$id];
        if (!empty($module['outside_cap'])) {
            $outside += (int) $module['price'];
        } else {
            $depth += (int) $module['price'];
        }
    }
    $depth = min($depth, ANALYSIS_DEPTH_CAP_KR);
    $futureMonths = analysis_builder_future_months($futureMonths);
    $future = (int) (ANALYSIS_FUTURE[$futureMonths]['price'] ?? 0);
    $human = $humanReview ? 360 : 0;
    return ANALYSIS_BASE_PRICE_KR + $depth + $outside + $future + $human;
}

function analysis_builder_label(array $item, string $lang): string
{
    return (string) ($item[$lang] ?? $item['en'] ?? $item['no'] ?? '');
}

function analysis_builder_config(array $source): array
{
    return [
        'version'       => 1,
        'modules'       => analysis_builder_normalize_modules($source['modules'] ?? []),
        'future_months' => analysis_builder_future_months($source['future_months'] ?? 0),
        'human_review'  => !empty($source['human_review']),
        'partner_name'  => trim((string) ($source['partner_name'] ?? '')),
        'partner_date'  => trim((string) ($source['partner_date'] ?? '')),
    ];
}

function analysis_builder_summary(array $config, string $lang): string
{
    $moduleCount = count($config['modules'] ?? []);
    $futureMonths = (int) ($config['future_months'] ?? 0);
    if ($lang === 'fa') {
        return 'تحلیل پایه + ' . $moduleCount . ' ماژول' . ($futureMonths ? ' + ' . $futureMonths . ' ماه آینده' : '');
    }
    if ($lang === 'en') {
        return 'Core analysis + ' . $moduleCount . ' modules' . ($futureMonths ? ' + ' . $futureMonths . ' future months' : '');
    }
    return 'Kjerneanalyse + ' . $moduleCount . ' moduler' . ($futureMonths ? ' + ' . $futureMonths . ' måneder fremtid' : '');
}
