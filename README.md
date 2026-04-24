# Numerologist (PHP-utgave)

Denne versjonen er gjort om til **rene PHP-sider** slik at du kan laste opp prosjektet på et vanlig webhotell (ikke VPS), uten å installere Python, Django eller andre tjenester på serveren.

## Hva som trengs på serveren
- PHP 8.x (typisk allerede aktivert hos webhotell)
- Apache/Nginx med vanlig PHP-støtte
- FTP/SFTP for opplasting

## Struktur
- `index.php` — forside + numerologi-kalkulator
- `page.php` — statiske infosider via `?slug=`
- `number.php` — enkel tolkning av tall via `?number=`
- `includes/data.php` — logikk og sideinnhold
- `includes/layout.php` — header/footer
- `assets/style.css` — stilark
- `.htaccess` — valgfri rewrite for penere URL-er

## Lokal test
```bash
php -S 127.0.0.1:8080
```
Åpne deretter `http://127.0.0.1:8080`.

## Opplasting til webhotell
1. Last opp alle filene i prosjektroten til `public_html` (eller tilsvarende).
2. Pass på at `index.php` ligger i webroot.
3. Besøk domenet ditt — siden skal fungere uten ekstra installasjon.

## Notat
Denne varianten er bevisst enkel og driftssikker for delt hosting.
