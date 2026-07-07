<?php

declare(strict_types=1);

require_once __DIR__ . '/config.php';

/**
 * Send confirmation email to the customer and a notification to admin.
 */
function send_order_confirmation(array $order): void
{
    $pkgName  = htmlspecialchars_decode($order['package']);
    $priceKr  = number_format((int) $order['price_ore'] / 100, 0, ',', ' ') . ' kr';
    $name     = $order['current_name'];
    $id       = $order['id'];
    $birthDate = $order['birth_date'];
    $email    = $order['email'];

    // ── Customer email ────────────────────────────────────────────────────────
    $subject = "Bestillingsbekreftelse – {$pkgName} | Numerologist";

    $body = <<<TEXT
Hei {$name},

Takk for din bestilling hos Numerologist – vi ser frem til å arbeide med kartet ditt!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BESTILLINGSDETALJER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bestillingsnummer : {$id}
Pakke             : {$pkgName}
Beløp             : {$priceKr}
Status            : Betaling mottatt ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hva skjer nå?
Vi starter arbeidet med din numerologianalyse og sender deg
resultatet per e-post innen 5–7 virkedager.

Har du spørsmål? Svar på denne e-posten, så hjelper vi deg.

Med vennlig hilsen,
Åse Steinsland
Numerologist.setai.no
TEXT;

    $headers = build_mail_headers();
    mail_send($email, $subject, $body, $headers);

    // ── Admin notification ────────────────────────────────────────────────────
    $adminSubject = "Ny bestilling [{$id}] – {$pkgName}";
    $adminBody    = <<<TEXT
Ny bestilling mottatt!

ID           : {$id}
Pakke        : {$pkgName}
Pris         : {$priceKr}
Nåværende navn : {$name}
Fødselsnavn  : {$order['birth_name']}
Fødselsdato  : {$birthDate}
Kjønn        : {$order['sex']}
Telefon      : {$order['phone']}
E-post       : {$email}
Adresse      : {$order['address']}

Logg inn for å se alle bestillinger:
https://numerologist.setai.no/admin/
TEXT;

    mail_send(MAIL_ADMIN, $adminSubject, $adminBody, $headers);
}

function build_mail_headers(): string
{
    return implode("\r\n", [
        'From: ' . MAIL_FROM_NAME . ' <' . MAIL_FROM . '>',
        'Reply-To: ' . MAIL_ADMIN,
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
        'X-Mailer: PHP/' . PHP_VERSION,
    ]);
}

function mail_send(string $to, string $subject, string $body, string $headers): void
{
    // Encode subject for UTF-8
    $encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
    @mail($to, $encodedSubject, $body, $headers);
}
