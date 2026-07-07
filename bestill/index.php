<?php

declare(strict_types=1);

require_once __DIR__ . '/../includes/config.php';
require_once __DIR__ . '/../includes/db.php';
require_once __DIR__ . '/../includes/vipps.php';
require_once __DIR__ . '/../includes/mail.php';
require_once __DIR__ . '/../includes/layout.php';

session_start();

// ── Packages ──────────────────────────────────────────────────────────────────
const PACKAGES = [
    'grunnpakke'  => ['name' => 'Grunnpakke',         'price' => 299, 'desc' => 'Livsveitall, sjelsurge og personlighetsprofil'],
    'fullstendig' => ['name' => 'Fullstendig profil',  'price' => 599, 'desc' => 'Komplett numerologisk kartlegging – alle kjernetall'],
    'arsanalyse'  => ['name' => 'Årsanalyse',          'price' => 399, 'desc' => 'Personlig år, måneds- og dagsplan for kommende år'],
    'par-analyse' => ['name' => 'Par-analyse',         'price' => 499, 'desc' => 'Numerologisk kompatibilitetsanalyse for to personer'],
];

// ── CSRF helper ───────────────────────────────────────────────────────────────
function csrf_token(): string
{
    if (empty($_SESSION['_csrf'])) {
        $_SESSION['_csrf'] = bin2hex(random_bytes(24));
    }
    return $_SESSION['_csrf'];
}

function csrf_verify(): void
{
    $token = (string) ($_POST['_csrf'] ?? '');
    if (!hash_equals((string) ($_SESSION['_csrf'] ?? ''), $token)) {
        http_response_code(403);
        die('Ugyldig forespørsel (CSRF).');
    }
}

// ── Sanitise helpers ──────────────────────────────────────────────────────────
function str_field(string $key, int $max = 200): string
{
    $v = trim((string) ($_POST[$key] ?? ''));
    return mb_substr($v, 0, $max);
}

function str_session(string $key, int $max = 200): string
{
    $v = (string) ($_SESSION['order'][$key] ?? '');
    return mb_substr($v, 0, $max);
}

// ── Determine current step ────────────────────────────────────────────────────
$step   = max(1, min(3, (int) ($_GET['step'] ?? 1)));
$errors = [];

// Redirect to step 1 if session is missing required earlier data
if ($step === 2 && empty($_SESSION['order']['package'])) {
    header('Location: /bestill/?step=1');
    exit;
}
if ($step === 3 && (empty($_SESSION['order']['package']) || empty($_SESSION['order']['email']))) {
    header('Location: /bestill/?step=1');
    exit;
}

