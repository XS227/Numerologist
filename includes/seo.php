<?php

declare(strict_types=1);

const SITE_URL  = 'https://numerologist.setai.no';
const SITE_NAME = 'Numerologist – Åse Steinsland';
const OG_IMAGE  = 'https://numerologist.setai.no/assets/og-numerologist.png';

/**
 * Outputs all SEO <head> tags and JSON-LD blocks.
 *
 * @param array{
 *   title:        string,
 *   description:  string,
 *   canonical:    string,
 *   lang?:        string,
 *   alt_no?:      string,
 *   alt_en?:      string,
 *   og_type?:     string,
 *   og_image?:    string,
 *   schema?:      array<string,mixed>,
 *   breadcrumbs?: list<array{string,string}>,
 *   noindex?:     bool,
 * } $cfg
 */
function seo_head(array $cfg): void
{
    $lang      = $cfg['lang']      ?? 'no';
    $ogType    = $cfg['og_type']   ?? 'website';
    $ogImage   = $cfg['og_image']  ?? OG_IMAGE;
    $canonical = $cfg['canonical'];
    $altNo     = $cfg['alt_no']    ?? $canonical;
    $altEn     = $cfg['alt_en']    ?? $canonical;
    $ogLocale  = ($lang === 'no')  ? 'nb_NO' : 'en_US';
    $noindex   = $cfg['noindex']   ?? false;

    $title = trim($cfg['title']);
    // Append site name only if not already present
    $fullTitle = str_contains($title, 'Numerologist') ? $title : $title . ' | ' . SITE_NAME;

    $esc = fn(string $s): string => htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');

    echo "  <title>{$esc($fullTitle)}</title>\n";
    echo "  <meta name=\"description\" content=\"{$esc($cfg['description'])}\">\n";
    if ($noindex) {
        echo "  <meta name=\"robots\" content=\"noindex,nofollow\">\n";
    }
    echo "  <link rel=\"canonical\"  href=\"{$esc($canonical)}\">\n";
    echo "  <link rel=\"alternate\" hreflang=\"no\"        href=\"{$esc($altNo)}\">\n";
    echo "  <link rel=\"alternate\" hreflang=\"en\"        href=\"{$esc($altEn)}\">\n";
    echo "  <link rel=\"alternate\" hreflang=\"x-default\" href=\"{$esc($altNo)}\">\n";

    // Open Graph
    echo "  <meta property=\"og:type\"        content=\"{$esc($ogType)}\">\n";
    echo "  <meta property=\"og:url\"         content=\"{$esc($canonical)}\">\n";
    echo "  <meta property=\"og:title\"       content=\"{$esc($title)}\">\n";
    echo "  <meta property=\"og:description\" content=\"{$esc($cfg['description'])}\">\n";
    echo "  <meta property=\"og:image\"       content=\"{$esc($ogImage)}\">\n";
    echo "  <meta property=\"og:image:width\" content=\"1200\">\n";
    echo "  <meta property=\"og:image:height\" content=\"630\">\n";
    echo "  <meta property=\"og:locale\"      content=\"{$esc($ogLocale)}\">\n";
    echo "  <meta property=\"og:site_name\"   content=\"{$esc(SITE_NAME)}\">\n";

    // Twitter / X
    echo "  <meta name=\"twitter:card\"        content=\"summary_large_image\">\n";
    echo "  <meta name=\"twitter:title\"       content=\"{$esc($title)}\">\n";
    echo "  <meta name=\"twitter:description\" content=\"{$esc($cfg['description'])}\">\n";
    echo "  <meta name=\"twitter:image\"       content=\"{$esc($ogImage)}\">\n";

    // Collect all JSON-LD blocks
    $schemas = [];

    if (!empty($cfg['schema'])) {
        $schemas[] = $cfg['schema'];
    }

    // BreadcrumbList
    if (!empty($cfg['breadcrumbs'])) {
        $items = [];
        foreach ($cfg['breadcrumbs'] as $pos => [$name, $url]) {
            $items[] = [
                '@type'    => 'ListItem',
                'position' => $pos + 1,
                'name'     => $name,
                'item'     => $url,
            ];
        }
        $schemas[] = [
            '@context'        => 'https://schema.org',
            '@type'           => 'BreadcrumbList',
            'itemListElement' => $items,
        ];
    }

    foreach ($schemas as $schema) {
        echo "  <script type=\"application/ld+json\">\n";
        echo '  ' . json_encode(
            $schema,
            JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT
        ) . "\n";
        echo "  </script>\n";
    }
}

/** Returns the active language from cookie, defaulting to 'no'. */
function current_lang(): string
{
    $l = (string) ($_COOKIE['nl_lang'] ?? 'no');
    return in_array($l, ['no', 'en'], true) ? $l : 'no';
}

/** Handles ?lang= switching and returns current lang. */
function handle_lang_switch(): string
{
    if (isset($_GET['lang'])) {
        $l = (string) $_GET['lang'];
        if (in_array($l, ['no', 'en'], true)) {
            setcookie('nl_lang', $l, [
                'expires'  => time() + 31_536_000,
                'path'     => '/',
                'samesite' => 'Lax',
                'secure'   => true,
            ]);
            // Redirect to same URL without the lang param
            $url = strtok((string) ($_SERVER['REQUEST_URI'] ?? '/'), '?');
            $params = $_GET;
            unset($params['lang']);
            if ($params) {
                $url .= '?' . http_build_query($params);
            }
            header('Location: ' . $url);
            exit;
        }
    }
    return current_lang();
}
