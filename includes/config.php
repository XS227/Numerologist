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

// ── Vipps payment API ─────────────────────────────────────────────────────────
// Production secrets stay server-side. If this app has no dedicated Vipps keys,
// it may read an explicitly configured local shared config file. Only the Vipps
// constants below are extracted; the source file itself is never exposed.
function shared_vipps_config(): array
{
    $file = env('VIPPS_SHARED_CONFIG');
    if ($file === '' || !is_readable($file)) return [];

    $source = (string) file_get_contents($file);
    $result = [];
    foreach (['VIPPS_ENV', 'VIPPS_CLIENT_ID', 'VIPPS_CLIENT_SECRET', 'VIPPS_SUBSCRIPTION_KEY', 'VIPPS_MSN'] as $key) {
        $pattern = "/define\\(\\s*['\\\"]" . preg_quote($key, '/') . "['\\\"]\\s*,\\s*['\\\"]([^'\\\"]*)['\\\"]\\s*\\)/";
        if (preg_match($pattern, $source, $match) === 1) {
            $result[$key] = $match[1];
        }
    }
    return $result;
}

$sharedVipps = shared_vipps_config();
$useSharedVipps = env('VIPPS_CLIENT_ID') === '' && !empty($sharedVipps['VIPPS_CLIENT_ID']);

define('VIPPS_CLIENT_ID',        $useSharedVipps ? ($sharedVipps['VIPPS_CLIENT_ID'] ?? '') : env('VIPPS_CLIENT_ID'));
define('VIPPS_CLIENT_SECRET',    $useSharedVipps ? ($sharedVipps['VIPPS_CLIENT_SECRET'] ?? '') : env('VIPPS_CLIENT_SECRET'));
define('VIPPS_SUBSCRIPTION_KEY', $useSharedVipps ? ($sharedVipps['VIPPS_SUBSCRIPTION_KEY'] ?? '') : env('VIPPS_SUBSCRIPTION_KEY'));
define('VIPPS_MSN',              $useSharedVipps ? ($sharedVipps['VIPPS_MSN'] ?? '') : env('VIPPS_MSN'));

$vippsTestMode = $useSharedVipps
    ? strtolower((string) ($sharedVipps['VIPPS_ENV'] ?? 'test')) !== 'prod'
    : env('VIPPS_TEST_MODE', 'true') === 'true';
define('VIPPS_TEST_MODE', $vippsTestMode);
define('VIPPS_BASE_URL', VIPPS_TEST_MODE ? 'https://apitest.vipps.no' : 'https://api.vipps.no');

// ── Lite calculator soft-launch gate ──────────────────────────────────────────
// 3-digit code visitors must enter to reveal their result while the homepage
// calculator is tried out with trusted testers only. Mirrors
// CALCULATOR_ACCESS_CODE on the Django side (same .env key, same value).
define('CALCULATOR_ACCESS_CODE', env('CALCULATOR_ACCESS_CODE', '227'));

// ── Mail ──────────────────────────────────────────────────────────────────────
define('MAIL_FROM',      env('MAIL_FROM',      'noreply@numerologist.setai.no'));
define('MAIL_FROM_NAME', env('MAIL_FROM_NAME', 'Numerologist – Åse Steinsland'));
define('MAIL_ADMIN',     env('MAIL_ADMIN',     'khabat.setaei@gmail.com'));

// ── Order database ────────────────────────────────────────────────────────────
define('DB_PATH', dirname(__DIR__) . '/data/orders.db');