// ── Handle POST ───────────────────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_verify();

    $postedStep = (int) ($_POST['step'] ?? 0);

    // Step 1: package selection
    if ($postedStep === 1) {
        $pkg = str_field('package', 20);
        if (!array_key_exists($pkg, PACKAGES)) {
            $errors[] = 'Velg en pakke.';
        } else {
            $_SESSION['order']['package']   = $pkg;
            $_SESSION['order']['price_ore'] = PACKAGES[$pkg]['price'] * 100;
            header('Location: /bestill/?step=2');
            exit;
        }
    }

    // Step 2: personal info
    if ($postedStep === 2) {
        $fields = [
            'birth_name'   => str_field('birth_name',   100),
            'current_name' => str_field('current_name', 100),
            'birth_date'   => str_field('birth_date',   10),
            'sex'          => str_field('sex',           10),
            'address'      => str_field('address',      200),
            'phone'        => preg_replace('/[^\d+\s\-\(\)]/', '', str_field('phone', 20)),
            'email'        => filter_var(str_field('email', 150), FILTER_SANITIZE_EMAIL),
        ];

        if ($fields['birth_name'] === '')   $errors[] = 'Fødselsnavn er påkrevd.';
        if ($fields['current_name'] === '') $errors[] = 'Nåværende navn er påkrevd.';
        if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $fields['birth_date'])) {
            $errors[] = 'Ugyldig fødselsdato.';
        }
        if (!in_array($fields['sex'], ['M', 'F', 'X'], true)) {
            $errors[] = 'Velg kjønn.';
        }
        if ($fields['address'] === '') $errors[] = 'Adresse er påkrevd.';
        if (!preg_match('/^[\d+][\d\s\-\(\)]{6,18}$/', $fields['phone'])) {
            $errors[] = 'Ugyldig telefonnummer.';
        }
        if (!filter_var($fields['email'], FILTER_VALIDATE_EMAIL)) {
            $errors[] = 'Ugyldig e-postadresse.';
        }

        if (empty($errors)) {
            $_SESSION['order'] = array_merge($_SESSION['order'] ?? [], $fields);
            header('Location: /bestill/?step=3');
            exit;
        }
        $step = 2; // re-render with errors
    }

    // Step 3: initiate Vipps payment
    if ($postedStep === 3) {
        $order = $_SESSION['order'] ?? [];
        if (empty($order['email'])) {
            header('Location: /bestill/?step=1');
            exit;
        }

        $pkg       = $order['package'];
        $pkgData   = PACKAGES[$pkg];
        $priceOre  = (int) $order['price_ore'];
        $authToken = bin2hex(random_bytes(24)); // stored + sent to Vipps

        try {
            $orderId = save_order([
                'package'         => $pkgData['name'],
                'price_ore'       => $priceOre,
                'birth_name'      => $order['birth_name'],
                'current_name'    => $order['current_name'],
                'birth_date'      => $order['birth_date'],
                'sex'             => $order['sex'],
                'address'         => $order['address'],
                'phone'           => $order['phone'],
                'email'           => $order['email'],
                'vipps_auth_token' => $authToken,
            ]);

            $redirectUrl = Vipps::initiatePayment(
                orderId:         $orderId,
                amountOre:       $priceOre,
                transactionText: $pkgData['name'] . ' – Numerologist',
                phone:           $order['phone'],
                authToken:       $authToken,
            );

            // Clear session order data after successful initiation
            unset($_SESSION['order']);

            header('Location: ' . $redirectUrl);
            exit;

        } catch (RuntimeException $e) {
            error_log('Vipps initiate error: ' . $e->getMessage());
            $errors[] = 'Betalingstjenesten er midlertidig utilgjengelig. Prøv igjen om litt, eller kontakt oss.';
            $step = 3;
        }
    }
}

// ── Render helpers ────────────────────────────────────────────────────────────
$lang  = handle_lang_switch();
$no    = ($lang === 'no');
$order = $_SESSION['order'] ?? [];

render_header($no ? 'Bestill analyse' : 'Order Analysis', [
    'title'       => $no ? 'Bestill numerologianalyse' : 'Order Numerology Analysis',
    'description' => $no
        ? 'Velg pakke og bestill din personlige numerologianalyse hos Åse Steinsland.'
        : 'Choose a package and order your personal numerology analysis.',
    'canonical'   => SITE_URL . '/bestill/',
    'lang'        => $lang,
    'noindex'     => true,
]);

$csrf = csrf_token();

function error_list(array $errors): void
{
    if (empty($errors)) return;
    echo '<ul class="form-errors" role="alert">';
    foreach ($errors as $e) {
        echo '<li>' . htmlspecialchars($e, ENT_QUOTES, 'UTF-8') . '</li>';
    }
    echo '</ul>';
}

function sel(string $val, string $test): string
{
    return $val === $test ? ' selected' : '';
}

function checked(string $val, string $test): string
{
    return $val === $test ? ' checked' : '';
}

?>
<link rel="stylesheet" href="/assets/bestill.css">

<nav class="breadcrumb" aria-label="Brødsmulesti">
  <ol>
    <li><a href="/">Hjem</a></li>
    <li aria-current="page">Bestill</li>
  </ol>
</nav>

