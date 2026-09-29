<?php

declare(strict_types=1);

require_once __DIR__ . '/../includes/config.php';
require_once __DIR__ . '/../includes/db.php';
require_once __DIR__ . '/../includes/vipps.php';
require_once __DIR__ . '/../includes/mail.php';
require_once __DIR__ . '/../includes/layout.php';

session_start();

// Language first, so validation errors below speak the visitor's language too.
$lang = handle_lang_switch();
$t    = fn(string $no, string $en, string $fa): string => nl_pick($lang, $no, $en, $fa);
$back = nl_is_rtl($lang) ? '→' : '←';

// ── Packages ──────────────────────────────────────────────────────────────────
const PACKAGES = [
    'ase227'      => ['name' => 'ÅSE 227 Edition', 'price' => 227,  'desc' => 'Digital fullrapport fra den komplette Numerologist-motoren'],
    'personlighet'=> ['name' => 'Personlighetsanalyse', 'price' => 698, 'desc' => 'Åses personlige analyse av personlighet, karmiske tema og lykketall'],
    'fremtid2'    => ['name' => 'Fremtidsanalyse 2 år', 'price' => 698, 'desc' => 'Årlig og månedlig analyse for de neste 2 årene'],
    'partner'     => ['name' => 'Partneranalyse + 1 år', 'price' => 798, 'desc' => 'Relasjon, kompatibilitet og 1 års fremtidsanalyse'],
    'komplett1'   => ['name' => 'Komplett analyse + 1 år', 'price' => 998, 'desc' => 'Personlighet, karma, helse, sykluser, transitter og 1 år fremover'],
    'komplett2'   => ['name' => 'Komplett analyse + 2 år', 'price' => 1098,'desc' => 'Personlighet, karma, helse, sykluser, transitter og 2 år fremover'],
    'komplett3'   => ['name' => 'Komplett analyse + 3 år', 'price' => 1198,'desc' => 'Personlighet, karma, helse, sykluser, transitter og 3 år fremover'],
    'veiledning15'=> ['name' => 'Veiledningssamtale 15 min', 'price' => 360, 'desc' => '15 minutter direkte med Åse, basert på 24 kr per minutt'],
    'familie3'    => ['name' => '3 komplette analyser + 1 år', 'price' => 2994,'desc' => 'Tre komplette analyser, hver med 1 års fremtidsanalyse'],
];

// Display names/descriptions per language. PACKAGES above stays the source
// for the order record and the Vipps transaction text.
const PACKAGE_LABELS = [
    'ase227' => [
        'en' => ['ÅSE 227 Edition', 'Digital complete report from the full Numerologist engine'],
        'fa' => ['نسخه ÅSE 227', 'گزارش دیجیتال کامل از موتور جامع Numerologist'],
    ],
    'personlighet' => [
        'en' => ['Personality Analysis', 'Åse’s personal analysis of personality, karmic themes and lucky numbers'],
        'fa' => ['تحلیل شخصیت', 'تحلیل شخصی Åse از شخصیت، موضوع‌های کارمایی و اعداد شانس'],
    ],
    'fremtid2' => [
        'en' => ['2-Year Future Analysis', 'Annual and monthly analysis for the next two years'],
        'fa' => ['تحلیل آینده ۲ ساله', 'تحلیل سالانه و ماهانه برای دو سال آینده'],
    ],
    'partner' => [
        'en' => ['Partner Analysis + 1 Year', 'Relationship compatibility and one year of future analysis'],
        'fa' => ['تحلیل رابطه + ۱ سال', 'سازگاری رابطه و یک سال تحلیل آینده'],
    ],
    'komplett1' => ['en' => ['Complete Analysis + 1 Year', 'Full Åse analysis plus 1 year'], 'fa' => ['تحلیل کامل + ۱ سال', 'تحلیل کامل Åse به‌همراه یک سال آینده']],
    'komplett2' => ['en' => ['Complete Analysis + 2 Years', 'Full Åse analysis plus 2 years'], 'fa' => ['تحلیل کامل + ۲ سال', 'تحلیل کامل Åse به‌همراه دو سال آینده']],
    'komplett3' => ['en' => ['Complete Analysis + 3 Years', 'Full Åse analysis plus 3 years'], 'fa' => ['تحلیل کامل + ۳ سال', 'تحلیل کامل Åse به‌همراه سه سال آینده']],
    'veiledning15' => ['en' => ['15-Minute Guidance Call', '15 minutes directly with Åse'], 'fa' => ['گفت‌وگوی ۱۵ دقیقه‌ای', '۱۵ دقیقه گفت‌وگوی مستقیم با Åse']],
    'familie3' => ['en' => ['3 Complete Analyses + 1 Year', 'Three complete analyses, each with one future year'], 'fa' => ['۳ تحلیل کامل + ۱ سال', 'سه تحلیل کامل، هرکدام با یک سال آینده']],
];

