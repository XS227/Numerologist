<?php

declare(strict_types=1);

require __DIR__ . '/includes/data.php';
require __DIR__ . '/includes/layout.php';

$lang = handle_lang_switch();
$no   = ($lang === 'no');

$number  = (int) ($_GET['number'] ?? 0);
$profile = $numberInterpretations[$number] ?? null;

if ($profile === null) {
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

$title   = $no ? ($profile['title']      ?? '') : ($profile['title_en']   ?? $profile['title']   ?? '');
$essence = $no ? ($profile['essence']    ?? '') : ($profile['essence_en'] ?? $profile['essence'] ?? '');
$desc    = $no ? ($profile['description'] ?? '') : ($profile['desc_en']   ?? $profile['description'] ?? '');

$isMaster = in_array($number, [11, 22, 33], true);

// Canonical = clean Django URL
$canonical = SITE_URL . '/numbers/' . $number . '/';
$altNo     = $canonical;
$altEn     = $canonical . '?lang=en';

// Thing/DefinedTerm schema representing the numerological concept
$schema = [
    '@context'    => 'https://schema.org',
    '@type'       => 'DefinedTerm',
    'name'        => $title,
    'description' => $desc,
    'url'         => $canonical,
    'inDefinedTermSet' => [
        '@type' => 'DefinedTermSet',
        'name'  => $no ? 'Numerologiske tall – Åse Steinsland' : 'Numerological Numbers – Åse Steinsland',
        'url'   => SITE_URL . '/',
    ],
];

// Breadcrumbs: Home → (Master) Numbers → This number
$home     = $no ? 'Hjem'          : 'Home';
$numLabel = $no ? ($isMaster ? 'Mestertall' : 'Tall i numerologi') : ($isMaster ? 'Master numbers' : 'Numbers');
$breadcrumbs = [
    [$home,     SITE_URL . '/'],
    [$numLabel, SITE_URL . '/calculators/'],
    [$title,    $canonical],
];

render_header($title, [
    'title'       => $title,
    'description' => $desc,
    'canonical'   => $canonical,
    'lang'        => $lang,
    'alt_no'      => $altNo,
    'alt_en'      => $altEn,
    'og_type'     => 'article',
    'schema'      => $schema,
    'breadcrumbs' => $breadcrumbs,
]);
?>

<nav class="breadcrumb" aria-label="<?= $no ? 'Brødsmulesti' : 'Breadcrumb' ?>">
  <ol>
    <li><a href="/"><?= htmlspecialchars($home) ?></a></li>
    <li><a href="/calculators/"><?= htmlspecialchars($numLabel) ?></a></li>
    <li aria-current="page"><?= htmlspecialchars($title) ?></li>
  </ol>
</nav>

<article class="card" aria-labelledby="num-title">
  <?php if ($isMaster): ?>
    <span class="num-badge"><?= $no ? 'Mestertall' : 'Master number' ?></span>
  <?php endif; ?>
  <h1 id="num-title"><?= htmlspecialchars($title) ?></h1>
  <p class="num-essence"><?= htmlspecialchars($essence) ?></p>
  <?php if ($desc): ?>
    <p class="num-desc"><?= htmlspecialchars($desc) ?></p>
  <?php endif; ?>

  <div class="num-actions">
    <a href="/#kalkulator" class="l-btn-sm">
      <?= $no ? 'Beregn ditt livsveitall' : 'Calculate your life path' ?>
    </a>
    <a href="/numbers/<?= ($number - 1 > 0 && isset($numberInterpretations[$number - 1])) ? $number - 1 : $number ?>/
    " class="l-btn-ghost"><?= $no ? '← Forrige tall' : '← Previous number' ?></a>
  </div>
</article>

<?php render_footer(); ?>
