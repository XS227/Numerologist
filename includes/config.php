<?php

declare(strict_types=1);

// Load .env into $_ENV (idempotent — won't overwrite already-set keys)
(static function (): void {
    $file = dirname(__DIR__) . '/.env';
    if (!is_file($file)) return;
    foreach (file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $line = trim($line);
        if ($line === '' || $line[0] === '#' || !str_contains($line, '=')) continue;
        [$k, $v] = explode('=', $line, 2);
        $k = trim($k);
        $v = trim($v);
        if (!array_key_exists($k, $_ENV)) {
            $_ENV[$k] = $v;
            putenv("{$k}={$v}");
        }
    }
})();

function env(string $key, string $default = ''): string
{
    $val = $_ENV[$key] ?? getenv($key);
    return ($val !== false && $val !== '') ? (string) $val : $default;
}

// ── Vipps eCommerce API v2 ────────────────────────────────────────────────────
define('VIPPS_CLIENT_ID',        env('VIPPS_CLIENT_ID'));
define('VIPPS_CLIENT_SECRET',    env('VIPPS_CLIENT_SECRET'));
define('VIPPS_SUBSCRIPTION_KEY', env('VIPPS_SUBSCRIPTION_KEY'));
define('VIPPS_MSN',              env('VIPPS_MSN'));          // Merchant Serial Number
define('VIPPS_TEST_MODE',        env('VIPPS_TEST_MODE', 'true') === 'true');
define('VIPPS_BASE_URL',         VIPPS_TEST_MODE
    ? 'https://apitest.vipps.no'
    : 'https://api.vipps.no');

// ── Mail ──────────────────────────────────────────────────────────────────────
define('MAIL_FROM',      env('MAIL_FROM',      'noreply@numerologist.setai.no'));
define('MAIL_FROM_NAME', env('MAIL_FROM_NAME', 'Numerologist – Åse Steinsland'));
define('MAIL_ADMIN',     env('MAIL_ADMIN',     'khabat.setaei@gmail.com'));

// ── Order database ────────────────────────────────────────────────────────────
define('DB_PATH', dirname(__DIR__) . '/data/orders.db');
