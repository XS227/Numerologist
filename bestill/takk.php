<?php

declare(strict_types=1);

require_once __DIR__ . '/../includes/config.php';
require_once __DIR__ . '/../includes/db.php';
require_once __DIR__ . '/../includes/vipps.php';
require_once __DIR__ . '/../includes/mail.php';
require_once __DIR__ . '/../includes/layout.php';

session_start();

$lang = handle_lang_switch();
$no   = ($lang === 'no');

$orderId = trim((string) ($_GET['orderId'] ?? ''));

// Validate format to prevent enumeration (orderId starts with NUM)
if (!preg_match('/^NUM\d{10}[A-F0-9]{6}$/i', $orderId)) {
    http_response_code(400);
    render_header($no ? 'Ugyldig lenke' : 'Invalid link', [
        'title'       => $no ? 'Ugyldig lenke' : 'Invalid link',
        'description' => '',
        'canonical'   => SITE_URL . '/bestill/takk.php',
        'lang'        => $lang,
        'noindex'     => true,
    ]);
    echo '<section class="card"><p>' . ($no ? 'Ugyldig bestillingslenke.' : 'Invalid order link.') . '</p></section>';
    render_footer();
    exit;
}

$order = get_order($orderId);

if ($order === null) {
    http_response_code(404);
    render_header($no ? 'Bestilling ikke funnet' : 'Order not found', [
        'title'       => $no ? 'Bestilling ikke funnet' : 'Order not found',
        'description' => '',
        'canonical'   => SITE_URL . '/bestill/',
        'lang'        => $lang,
        'noindex'     => true,
    ]);
    echo '<section class="card"><p>' .
         ($no ? 'Vi fant ikke bestillingen. Kontakt oss hvis du mener dette er feil.'
               : 'We could not find your order. Contact us if you believe this is an error.') .
         '</p></section>';
    render_footer();
    exit;
}

// Poll Vipps for status if still pending (user may land here before callback fires)
if ($order['payment_status'] === 'pending' && VIPPS_CLIENT_ID !== '') {
    try {
        $details     = Vipps::paymentDetails($orderId);
        $history     = $details['transactionLogHistory'] ?? [];
        $latestEntry = end($history) ?: [];
        $vStatus     = strtolower((string) ($latestEntry['operation'] ?? ''));

        $resolved = match(true) {
            in_array($vStatus, ['reserved', 'captured', 'sale'], true) => 'paid',
            in_array($vStatus, ['cancelled', 'void', 'failed', 'rejected'], true) => $vStatus,
            default => null,
        };

        if ($resolved !== null) {
            update_order_payment($orderId, $resolved);
            if ($resolved === 'paid') {
                // Reload and send confirmation if callback hasn't fired yet
                $order = get_order($orderId);
                if ($order !== null) {
                    send_order_confirmation($order);
                }
            }
            $order = get_order($orderId) ?? $order;
        }
    } catch (RuntimeException) {
        // Vipps unavailable — show pending state, callback will update later
    }
}

$paymentStatus = $order['payment_status'];
$isPaid        = ($paymentStatus === 'paid');
$isCancelled   = in_array($paymentStatus, ['cancelled', 'void'], true);
$isFailed      = in_array($paymentStatus, ['failed', 'rejected'], true);

render_header(
    $isPaid    ? ($no ? 'Bestilling bekreftet!' : 'Order confirmed!')
               : ($no ? 'Betalingsstatus' : 'Payment status'),
    [
        'title'       => $isPaid
            ? ($no ? 'Bestilling bekreftet!' : 'Order confirmed!')
            : ($no ? 'Betalingsstatus' : 'Payment status'),
        'description' => '',
        'canonical'   => SITE_URL . '/bestill/',
        'lang'        => $lang,
        'noindex'     => true,
    ]
);
?>
<link rel="stylesheet" href="/assets/bestill.css">

