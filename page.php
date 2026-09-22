<?php

declare(strict_types=1);

// Legacy URL (?slug=X) from before the Django clean-URL static pages
// existed. This used to re-render the whole page a second time under a
// second URL (duplicate content, same problem as the old /articles.html)
// — it already declared the Django URL as canonical, so a real redirect
// is strictly better than a soft hint, and merges the two into one URL
// for real.

require_once __DIR__ . '/includes/data.php';
require_once __DIR__ . '/includes/seo.php';

$slug = trim((string) ($_GET['slug'] ?? ''));
$page = $pages[$slug] ?? null;

if ($page === null) {
    require_once __DIR__ . '/includes/layout.php';
    $lang = handle_lang_switch();
    $no   = ($lang === 'no');
    http_response_code(404);
    render_header($no ? 'Side ikke funnet' : 'Page Not Found', [
        'title'       => $no ? 'Side ikke funnet' : 'Page Not Found',
        'description' => $no ? 'Siden du leter etter finnes ikke.' : 'The page you are looking for does not exist.',
        'canonical'   => SITE_URL . '/page.php',
        'lang'        => $lang,
        'noindex'     => true,
    ]);
    echo '<section class="card"><h1>404</h1><p>' .
         htmlspecialchars($no ? 'Siden finnes ikke.' : 'Page not found.') . '</p>' .
         '<p><a href="/">' . ($no ? '← Tilbake til forsiden' : '← Back to home') . '</a></p>' .
         '</section>';
    render_footer();
    exit;
}

header('Location: ' . SITE_URL . '/' . $slug . '/', true, 301);
exit;
