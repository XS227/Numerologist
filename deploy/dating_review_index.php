<?php
declare(strict_types=1);
// Only this /dating/ preview uses this session; existing site accounts are untouched.
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: private, no-store, max-age=0');
header('X-Robots-Tag: noindex, nofollow, noarchive');
header('Referrer-Policy: same-origin');
header("Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; script-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'self'; form-action 'self'");
header('X-Content-Type-Options: nosniff');
if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 8192) {
    http_response_code(413); exit('Request too large.');
}
session_name('setaei_dating_review');
session_set_cookie_params(['path'=>'/dating', 'secure'=>true, 'httponly'=>true, 'samesite'=>'Lax']);
session_start();
if (!isset($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));
$csrf = $_SESSION['csrf'];
$post = ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST';
if (!in_array($_SERVER['REQUEST_METHOD'] ?? 'GET', ['GET','HEAD','POST'], true)) {
    http_response_code(405); header('Allow: GET, HEAD, POST'); exit;
}
if ($post && (!is_string($_POST['csrfmiddlewaretoken'] ?? null) ||
              !hash_equals($csrf, $_POST['csrfmiddlewaretoken']))) {
    http_response_code(403); exit('Last inn siden på nytt og prøv igjen.');
}
$lang = is_string($_GET['lang'] ?? null) ? $_GET['lang'] : 'no';
if (!in_array($lang, ['no','en','fa'], true)) $lang = 'no';
$error = '';
if (empty($_SESSION['preview_allowed'])) {
    if ($post && isset($_POST['preview_code'])) {
        $now = time();
        if (($now - (int)($_SESSION['gate_since'] ?? 0)) > 60) {
            $_SESSION['gate_since'] = $now; $_SESSION['gate_attempts'] = 0;
        }
        $_SESSION['gate_attempts'] = (int)($_SESSION['gate_attempts'] ?? 0) + 1;
        if ($_SESSION['gate_attempts'] > 10) {
            http_response_code(429); $error = 'Vent ett minutt og prøv igjen.';
        } elseif (is_string($_POST['preview_code']) && hash_equals('227', trim($_POST['preview_code']))) {
            $_SESSION['preview_allowed'] = true;
            session_write_close();
            header('Location: /dating/?lang=' . $lang, true, 303);
            exit;
        } else $error = 'Koden er ikke riktig.';
    }
    $token = htmlspecialchars($csrf, ENT_QUOTES, 'UTF-8');
    session_write_close();
    echo '<!doctype html><html lang="no"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">';
    echo '<meta name="robots" content="noindex,nofollow"><title>Early preview · Numerologist Dating</title>';
    echo '<style>html{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#14121c;color:#f2ede6;font:16px/1.6 system-ui;min-height:100svh;display:grid;place-items:center;padding:24px}main{max-width:420px;width:100%}.brand{color:#f8a77b;letter-spacing:3px;font-size:11px}h1{font:44px/1.2 Georgia;margin:25px 0}p,label{color:#b0a8b9}label{display:block;font-size:13px;margin-bottom:8px}input{width:100%;padding:16px;border:1px solid #544356;border-radius:12px;background:#211c2a;color:#fff;font:22px system-ui;letter-spacing:10px}button{width:100%;padding:15px;background:#f8a77b;border:0;border-radius:100px;color:#241712;font-weight:600;margin-top:20px;cursor:pointer}input:focus,button:focus-visible{outline:3px solid #b9a2e5;outline-offset:3px}.error{color:#ffc1ad}</style>';
    echo '<main><span class="brand">NUMEROLOGIST × SETAEI</span><h1>Early preview</h1><p>Et datingeksperiment med tall, forbindelser og felles rytme.</p><form method="post"><input type="hidden" name="csrfmiddlewaretoken" value="' . $token . '"><label for="code">Early preview code</label><input id="code" name="preview_code" inputmode="numeric" pattern="[0-9]{3}" maxlength="3" required autocomplete="off" autofocus><button type="submit">Åpne forhåndsvisningen ↗</button></form>';
    if ($error !== '') echo '<p class="error" role="alert">' . htmlspecialchars($error) . '</p>';
    echo '</main></html>'; exit;
}
$mode = is_string($_POST['mode'] ?? null) ? $_POST['mode'] :
        (is_string($_GET['mode'] ?? null) ? $_GET['mode'] : 'self');
$mode = $mode === 'pair' ? 'pair' : 'self';
$view = is_string($_GET['view'] ?? null) ? $_GET['view'] : '';
$view = in_array($view, ['profile','matches'], true) ? $view : $mode;
if ($post) {
    $now = time();
    if (($now - (int)($_SESSION['calc_since'] ?? 0)) > 60) {
        $_SESSION['calc_since'] = $now; $_SESSION['calc_count'] = 0;
    }
    $_SESSION['calc_count'] = (int)($_SESSION['calc_count'] ?? 0) + 1;
    if ($_SESSION['calc_count'] > 30) {
        session_write_close(); http_response_code(429); exit('Vent ett minutt og prøv igjen.');
    }
}
session_write_close();
if ($post) {
    $fields = [];
    foreach (['you-full_name','you-birth_date','other-full_name','other-birth_date'] as $key) {
        if (isset($_POST[$key]) && is_string($_POST[$key])) $fields[$key] = substr($_POST[$key], 0, 600);
    }
    $payload = json_encode(['lang'=>$lang,'mode'=>$mode,'fields'=>$fields], JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    $command = ['/usr/bin/timeout','15s','/var/www/numerologist/.venv/bin/python',
                '/opt/numerologist-dating-review/deploy/dating_review.py'];
    $process = proc_open($command, [0=>['pipe','r'],1=>['pipe','w'],2=>['file','/dev/null','a']], $pipes,
                         '/opt/numerologist-dating-review', null, ['bypass_shell'=>true]);
    if (!is_resource($process)) { http_response_code(503); exit('Beregningen er midlertidig utilgjengelig.'); }
    fwrite($pipes[0], $payload); fclose($pipes[0]);
    $html = stream_get_contents($pipes[1], 1000000); fclose($pipes[1]);
    if (proc_close($process) !== 0 || !is_string($html) || !str_contains($html, '<!doctype html>')) {
        http_response_code(503); exit('Beregningen er midlertidig utilgjengelig.');
    }
} else {
    $html = file_get_contents('/var/cache/numerologist-dating-review/' . $lang . '-' . $view . '.html');
    if ($html === false) { http_response_code(503); exit('Forhåndsvisningen er midlertidig utilgjengelig.'); }
}
echo preg_replace('/name="csrfmiddlewaretoken" value="[^"]*"/',
    'name="csrfmiddlewaretoken" value="' . htmlspecialchars($csrf, ENT_QUOTES, 'UTF-8') . '"', $html);
