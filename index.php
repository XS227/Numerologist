<?php

declare(strict_types=1);

require __DIR__ . '/includes/data.php';
require __DIR__ . '/includes/layout.php';

$result = null;
$error = null;
$fullName = '';
$birthDate = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $fullName = trim((string) ($_POST['full_name'] ?? ''));
    $birthDate = (string) ($_POST['birth_date'] ?? '');

    if ($fullName === '' || $birthDate === '') {
        $error = 'Fyll inn navn og fødselsdato.';
    } else {
        $result = calculate_numerology($fullName, $birthDate);
    }
}

render_header('Hjem');
?>
<section class="card">
  <h1>Numerologist i ren PHP</h1>
  <p>Dette er en serverløs versjon (ingen Python/Django installasjon). Last opp filene via FTP på vanlig webhotell med PHP-støtte.</p>
</section>

<section class="card">
  <h2>Rask kalkulator</h2>
  <?php if ($error !== null): ?>
    <p class="error"><?= htmlspecialchars($error) ?></p>
  <?php endif; ?>
  <form method="post" class="form-grid">
    <label>
      Fullt navn
      <input type="text" name="full_name" value="<?= htmlspecialchars($fullName) ?>" required>
    </label>
    <label>
      Fødselsdato
      <input type="date" name="birth_date" value="<?= htmlspecialchars($birthDate) ?>" required>
    </label>
    <button type="submit">Beregn</button>
  </form>

  <?php if ($result !== null): ?>
    <div class="result-grid">
      <article><h3>Livsvei</h3><p><a href="/number.php?number=<?= $result['life_path'] ?>"><?= $result['life_path'] ?></a></p></article>
      <article><h3>Uttrykkstall</h3><p><?= $result['expression'] ?></p></article>
      <article><h3>Sjelstallet</h3><p><?= $result['soul_urge'] ?></p></article>
      <article><h3>Personlighet</h3><p><?= $result['personality'] ?></p></article>
    </div>
  <?php endif; ?>
</section>

<section class="card">
  <h2>Sider</h2>
  <ul>
    <?php foreach ($pages as $slug => $page): ?>
      <li><a href="/page.php?slug=<?= urlencode($slug) ?>"><?= htmlspecialchars($page['title']) ?></a></li>
    <?php endforeach; ?>
  </ul>
</section>
<?php render_footer(); ?>