/** [name, description] of a package in the visitor's language. */
function package_label(string $key, string $lang): array
{
    $pkg = PACKAGES[$key] ?? null;
    if ($pkg === null) {
        return ['', ''];
    }
    return PACKAGE_LABELS[$key][$lang] ?? [$pkg['name'], $pkg['desc']];
}

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
        die(nl_t('Ugyldig forespørsel (CSRF).', 'Invalid request (CSRF).', 'درخواست نامعتبر (CSRF).'));
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

// Direct package links from ÅSE Edition / results. Selecting is not a payment action.
$directPackage = trim((string) ($_GET['package'] ?? ''));
if ($directPackage !== '' && array_key_exists($directPackage, PACKAGES)) {
    $_SESSION['order']['package'] = $directPackage;
    $_SESSION['order']['price_ore'] = PACKAGES[$directPackage]['price'] * 100;
    header('Location: /bestill/?step=2');
    exit;
}

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
            $errors[] = $t('Velg en pakke.', 'Choose a package.', 'یک بسته انتخاب کنید.');
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
            'sex'          => str_field('sex',           10) ?: 'X',
            'address'      => str_field('address',      200),
            'phone'        => preg_replace('/[^\d+\s\-\(\)]/', '', str_field('phone', 20)),
            'email'        => filter_var(str_field('email', 150), FILTER_SANITIZE_EMAIL),
            'notes'        => str_field('notes', 2000),
        ];

        if ($fields['birth_name'] === '')   $errors[] = $t('Fødselsnavn er påkrevd.', 'Birth name is required.', 'نام هنگام تولد الزامی است.');
        if ($fields['current_name'] === '') $errors[] = $t('Nåværende navn er påkrevd.', 'Current name is required.', 'نام فعلی الزامی است.');
        if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $fields['birth_date'])) {
            $errors[] = $t('Ugyldig fødselsdato.', 'Invalid date of birth.', 'تاریخ تولد نامعتبر است.');
        }
        if (!in_array($fields['sex'], ['M', 'F', 'X'], true)) {
            $errors[] = $t('Velg kjønn.', 'Choose a gender.', 'جنسیت را انتخاب کنید.');
        }
        $addressOptional = in_array((string) ($_SESSION['order']['package'] ?? ''), ['ase227', 'veiledning15'], true);
        if (!$addressOptional && $fields['address'] === '') $errors[] = $t('Adresse er påkrevd for denne analysen.', 'Address is required for this analysis.', 'برای این تحلیل نشانی الزامی است.');
        $needsExtra = in_array((string) ($_SESSION['order']['package'] ?? ''), ['partner', 'familie3'], true);
        if ($needsExtra && $fields['notes'] === '') $errors[] = $t('Legg inn opplysningene om den/de andre personen(e).', 'Enter the details for the other person/people.', 'اطلاعات فرد یا افراد دیگر را وارد کنید.');
        if (!preg_match('/^[\d+][\d\s\-\(\)]{6,18}$/', $fields['phone'])) {
            $errors[] = $t('Ugyldig telefonnummer.', 'Invalid phone number.', 'شماره‌ی تلفن نامعتبر است.');
        }
        if (!filter_var($fields['email'], FILTER_VALIDATE_EMAIL)) {
            $errors[] = $t('Ugyldig e-postadresse.', 'Invalid email address.', 'نشانی ایمیل نامعتبر است.');
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
                'notes'           => $order['notes'] ?? '',
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
            $errors[] = $t('Betalingstjenesten er midlertidig utilgjengelig. Prøv igjen om litt, eller kontakt oss.', 'The payment service is temporarily unavailable. Please try again shortly, or contact us.', 'سرویس پرداخت موقتاً در دسترس نیست. کمی بعد دوباره تلاش کنید یا با ما تماس بگیرید.');
            $step = 3;
        }
    }
}

