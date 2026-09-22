<?php

declare(strict_types=1);

require_once __DIR__ . '/seo.php';

/**
 * Renders the full <html> opening, <head>, and <body> header.
 *
 * @param string $pageTitle  Plain page title (no site suffix).
 * @param array  $seo        SEO config forwarded to seo_head(). Supported keys:
 *                           description, canonical, lang, alt_no, alt_en,
 *                           og_type, og_image, schema, breadcrumbs, noindex.
 */
function render_header(string $pageTitle, array $seo = []): void
{
    $lang = $seo['lang'] ?? current_lang();

    // Sensible canonical default (slug-based clean URL via Django)
    $seo['title']       ??= $pageTitle;
    $seo['lang']        ??= $lang;
    $seo['description'] ??= '';
    $seo['canonical']   ??= SITE_URL . '/';

    $no       = ($lang === 'no');
    $htmlLang = htmlspecialchars($lang, ENT_QUOTES, 'UTF-8');
    $navLabel = htmlspecialchars($no ? 'Navigasjon' : 'Navigation', ENT_QUOTES, 'UTF-8');

    echo "<!doctype html>\n";
    echo "<html lang=\"{$htmlLang}\">\n";
    echo "<head>\n";
    echo "  <meta charset=\"utf-8\">\n";
    echo "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n";
    seo_head($seo);
    echo "  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n";
    echo "  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n";
    echo "  <link rel=\"stylesheet\" href=\"/assets/fibonacci.css\">\n";
    echo "  <link rel=\"stylesheet\" href=\"/assets/style.css\">\n";
    echo "</head>\n";
    echo "<body>\n";

    $home      = htmlspecialchars(SITE_URL . '/', ENT_QUOTES, 'UTF-8');
    $langNoUrl = htmlspecialchars($seo['alt_no'] ?? $seo['canonical'], ENT_QUOTES, 'UTF-8');
    $langEnUrl = htmlspecialchars($seo['alt_en'] ?? $seo['canonical'], ENT_QUOTES, 'UTF-8');
    $activeNo  = $no  ? ' class="lang-active"' : '';
    $activeEn  = !$no ? ' class="lang-active"' : '';
    $noLabel   = $no  ? 'Hjem'      : 'Home';
    $aboutLabel = $no ? 'Om numerologi' : 'About numerology';
    $srvLabel  = $no  ? 'Tjenester' : 'Services';
    $artLabel  = $no  ? 'Artikler'  : 'Articles';
    $contactLabel = $no ? 'Kontakt' : 'Contact';

    echo <<<HTML
<nav class="l-nav" aria-label="{$navLabel}">
  <div class="l-wrap l-nav-inner">
    <a class="l-brand" href="{$home}">Numero<em>logist</em></a>
    <ul class="l-nav-links" id="lNavLinks">
      <li><a href="{$home}">{$noLabel}</a></li>
      <li><a href="/discover-numerology/">{$aboutLabel}</a></li>
      <li><a href="/#tjenester">{$srvLabel}</a></li>
      <li><a href="/articles/">{$artLabel}</a></li>
      <li><a href="/contact-qa/">{$contactLabel}</a></li>
    </ul>
    <div class="l-nav-right">
      <div class="l-lang" aria-label="Velg språk / Select language">
        <a href="{$langNoUrl}?lang=no" hreflang="no"{$activeNo}>🇳🇴 NO</a>
        <a href="{$langEnUrl}?lang=en" hreflang="en"{$activeEn}>🇬🇧 EN</a>
      </div>
      <button class="l-burger" id="lBurger" aria-expanded="false" aria-controls="lNavLinks"
              aria-label="Åpne meny">☰</button>
    </div>
  </div>
</nav>
<main class="l-main l-wrap">
HTML;
}

function render_footer(): void
{
    $year  = date('Y');
    $no    = (current_lang() === 'no');
    $copy  = htmlspecialchars("© {$year} Åse Steinsland · Numerologist", ENT_QUOTES, 'UTF-8');
    // Where numbers and technology meet: Åse's Pythagorean method, computed in
    // Python. The studio's ethos — right calculation, right technology.
    $ethos = htmlspecialchars($no
        ? 'Der tall og teknologi jobber sammen — den pytagoreiske metoden, beregnet i Python. Riktig beregning, riktig teknologi.'
        : 'Where numbers and technology work together — the Pythagorean method, computed in Python. Right calculation, right technology.',
        ENT_QUOTES, 'UTF-8');
    $tagline = htmlspecialchars($no
        ? 'Norges fremste numerolog, basert i Oslo. Vi hjelper deg å forstå deg selv gjennom tallenes visdom.'
        : "Norway's leading numerologist, based in Oslo. Helping you understand yourself through the wisdom of numbers.",
        ENT_QUOTES, 'UTF-8');
    $h1 = $no ? 'Utforsk' : 'Explore';
    $h2 = $no ? 'Om oss' : 'About us';
    $l1 = $no
        ? [['Kalkulatorer', '/calculators/'], ['Om numerologi', '/discover-numerology/'], ['Artikler', '/articles/']]
        : [['Calculators', '/calculators/'], ['About numerology', '/discover-numerology/'], ['Articles', '/articles/']];
    $l2 = $no
        ? [['Møt Åse', '/about-the-firm/'], ['Veiledning', '/guidance-support/'], ['Personvern', '/privacy-policy/']]
        : [['Meet Åse', '/about-the-firm/'], ['Guidance', '/guidance-support/'], ['Privacy policy', '/privacy-policy/']];

    $l1Html = '';
    foreach ($l1 as [$label, $href]) {
        $l1Html .= '<li><a href="' . htmlspecialchars($href) . '">' . htmlspecialchars($label) . "</a></li>\n";
    }
    $l2Html = '';
    foreach ($l2 as [$label, $href]) {
        $l2Html .= '<li><a href="' . htmlspecialchars($href) . '">' . htmlspecialchars($label) . "</a></li>\n";
    }

    echo <<<HTML
</main>
<footer class="l-footer">
  <div class="l-wrap">
    <div class="l-footer-grid">
      <div>
        <a href="/" class="l-footer-brand">Numero<em>logist</em></a>
        <p class="l-footer-tagline">{$tagline}</p>
      </div>
      <div class="l-footer-col">
        <h4>{$h1}</h4>
        <ul>
          {$l1Html}
        </ul>
      </div>
      <div class="l-footer-col">
        <h4>{$h2}</h4>
        <ul>
          {$l2Html}
        </ul>
      </div>
    </div>
    <div class="l-footer-bottom">
      <span>{$copy}<br><small class="footer-ethos">{$ethos}</small></span>
      <div class="l-footer-langs">
        <a href="?lang=no">🇳🇴 Norsk</a>
        <a href="?lang=en">🇬🇧 English</a>
      </div>
    </div>
  </div>
</footer>
<script>
(function(){
  var b = document.getElementById('lBurger');
  var n = document.getElementById('lNavLinks');
  if (b && n) {
    b.addEventListener('click', function(){
      var o = n.classList.toggle('is-open');
      b.setAttribute('aria-expanded', String(o));
      b.textContent = o ? '✕' : '☰';
    });
  }
})();
</script>
</body>
</html>
HTML;
}