<!-- Step indicator -->
<div class="stepper" aria-label="Stegindikator">
  <div class="stepper-inner">
    <div class="step <?= $step >= 1 ? 'step--done' : '' ?> <?= $step === 1 ? 'step--active' : '' ?>">
      <span class="step-num">1</span>
      <span class="step-label"><?= $no ? 'Pakke' : 'Package' ?></span>
    </div>
    <div class="step-line <?= $step >= 2 ? 'step-line--done' : '' ?>"></div>
    <div class="step <?= $step >= 2 ? 'step--done' : '' ?> <?= $step === 2 ? 'step--active' : '' ?>">
      <span class="step-num">2</span>
      <span class="step-label"><?= $no ? 'Opplysninger' : 'Your Info' ?></span>
    </div>
    <div class="step-line <?= $step >= 3 ? 'step-line--done' : '' ?>"></div>
    <div class="step <?= $step === 3 ? 'step--active' : '' ?>">
      <span class="step-num">3</span>
      <span class="step-label"><?= $no ? 'Betal' : 'Pay' ?></span>
    </div>
  </div>
</div>

<?php if ($step === 1): ?>
<!-- ══ STEP 1 — Choose package ════════════════════════════════════════════════ -->
<section class="card order-card">
  <h1><?= $no ? 'Velg pakke' : 'Choose package' ?></h1>
  <p class="order-intro">
    <?= $no
        ? 'Alle analyser leveres skriftlig per e-post innen 5–7 virkedager.'
        : 'All analyses are delivered in writing by email within 5–7 business days.' ?>
  </p>
  <?php error_list($errors); ?>
  <form method="post" action="/bestill/?step=1" class="pkg-form" novalidate>
    <input type="hidden" name="step" value="1">
    <input type="hidden" name="_csrf" value="<?= htmlspecialchars($csrf, ENT_QUOTES) ?>">

    <div class="pkg-grid" role="radiogroup" aria-label="Velg analysepakke">
      <?php foreach (PACKAGES as $key => $pkg): ?>
        <label class="pkg-card <?= $key === ($order['package'] ?? '') ? 'pkg-card--selected' : '' ?>">
          <input type="radio" name="package" value="<?= $key ?>"
                 <?= checked($order['package'] ?? '', $key) ?> required>
          <span class="pkg-name"><?= htmlspecialchars($pkg['name']) ?></span>
          <span class="pkg-price"><?= $pkg['price'] ?> kr</span>
          <span class="pkg-desc"><?= htmlspecialchars($pkg['desc']) ?></span>
        </label>
      <?php endforeach; ?>
    </div>

    <button type="submit" class="btn-primary">
      <?= $no ? 'Gå videre →' : 'Continue →' ?>
    </button>
  </form>
</section>

