<?php

declare(strict_types=1);

/**
 * Dynamic XML sitemap — outputs all crawlable URLs with hreflang alternates.
 * Accessible at /sitemap.php (nginx falls through to PHP) and linked from robots.txt.
 */

header('Content-Type: application/xml; charset=utf-8');
header('X-Robots-Tag: noindex');

const BASE = 'https://numerologist.setai.no';

/**
 * @param list<array{
 *   loc:      string,
 *   alt_no?:  string,
 *   alt_en?:  string,
 *   lastmod?: string,
 *   priority?: string,
 *   changefreq?: string,
 * }> $urls
 */
function xml_url(array $url): string
{
    $loc       = htmlspecialchars($url['loc'], ENT_XML1, 'UTF-8');
    $lastmod   = htmlspecialchars($url['lastmod']   ?? date('Y-m-d'), ENT_XML1, 'UTF-8');
    $priority  = htmlspecialchars($url['priority']  ?? '0.6',        ENT_XML1, 'UTF-8');
    $changefreq = htmlspecialchars($url['changefreq'] ?? 'monthly',  ENT_XML1, 'UTF-8');

    $out = "  <url>\n";
    $out .= "    <loc>{$loc}</loc>\n";
    $out .= "    <lastmod>{$lastmod}</lastmod>\n";
    $out .= "    <changefreq>{$changefreq}</changefreq>\n";
    $out .= "    <priority>{$priority}</priority>\n";

    if (!empty($url['alt_no'])) {
        $no = htmlspecialchars($url['alt_no'], ENT_XML1, 'UTF-8');
        $out .= "    <xhtml:link rel=\"alternate\" hreflang=\"no\" href=\"{$no}\"/>\n";
    }
    if (!empty($url['alt_en'])) {
        $en = htmlspecialchars($url['alt_en'], ENT_XML1, 'UTF-8');
        $out .= "    <xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"{$en}\"/>\n";
    }
    if (!empty($url['alt_no'])) {
        $xd = htmlspecialchars($url['alt_no'], ENT_XML1, 'UTF-8');
        $out .= "    <xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"{$xd}\"/>\n";
    }

    $out .= "  </url>\n";
    return $out;
}

$today = date('Y-m-d');

// ── Static pages ─────────────────────────────────────────────────────────────
// Kept in sync by hand with tall_project/navigation.py STATIC_PAGES.
// Excluded on purpose: legal, terms-conditions, privacy-policy (noindex),
// and quranic-analysis (noindex, canonicalizes to quranian-numerology).
$staticSlugs = [
    'discover-numerology',
    'calculators',
    'pythagoras-legacy',
    'general-interpretation',
    'calculation-methods-overview',
    'letter-value-chart',
    'personal-insights',
    'compute-destiny-number',
    'compute-name-vowel-consonant',
    'lifes-fourth-stage',
    'realization-number',
    'pythagoras-arrows',
    'same-number-meaning',
    'resources',
    'projects-lab',
    'arecibo-line',
    'free-analyses',
    'blog-articles',
    'references',
    'numerologist-in-media',
    'quranian-numerology',
    'guidance-support',
    'about-the-firm',
    'telephone-guidance',
    'contact-qa',
];

// ── Number pages (Django clean URLs) ─────────────────────────────────────────
$numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33];

// ── Article pages (Django-served; hardcoded known slugs) ─────────────────────
$articleSlugs = [
    ['slug' => 'master-number-33',                                          'date' => '2025-11-12'],
    ['slug' => 'navn-og-numerologi',                                        'date' => '2025-11-03'],
    ['slug' => 'creative-research-practice-for-numerology',                 'date' => '2025-10-18'],
    ['slug' => 'numerological-reflection-on-mahsa-amini-and-bita-azizi',    'date' => '2025-11-24'],
];

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n";
echo "        xmlns:xhtml=\"http://www.w3.org/1999/xhtml\">\n\n";

// ── Homepage ──────────────────────────────────────────────────────────────────
echo xml_url([
    'loc'        => BASE . '/',
    'alt_no'     => BASE . '/',
    'alt_en'     => BASE . '/?lang=en',
    'lastmod'    => $today,
    'priority'   => '1.0',
    'changefreq' => 'weekly',
]);

// ── Static pages ──────────────────────────────────────────────────────────────
foreach ($staticSlugs as $slug) {
    echo xml_url([
        'loc'     => BASE . '/' . $slug . '/',
        'alt_no'  => BASE . '/' . $slug . '/',
        'alt_en'  => BASE . '/' . $slug . '/?lang=en',
        'lastmod' => $today,
    ]);
}

// ── Number pages ──────────────────────────────────────────────────────────────
foreach ($numbers as $n) {
    echo xml_url([
        'loc'      => BASE . '/numbers/' . $n . '/',
        'alt_no'   => BASE . '/numbers/' . $n . '/',
        'alt_en'   => BASE . '/numbers/' . $n . '/?lang=en',
        'lastmod'  => $today,
        'priority' => '0.7',
    ]);
}

// ── Article list ─────────────────────────────────────────────────────────────
echo xml_url([
    'loc'        => BASE . '/articles/',
    'alt_no'     => BASE . '/articles/',
    'alt_en'     => BASE . '/articles/?lang=en',
    'lastmod'    => $today,
    'priority'   => '0.6',
    'changefreq' => 'weekly',
]);

// ── Article pages ─────────────────────────────────────────────────────────────
foreach ($articleSlugs as $article) {
    echo xml_url([
        'loc'        => BASE . '/articles/' . $article['slug'] . '/',
        'alt_no'     => BASE . '/articles/' . $article['slug'] . '/',
        'alt_en'     => BASE . '/articles/' . $article['slug'] . '/?lang=en',
        'lastmod'    => $article['date'],
        'priority'   => '0.8',
        'changefreq' => 'monthly',
    ]);
}

echo "</urlset>\n";
