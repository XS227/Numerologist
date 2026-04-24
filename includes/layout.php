<?php

declare(strict_types=1);

function render_header(string $title): void
{
    echo '<!doctype html><html lang="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">';
    echo '<title>' . htmlspecialchars($title) . ' | Numerologist</title>';
    echo '<link rel="stylesheet" href="/assets/style.css">';
    echo '</head><body><header><div class="wrap"><a class="brand" href="/index.php">Numerologist</a><nav>';
    echo '<a href="/index.php">Hjem</a><a href="/page.php?slug=discover-numerology">Numerologi</a><a href="/page.php?slug=resources">Ressurser</a><a href="/page.php?slug=legal">Legal</a>';
    echo '</nav></div></header><main class="wrap">';
}

function render_footer(): void
{
    echo '</main><footer><div class="wrap">Klar for delt hosting (kun PHP-filer)</div></footer></body></html>';
}