<?php elseif ($step === 2): ?>
<!-- ══ STEP 2 — Personal info ═════════════════════════════════════════════════ -->
<?php
$selPkg    = $order['package'] ?? '';
$pkgInfo   = PACKAGES[$selPkg] ?? null;
?>
<section class="card order-card">
  <h1><?= $no ? 'Dine opplysninger' : 'Your details' ?></h1>
  <?php if ($pkgInfo): ?>
    <div class="selected-pkg-badge">
      <?= htmlspecialchars($pkgInfo['name']) ?> &mdash; <?= $pkgInfo['price'] ?> kr
      <a href="/bestill/?step=1" class="change-link"><?= $no ? '(endre)' : '(change)' ?></a>
    </div>
  <?php endif; ?>
  <?php error_list($errors); ?>
  <form method="post" action="/bestill/?step=2" class="info-form" novalidate>
    <input type="hidden" name="step" value="2">
    <input type="hidden" name="_csrf" value="<?= htmlspecialchars($csrf, ENT_QUOTES) ?>">

    <div class="field-row">
      <div class="field">
        <label for="birth_name"><?= $no ? 'Fullt fødselsnavn *' : 'Full birth name *' ?></label>
        <input id="birth_name" name="birth_name" type="text" autocomplete="off"
               value="<?= htmlspecialchars($order['birth_name'] ?? '', ENT_QUOTES) ?>"
               placeholder="<?= $no ? 'Slik det står i fødselsattest' : 'As in birth certificate' ?>" required>
        <small><?= $no ? 'Nøyaktig navn ved fødsel, inkl. mellomnavn.' : 'Exact name at birth, incl. middle names.' ?></small>
      </div>
      <div class="field">
        <label for="current_name"><?= $no ? 'Nåværende navn *' : 'Current name *' ?></label>
        <input id="current_name" name="current_name" type="text" autocomplete="name"
               value="<?= htmlspecialchars($order['current_name'] ?? '', ENT_QUOTES) ?>"
               placeholder="<?= $no ? 'Navn du bruker til daglig' : 'Name you use daily' ?>" required>
      </div>
    </div>

    <div class="field-row">
      <div class="field">
        <label for="birth_date"><?= $no ? 'Fødselsdato *' : 'Date of birth *' ?></label>
        <input id="birth_date" name="birth_date" type="date"
               value="<?= htmlspecialchars($order['birth_date'] ?? '', ENT_QUOTES) ?>"
               max="<?= date('Y-m-d') ?>" required>
      </div>
      <div class="field">
        <label for="sex"><?= $no ? 'Kjønn *' : 'Gender *' ?></label>
        <select id="sex" name="sex" required>
          <option value=""><?= $no ? '— velg —' : '— select —' ?></option>
          <option value="F"<?= sel($order['sex'] ?? '', 'F') ?>><?= $no ? 'Kvinne' : 'Female' ?></option>
          <option value="M"<?= sel($order['sex'] ?? '', 'M') ?>><?= $no ? 'Mann' : 'Male' ?></option>
          <option value="X"<?= sel($order['sex'] ?? '', 'X') ?>><?= $no ? 'Annet / ikke spesifisert' : 'Other / not specified' ?></option>
        </select>
      </div>
    </div>

    <div class="field">
      <label for="address"><?= $no ? 'Adresse *' : 'Address *' ?></label>
      <input id="address" name="address" type="text" autocomplete="street-address"
             value="<?= htmlspecialchars($order['address'] ?? '', ENT_QUOTES) ?>"
             placeholder="<?= $no ? 'Gateadresse, postnummer, sted' : 'Street, postal code, city' ?>" required>
    </div>

    <div class="field-row">
      <div class="field">
        <label for="phone"><?= $no ? 'Mobilnummer *' : 'Mobile number *' ?></label>
        <input id="phone" name="phone" type="tel" autocomplete="tel"
               value="<?= htmlspecialchars($order['phone'] ?? '', ENT_QUOTES) ?>"
               placeholder="<?= $no ? '+47 9XX XX XXX' : '+47 9XX XX XXX' ?>" required>
        <small><?= $no ? 'Brukes for Vipps-betaling.' : 'Used for Vipps payment.' ?></small>
      </div>
      <div class="field">
        <label for="email"><?= $no ? 'E-postadresse *' : 'Email address *' ?></label>
        <input id="email" name="email" type="email" autocomplete="email"
               value="<?= htmlspecialchars($order['email'] ?? '', ENT_QUOTES) ?>"
               placeholder="din@epost.no" required>
        <small><?= $no ? 'Analysen sendes hit.' : 'Analysis delivered here.' ?></small>
      </div>
    </div>

    <div class="form-actions">
      <a href="/bestill/?step=1" class="btn-ghost">← <?= $no ? 'Tilbake' : 'Back' ?></a>
      <button type="submit" class="btn-primary">
        <?= $no ? 'Gå til betaling →' : 'Go to payment →' ?>
      </button>
    </div>
  </form>
</section>

