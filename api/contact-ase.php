<?php

declare(strict_types=1);

require_once __DIR__ . '/../includes/mail.php';

const REDIRECT_BASE = '/about-the-firm/';
const CONTACT_TO = 'epost@numerologen.no';

function redirect(string $status): void
{
    header('Location: ' . REDIRECT_BASE . '?contact=' . $status);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ' . REDIRECT_BASE);
    exit;
}

// Honeypot: bots that fill this hidden field get a fake "success" with no email sent.
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    redirect('ok');
}

$name    = trim((string) ($_POST['name'] ?? ''));
$email   = trim((string) ($_POST['email'] ?? ''));
$phone   = trim((string) ($_POST['phone'] ?? ''));
$message = trim((string) ($_POST['message'] ?? ''));

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    redirect('error');
}

$subject = 'Ny henvendelse fra numerologist.setai.no';
$body = "Navn: {$name}\n"
    . "E-post: {$email}\n"
    . "Telefon: " . ($phone !== '' ? $phone : '(ikke oppgitt)') . "\n\n"
    . "Melding:\n{$message}\n";

$headers = build_mail_headers();
mail_send(CONTACT_TO, $subject, $body, $headers);

redirect('ok');
