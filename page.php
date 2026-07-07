<?php

declare(strict_types=1);

require __DIR__ . '/includes/data.php';
require __DIR__ . '/includes/layout.php';

$lang = handle_lang_switch();
$no   = ($lang === 'no');

$slug = trim((string) ($_GET['slug'] ?? ''));
$page = $pages[$slug] ?? null;

if ($page === null) {
    http_response_code(404);
    $seo404 = [
        'title'       => $no ? 'Side ikke funnet' : 'Page Not Found',
        'description' => $no ? 'Siden du leter etter finnes ikke.' : 'The page you are looking for does not exist.',
        'canonical'   => SITE_URL . '/page.php',
        'lang'        => $lang,
        'noindex'     => true,
    ];
    render_header($no ? '404 – Siden finnes ikke' : '404 – Page Not Found', $seo404);
    echo '<section class="card"><h1>404</h1><p>' .
         htmlspecialchars($no ? 'Siden finnes ikke.' : 'Page not found.') . '</p>' .
         '<p><a href="/">' . ($no ? '← Tilbake til forsiden' : '← Back to home') . '</a></p>' .
         '</section>';
    render_footer();
    exit;
}

$title      = $no ? ($page['title']    ?? '') : ($page['title_en']    ?? $page['title']    ?? '');
$desc       = $no ? ($page['description'] ?? '') : ($page['desc_en'] ?? $page['description'] ?? '');
$body       = htmlspecialchars($page['body'] ?? '', ENT_QUOTES, 'UTF-8');
$noindex    = (bool) ($page['noindex'] ?? false);

// Canonical points to the clean Django URL (no ?slug= query string)
$canonical  = SITE_URL . '/' . $slug . '/';
$altNo      = SITE_URL . '/' . $slug . '/';
$altEn      = SITE_URL . '/' . $slug . '/?lang=en';

// WebPage JSON-LD
$schema = [
    '@context'    => 'https://schema.org',
    '@type'       => 'WebPage',
    'name'        => $title,
    'description' => $desc,
    'url'         => $canonical,
    'inLanguage'  => $no ? 'nb-NO' : 'en',
    'isPartOf'    => ['@type' => 'WebSite', 'url' => SITE_URL . '/'],
    'author'      => [
        '@type' => 'Person',
        'name'  => 'Åse Steinsland',
        'url'   => SITE_URL . '/',
    ],
];

// Breadcrumbs: Home → Page Title
$home = $no ? 'Hjem' : 'Home';
$breadcrumbs = [
    [$home, SITE_URL . '/'],
    [$title, $canonical],
];

render_header($title, [
    'title'       => $title,
    'description' => $desc,
    'canonical'   => $canonical,
    'lang'        => $lang,
    'alt_no'      => $altNo,
    'alt_en'      => $altEn,
    'og_type'     => 'website',
    'schema'      => $schema,
    'breadcrumbs' => $breadcrumbs,
    'noindex'     => $noindex,
]);
?>

<nav class="breadcrumb" aria-label="<?= $no ? 'Brødsmulesti' : 'Breadcrumb' ?>">
  <ol>
    <li><a href="/"><?= htmlspecialchars($home) ?></a></li>
    <li aria-current="page"><?= htmlspecialchars($title) ?></li>
  </ol>
</nav>

<article class="card">
  <h1><?= htmlspecialchars($title) ?></h1>
  <p><?= $body ?></p>
</article>

<?php render_footer(); ?>