// ── Render helpers ────────────────────────────────────────────────────────────
$order = $_SESSION['order'] ?? [];

render_header($t('Bestill analyse', 'Order Analysis', 'سفارش تحلیل'), [
    'title'       => $t('Bestill numerologianalyse', 'Order Numerology Analysis', 'سفارش تحلیل عددشناسی'),
    'description' => $t('Velg pakke og bestill din personlige numerologianalyse hos Åse Steinsland.', 'Choose a package and order your personal numerology analysis.', 'بسته‌ی مورد نظر را انتخاب کنید و تحلیل عددشناسی شخصی خود را از اوسه استاینسلند سفارش دهید.'),
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

<nav class="breadcrumb" aria-label="<?= $t('Brødsmulesti', 'Breadcrumb', 'مسیر صفحه') ?>">
  <ol>
    <li><a href="/"><?= $t('Hjem', 'Home', 'خانه') ?></a></li>
    <li aria-current="page"><?= $t('Bestill', 'Order', 'سفارش') ?></li>
  </ol>
</nav>

<!-- Step indicator -->
<div class="stepper" aria-label="<?= $t('Stegindikator', 'Progress', 'مراحل') ?>">
  <div class="stepper-inner">
    <div class="step <?= $step >= 1 ? 'step--done' : '' ?> <?= $step === 1 ? 'step--active' : '' ?>">
      <span class="step-num">1</span>
      <span class="step-label"><?= $t('Pakke', 'Package', 'بسته') ?></span>
    </div>
    <div class="step-line <?= $step >= 2 ? 'step-line--done' : '' ?>"></div>
    <div class="step <?= $step >= 2 ? 'step--done' : '' ?> <?= $step === 2 ? 'step--active' : '' ?>">
      <span class="step-num">2</span>
      <span class="step-label"><?= $t('Opplysninger', 'Your Info', 'اطلاعات شما') ?></span>
    </div>
    <div class="step-line <?= $step >= 3 ? 'step-line--done' : '' ?>"></div>
    <div class="step <?= $step === 3 ? 'step--active' : '' ?>">
      <span class="step-num">3</span>
      <span class="step-label"><?= $t('Betal', 'Pay', 'پرداخت') ?></span>
    </div>
  </div>
</div>

<?php if ($step === 1): ?>
<!-- ══ STEP 1 — Choose package ════════════════════════════════════════════════ -->
<section class="card order-card">
  <h1><?= $t('Velg pakke', 'Choose package', 'انتخاب بسته') ?></h1>
  <p class="order-intro">
    <?= $t('Velg den pakken som passer ønsket ditt. Åses personlige analyser leveres normalt per e-post innen 5–7 virkedager; ÅSE 227 er den digitale motorpakken.', 'Choose the package that fits your goal. Åse’s personal analyses are normally delivered by email within 5–7 business days; ÅSE 227 is the digital engine package.', 'بسته‌ای را انتخاب کنید که با هدف شما هماهنگ است. تحلیل‌های شخصی Åse معمولاً طی ۵ تا ۷ روز کاری با ایمیل ارسال می‌شوند؛ ÅSE 227 بسته دیجیتال موتور است.') ?>
  </p>
  <?php error_list($errors); ?>
  <form method="post" action="/bestill/?step=1" class="pkg-form" novalidate>
    <input type="hidden" name="step" value="1">
    <input type="hidden" name="_csrf" value="<?= htmlspecialchars($csrf, ENT_QUOTES) ?>">

    <div class="pkg-grid" role="radiogroup" aria-label="<?= $t('Velg analysepakke', 'Choose an analysis package', 'انتخاب بسته‌ی تحلیل') ?>">
      <?php foreach (PACKAGES as $key => $pkg): ?>
        <label class="pkg-card <?= $key === ($order['package'] ?? '') ? 'pkg-card--selected' : '' ?>">
          <input type="radio" name="package" value="<?= $key ?>"
                 <?= checked($order['package'] ?? '', $key) ?> required>
          <?php [$pkgName, $pkgDesc] = package_label($key, $lang); ?>
          <span class="pkg-name"><?= htmlspecialchars($pkgName) ?></span>
          <span class="pkg-price"><?= $pkg['price'] ?> kr</span>
          <span class="pkg-desc"><?= htmlspecialchars($pkgDesc) ?></span>
        </label>
      <?php endforeach; ?>
    </div>

    <button type="submit" class="btn-primary">
      <?= $t('Gå videre →', 'Continue →', 'ادامه ←') ?>
    </button>
  </form>
</section>

<?php elseif ($step === 2): ?>
<!-- ══ STEP 2 — Personal info ═════════════════════════════════════════════════ -->
<?php
$selPkg    = $order['package'] ?? '';
$pkgInfo   = PACKAGES[$selPkg] ?? null;
[$pkgName, $pkgDesc] = package_label($selPkg, $lang);
?>
<section class="card order-card">
  <h1><?= $t('Dine opplysninger', 'Your details', 'اطلاعات شما') ?></h1>
  <?php if ($pkgInfo): ?>
    <div class="selected-pkg-badge">
      <?= htmlspecialchars($pkgName) ?> &mdash; <?= $pkgInfo['price'] ?> kr
      <a href="/bestill/?step=1" class="change-link"><?= $t('(endre)', '(change)', '(تغییر)') ?></a>
    </div>
  <?php endif; ?>
  <?php error_list($errors); ?>
  <form method="post" action="/bestill/?step=2" class="info-form" novalidate>
    <input type="hidden" name="step" value="2">
    <input type="hidden" name="_csrf" value="<?= htmlspecialchars($csrf, ENT_QUOTES) ?>">

    <div class="field-row">
      <div class="field">
        <label for="birth_name"><?= $t('Fullt fødselsnavn *', 'Full birth name *', 'نام کامل هنگام تولد *') ?></label>
        <input id="birth_name" name="birth_name" type="text" autocomplete="off"
               value="<?= htmlspecialchars($order['birth_name'] ?? '', ENT_QUOTES) ?>"
               placeholder="<?= $t('Slik det står i fødselsattest', 'As in birth certificate', 'همان‌طور که در شناسنامه آمده است') ?>" required>
        <small><?= $t('Nøyaktig navn ved fødsel, inkl. mellomnavn.', 'Exact name at birth, incl. middle names.', 'نام دقیق هنگام تولد، همراه با نام‌های میانی.') ?></small>
      </div>
      <div class="field">
        <label for="current_name"><?= $t('Nåværende navn *', 'Current name *', 'نام فعلی *') ?></label>
        <input id="current_name" name="current_name" type="text" autocomplete="name"
               value="<?= htmlspecialchars($order['current_name'] ?? '', ENT_QUOTES) ?>"
               placeholder="<?= $t('Navn du bruker til daglig', 'Name you use daily', 'نامی که هر روز از آن استفاده می‌کنید') ?>" required>
      </div>
    </div>

    <div class="field-row">
      <div class="field">
        <label for="birth_date"><?= $t('Fødselsdato *', 'Date of birth *', 'تاریخ تولد *') ?></label>
        <input id="birth_date" name="birth_date" type="date"
               value="<?= htmlspecialchars($order['birth_date'] ?? '', ENT_QUOTES) ?>"
               max="<?= date('Y-m-d') ?>" required>
      </div>
      <input type="hidden" name="sex" value="X">
    </div>

    <div class="field">
      <?php $addressOptional = in_array($selPkg, ['ase227', 'veiledning15'], true); ?>
      <label for="address"><?= $addressOptional ? $t('Adresse (valgfritt)', 'Address (optional)', 'نشانی (اختیاری)') : $t('Adresse *', 'Address *', 'نشانی *') ?></label>
      <input id="address" name="address" type="text" autocomplete="street-address"
             value="<?= htmlspecialchars($order['address'] ?? '', ENT_QUOTES) ?>"
             placeholder="<?= $t('Gateadresse, postnummer, sted', 'Street, postal code, city', 'خیابان، کد پستی، شهر') ?>" <?= $addressOptional ? '' : 'required' ?>>
    </div>

    <div class="field">
      <?php $notesRequired = in_array($selPkg, ['partner', 'familie3'], true); ?>
      <label for="notes"><?php
        if ($selPkg === 'partner') echo $t('Partnerens navn og fødselsdato *', "Partner's name and date of birth *", 'نام و تاریخ تولد شریک *');
        elseif ($selPkg === 'familie3') echo $t('Person 2 og 3 – navn og fødselsdato *', 'People 2 and 3 – names and dates of birth *', 'نفرات ۲ و ۳ – نام و تاریخ تولد *');
        else echo $t('Tilleggsopplysninger (valgfritt)', 'Additional details (optional)', 'توضیحات اضافی (اختیاری)');
      ?></label>
      <textarea id="notes" name="notes" rows="4" <?= $notesRequired ? 'required' : '' ?> placeholder="<?= $t('Skriv det du vil Åse skal vite før analysen.', 'Anything you want Åse to know before the analysis.', 'هر نکته‌ای که می‌خواهید Åse پیش از تحلیل بداند.') ?>"><?= htmlspecialchars($order['notes'] ?? '', ENT_QUOTES) ?></textarea>
    </div>

    <div class="field-row">
      <div class="field">
        <label for="phone"><?= $t('Mobilnummer *', 'Mobile number *', 'شماره‌ی موبایل *') ?></label>
        <input id="phone" name="phone" type="tel" autocomplete="tel"
               value="<?= htmlspecialchars($order['phone'] ?? '', ENT_QUOTES) ?>"
               placeholder="<?= $t('+47 9XX XX XXX', '+47 9XX XX XXX', '+47 9XX XX XXX') ?>" required>
        <small><?= $t('Brukes for Vipps-betaling.', 'Used for Vipps payment.', 'برای پرداخت با Vipps استفاده می‌شود.') ?></small>
      </div>
      <div class="field">
        <label for="email"><?= $t('E-postadresse *', 'Email address *', 'نشانی ایمیل *') ?></label>
        <input id="email" name="email" type="email" autocomplete="email"
               value="<?= htmlspecialchars($order['email'] ?? '', ENT_QUOTES) ?>"
               placeholder="<?= $t('din@epost.no', 'you@example.com', 'you@example.com') ?>" required>
        <small><?= $t('Analysen sendes hit.', 'Analysis delivered here.', 'تحلیل به این نشانی ارسال می‌شود.') ?></small>
      </div>
    </div>

    <div class="form-actions">
      <a href="/bestill/?step=1" class="btn-ghost"><?= $back ?> <?= $t('Tilbake', 'Back', 'بازگشت') ?></a>
      <button type="submit" class="btn-primary">
        <?= $t('Gå til betaling →', 'Go to payment →', 'رفتن به پرداخت ←') ?>
      </button>
    </div>
  </form>
</section>

<?php elseif ($step === 3): ?>
<!-- ══ STEP 3 — Review + Pay ═════════════════════════════════════════════════ -->
<?php
$selPkg  = $order['package'] ?? '';
$pkgInfo = PACKAGES[$selPkg] ?? null;
[$pkgName, $pkgDesc] = package_label($selPkg, $lang);
?>
<section class="card order-card">
  <h1><?= $t('Gjennomgang og betaling', 'Review and payment', 'بازبینی و پرداخت') ?></h1>
  <?php error_list($errors); ?>

  <div class="review-grid">
    <div class="review-section">
      <h2><?= $t('Din pakke', 'Your package', 'بسته‌ی شما') ?></h2>
      <?php if ($pkgInfo): ?>
        <div class="review-pkg">
          <strong><?= htmlspecialchars($pkgName) ?></strong>
          <span class="review-price"><?= $pkgInfo['price'] ?> kr</span>
          <p><?= htmlspecialchars($pkgDesc) ?></p>
        </div>
      <?php endif; ?>
    </div>

    <div class="review-section">
      <h2><?= $t('Dine opplysninger', 'Your details', 'اطلاعات شما') ?></h2>
      <dl class="review-dl">
        <dt><?= $t('Fødselsnavn', 'Birth name', 'نام هنگام تولد') ?></dt>
        <dd><?= htmlspecialchars($order['birth_name'] ?? '') ?></dd>
        <dt><?= $t('Nåværende navn', 'Current name', 'نام فعلی') ?></dt>
        <dd><?= htmlspecialchars($order['current_name'] ?? '') ?></dd>
        <dt><?= $t('Fødselsdato', 'Date of birth', 'تاریخ تولد') ?></dt>
        <dd><?= htmlspecialchars($order['birth_date'] ?? '') ?></dd>
        <dt><?= $t('Telefon', 'Phone', 'تلفن') ?></dt>
        <dd><?= htmlspecialchars($order['phone'] ?? '') ?></dd>
        <dt><?= $t('E-post', 'Email', 'ایمیل') ?></dt>
        <dd><?= htmlspecialchars($order['email'] ?? '') ?></dd>
        <dt><?= $t('Adresse', 'Address', 'نشانی') ?></dt>
        <dd><?= htmlspecialchars($order['address'] ?? '') ?></dd>
        <?php if (!empty($order['notes'])): ?>
        <dt><?= $t('Tilleggsopplysninger', 'Additional details', 'توضیحات اضافی') ?></dt>
        <dd><?= nl2br(htmlspecialchars($order['notes'])) ?></dd>
        <?php endif; ?>
      </dl>
    </div>
  </div>

  <div class="total-row">
    <span><?= $t('Totalt å betale', 'Total to pay', 'مبلغ قابل پرداخت') ?></span>
    <strong><?= $pkgInfo['price'] ?? 0 ?> kr</strong>
  </div>

  <form method="post" action="/bestill/?step=3" class="pay-form">
    <input type="hidden" name="step" value="3">
    <input type="hidden" name="_csrf" value="<?= htmlspecialchars($csrf, ENT_QUOTES) ?>">

    <button type="submit" class="btn-vipps" aria-label="<?= $t('Betal med Vipps', 'Pay with Vipps', 'پرداخت با Vipps') ?>">
      <svg width="80" height="28" viewBox="0 0 80 28" aria-hidden="true" fill="none" xmlns="http://www.w3.org/2000/svg">
        <text x="4" y="21" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="white"><?= $t('Betal med', 'Pay with', 'پرداخت با') ?></text>
      </svg>
      <span class="vipps-logo" aria-label="Vipps">Vipps</span>
    </button>

    <p class="pay-note">
      <?= $t('Du sendes til Vipps for sikker betaling. Analysen leveres per e-post etter betaling er bekreftet.', 'You will be sent to Vipps for secure payment. Analysis delivered by email after payment confirmed.', 'برای پرداخت امن به Vipps هدایت می‌شوید. پس از تأیید پرداخت، تحلیل از طریق ایمیل ارسال می‌شود.') ?>
    </p>
  </form>

  <div class="review-edit-links">
    <a href="/bestill/?step=1"><?= $back ?> <?= $t('Endre pakke', 'Change package', 'تغییر بسته') ?></a>
    <a href="/bestill/?step=2"><?= $back ?> <?= $t('Endre opplysninger', 'Edit details', 'ویرایش اطلاعات') ?></a>
  </div>
</section>
<?php endif; ?>

<script>
// Reuse details already entered in ÅSE Edition (same domain / same browser).
try {
  var ase = JSON.parse(localStorage.getItem('numerologist.aseedition.v1') || '{}');
  var setIfEmpty = function(id, value) { var el=document.getElementById(id); if(el && !el.value && value) el.value=value; };
  setIfEmpty('birth_name', [ase.birthFirst, ase.birthMiddle, ase.birthLast].filter(Boolean).join(' '));
  setIfEmpty('current_name', ase.currentName || [ase.birthFirst, ase.birthMiddle, ase.birthLast].filter(Boolean).join(' '));
  setIfEmpty('birth_date', ase.birthDate);
  setIfEmpty('address', ase.address);
  setIfEmpty('phone', ase.phone);
  if (document.getElementById('notes') && !document.getElementById('notes').value && ase.partnerName) {
    document.getElementById('notes').value = 'Partner: ' + ase.partnerName + (ase.partnerDate ? ' · ' + ase.partnerDate : '');
  }
} catch (e) {}

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
