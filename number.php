<?php

declare(strict_types=1);

// Legacy URL (?number=N) from before the Django /numbers/<n>/ pages existed.
// This used to re-render the whole page a second time under a second URL
// (duplicate content, same problem as the old /articles.html) — it already
// declared the Django URL as canonical, so a real redirect is strictly
// better than a soft hint, and merges the two into one URL for real.

require_once __DIR__ . '/includes/data.php';
require_once __DIR__ . '/includes/seo.php';

$number  = (int) ($_GET['number'] ?? 0);
$profile = $numberInterpretations[$number] ?? null;

if ($profile === null) {
    require __DIR__ . '/includes/layout.php';
    $lang = handle_lang_switch();
    $no   = ($lang === 'no');
    http_response_code(404);
    render_header($no ? 'Tall ikke funnet' : 'Number Not Found', [
        'title'       => $no ? 'Tall ikke funnet' : 'Number Not Found',
        'description' => $no ? 'Dette tallet har ingen numerologisk profil.' : 'This number has no numerology profile.',
        'canonical'   => SITE_URL . '/number.php',
        'lang'        => $lang,
        'noindex'     => true,
    ]);
    echo '<section class="card"><h1>404</h1><p>' .
         htmlspecialchars($no ? 'Dette tallet har ingen profil.' : 'This number has no profile.') . '</p>' .
         '<p><a href="/">' . ($no ? '← Tilbake til forsiden' : '← Back to home') . '</a></p>' .
         '</section>';
    render_footer();
    exit;
}

header('Location: ' . SITE_URL . '/numbers/' . $number . '/', true, 301);
exit;