<section class="card order-card confirmation-card">
  <?php if ($isPaid): ?>
    <div class="confirm-icon confirm-icon--ok" aria-hidden="true">✓</div>
    <h1><?= $no ? 'Takk for din bestilling!' : 'Thank you for your order!' ?></h1>
    <p class="confirm-sub">
      <?= $no
          ? 'Betalingen er bekreftet. Vi sender deg en bekreftelse per e-post og starter analysen.'
          : 'Payment confirmed. We will send a confirmation by email and start your analysis.' ?>
    </p>

    <dl class="review-dl review-dl--confirm">
      <dt><?= $no ? 'Bestillingsnummer' : 'Order ID' ?></dt>
      <dd><?= htmlspecialchars($orderId) ?></dd>
      <dt><?= $no ? 'Pakke' : 'Package' ?></dt>
      <dd><?= htmlspecialchars($order['package']) ?></dd>
      <dt><?= $no ? 'Beløp' : 'Amount' ?></dt>
      <dd><?= number_format((int) $order['price_ore'] / 100, 0, ',', ' ') ?> kr</dd>
      <dt>E-post</dt>
      <dd><?= htmlspecialchars($order['email']) ?></dd>
      <dt><?= $no ? 'Forventet leveringstid' : 'Expected delivery' ?></dt>
      <dd><?= $no ? '5–7 virkedager' : '5–7 business days' ?></dd>
    </dl>

    <a href="/" class="btn-primary" style="display:inline-block;margin-top:1.5rem;">
      ← <?= $no ? 'Tilbake til forsiden' : 'Back to home' ?>
    </a>

  <?php elseif ($isCancelled): ?>
    <div class="confirm-icon confirm-icon--warn" aria-hidden="true">⚠</div>
    <h1><?= $no ? 'Betaling avbrutt' : 'Payment cancelled' ?></h1>
    <p>
      <?= $no
          ? 'Betalingen ble avbrutt. Ingen beløp er trukket. Du kan prøve igjen.'
          : 'The payment was cancelled. No amount was charged. You can try again.' ?>
    </p>
    <a href="/bestill/" class="btn-primary">
      <?= $no ? 'Prøv igjen' : 'Try again' ?>
    </a>

  <?php elseif ($isFailed): ?>
    <div class="confirm-icon confirm-icon--err" aria-hidden="true">✕</div>
    <h1><?= $no ? 'Betaling mislyktes' : 'Payment failed' ?></h1>
    <p>
      <?= $no
          ? 'Noe gikk galt med betalingen. Prøv igjen eller kontakt oss.'
          : 'Something went wrong with the payment. Please try again or contact us.' ?>
    </p>
    <div class="form-actions">
      <a href="/bestill/" class="btn-primary"><?= $no ? 'Prøv igjen' : 'Try again' ?></a>
      <a href="mailto:<?= MAIL_ADMIN ?>" class="btn-ghost"><?= $no ? 'Kontakt oss' : 'Contact us' ?></a>
    </div>

  <?php else: /* pending */ ?>
    <div class="confirm-icon confirm-icon--spin" aria-hidden="true">⏳</div>
    <h1><?= $no ? 'Betaling behandles…' : 'Processing payment…' ?></h1>
    <p>
      <?= $no
          ? 'Vi venter på bekreftelse fra Vipps. Siden oppdateres automatisk.'
          : 'Waiting for confirmation from Vipps. This page refreshes automatically.' ?>
    </p>
    <p>
      <?= $no ? 'Bestillingsnummer' : 'Order ID' ?>:
      <strong><?= htmlspecialchars($orderId) ?></strong>
    </p>
    <!-- Auto-refresh until Vipps callback fires -->
    <meta http-equiv="refresh" content="5;url=<?= SITE_URL ?>/bestill/takk.php?orderId=<?= rawurlencode($orderId) ?>">
  <?php endif; ?>
</section>

<?php render_footer(); ?>