<?php elseif ($step === 3): ?>
<!-- ══ STEP 3 — Review + Pay ═════════════════════════════════════════════════ -->
<?php
$selPkg  = $order['package'] ?? '';
$pkgInfo = PACKAGES[$selPkg] ?? null;
?>
<section class="card order-card">
  <h1><?= $no ? 'Gjennomgang og betaling' : 'Review and payment' ?></h1>
  <?php error_list($errors); ?>

  <div class="review-grid">
    <div class="review-section">
      <h2><?= $no ? 'Din pakke' : 'Your package' ?></h2>
      <?php if ($pkgInfo): ?>
        <div class="review-pkg">
          <strong><?= htmlspecialchars($pkgInfo['name']) ?></strong>
          <span class="review-price"><?= $pkgInfo['price'] ?> kr</span>
          <p><?= htmlspecialchars($pkgInfo['desc']) ?></p>
        </div>
      <?php endif; ?>
    </div>

    <div class="review-section">
      <h2><?= $no ? 'Dine opplysninger' : 'Your details' ?></h2>
      <dl class="review-dl">
        <dt><?= $no ? 'Fødselsnavn' : 'Birth name' ?></dt>
        <dd><?= htmlspecialchars($order['birth_name'] ?? '') ?></dd>
        <dt><?= $no ? 'Nåværende navn' : 'Current name' ?></dt>
        <dd><?= htmlspecialchars($order['current_name'] ?? '') ?></dd>
        <dt><?= $no ? 'Fødselsdato' : 'Date of birth' ?></dt>
        <dd><?= htmlspecialchars($order['birth_date'] ?? '') ?></dd>
        <dt><?= $no ? 'Kjønn' : 'Gender' ?></dt>
        <dd><?= match($order['sex'] ?? '') {
            'F' => $no ? 'Kvinne' : 'Female',
            'M' => $no ? 'Mann' : 'Male',
            'X' => $no ? 'Annet' : 'Other',
            default => '',
        } ?></dd>
        <dt><?= $no ? 'Telefon' : 'Phone' ?></dt>
        <dd><?= htmlspecialchars($order['phone'] ?? '') ?></dd>
        <dt>E-post</dt>
        <dd><?= htmlspecialchars($order['email'] ?? '') ?></dd>
        <dt><?= $no ? 'Adresse' : 'Address' ?></dt>
        <dd><?= htmlspecialchars($order['address'] ?? '') ?></dd>
      </dl>
    </div>
  </div>

  <div class="total-row">
    <span><?= $no ? 'Totalt å betale' : 'Total to pay' ?></span>
    <strong><?= $pkgInfo['price'] ?? 0 ?> kr</strong>
  </div>

  <form method="post" action="/bestill/?step=3" class="pay-form">
    <input type="hidden" name="step" value="3">
    <input type="hidden" name="_csrf" value="<?= htmlspecialchars($csrf, ENT_QUOTES) ?>">

    <button type="submit" class="btn-vipps" aria-label="Betal med Vipps">
      <svg width="80" height="28" viewBox="0 0 80 28" aria-hidden="true" fill="none" xmlns="http://www.w3.org/2000/svg">
        <text x="4" y="21" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="white">Betal med</text>
      </svg>
      <span class="vipps-logo" aria-label="Vipps">Vipps</span>
    </button>

    <p class="pay-note">
      <?= $no
          ? 'Du sendes til Vipps for sikker betaling. Analysen leveres per e-post etter betaling er bekreftet.'
          : 'You will be sent to Vipps for secure payment. Analysis delivered by email after payment confirmed.' ?>
    </p>
  </form>

  <div class="review-edit-links">
    <a href="/bestill/?step=1">← <?= $no ? 'Endre pakke' : 'Change package' ?></a>
    <a href="/bestill/?step=2">← <?= $no ? 'Endre opplysninger' : 'Edit details' ?></a>
  </div>
</section>
<?php endif; ?>

<script>
// Highlight selected package card on click
document.querySelectorAll('.pkg-card').forEach(function(card) {
  card.addEventListener('click', function() {
    document.querySelectorAll('.pkg-card').forEach(function(c) {
      c.classList.remove('pkg-card--selected');
    });
    this.classList.add('pkg-card--selected');
  });
});
</script>

<?php render_footer(); ?>
