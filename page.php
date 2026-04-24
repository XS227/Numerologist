<?php

declare(strict_types=1);

require __DIR__ . '/includes/data.php';
require __DIR__ . '/includes/layout.php';

$slug = (string) ($_GET['slug'] ?? '');
$page = $pages[$slug] ?? null;

if ($page === null) {
    http_response_code(404);
    render_header('Fant ikke siden');
    echo '<section class="card"><h1>404</h1><p>Siden finnes ikke.</p></section>';
    render_footer();
    exit;
}

render_header($page['title']);
?>
<section class="card">
  <h1><?= htmlspecialchars($page['title']) ?></h1>
  <p><?= htmlspecialchars($page['body']) ?></p>
</section>
<?php render_footer(); ?>
