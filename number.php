<?php

declare(strict_types=1);

require __DIR__ . '/includes/data.php';
require __DIR__ . '/includes/layout.php';

$number = (int) ($_GET['number'] ?? 0);
$profile = $numberInterpretations[$number] ?? null;

if ($profile === null) {
    http_response_code(404);
    render_header('Tall ikke funnet');
    echo '<section class="card"><h1>404</h1><p>Dette tallet har ingen profil.</p></section>';
    render_footer();
    exit;
}

render_header($profile['title']);
?>
<section class="card">
  <h1><?= htmlspecialchars($profile['title']) ?></h1>
  <p><?= htmlspecialchars($profile['essence']) ?></p>
</section>
<?php render_footer(); ?>
