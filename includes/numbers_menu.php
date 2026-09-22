<?php
// Numbers quick-menu in the top nav: an icon that opens every core number
// (1–9 + master numbers) with its keyword. Pure <details>, so it works
// without JS; the small script only closes it on outside click / Escape.
// Django twin: tall_project/templates/_numbers_menu.html — keep in sync.
function render_numbers_menu(bool $no): string
{
    $core = $no
        ? ['Initiativ', 'Samarbeid', 'Uttrykk', 'Struktur', 'Frihet', 'Omsorg', 'Fordypning', 'Realisering', 'Fullføring']
        : ['Initiative', 'Cooperation', 'Expression', 'Structure', 'Freedom', 'Care', 'Reflection', 'Realisation', 'Completion'];
    $masters = $no
        ? [11 => 'Inspirasjon', 22 => 'Byggmester', 33 => 'Mesterlærer']
        : [11 => 'Inspiration', 22 => 'Builder', 33 => 'Teacher'];
    $cells = '';
    foreach ($core as $i => $word) {
        $n = $i + 1;
        $cells .= "<a href=\"/numbers/{$n}/\"><b>{$n}</b><span>{$word}</span></a>";
    }
    $masterCells = '';
    foreach ($masters as $n => $word) {
        $masterCells .= "<a href=\"/numbers/{$n}/\"><b>{$n}</b><span>{$word}</span></a>";
    }
    $aria   = $no ? 'Tallene – velg et tall' : 'The numbers – pick one';
    $label  = $no ? 'Tall' : 'Numbers';
    $title  = $no ? 'Velg et tall og les mer' : 'Pick a number to read more';
    $mTitle = $no ? 'Mestertall' : 'Master numbers';
    $all    = $no ? 'Se alle tallene samlet' : 'See all the numbers together';

    return <<<HTML
<details class="l-numbers">
  <summary aria-label="{$aria}">
    <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><g fill="currentColor"><circle cx="5" cy="5" r="2"/><circle cx="12" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="12" cy="19" r="2"/><circle cx="19" cy="19" r="2"/></g></svg>
    <span class="l-numbers__label">{$label}</span>
  </summary>
  <div class="l-numbers__panel">
    <p class="l-numbers__title">{$title}</p>
    <div class="l-numbers__grid">{$cells}</div>
    <p class="l-numbers__title">{$mTitle}</p>
    <div class="l-numbers__grid l-numbers__grid--masters">{$masterCells}</div>
    <a class="l-numbers__all" href="/general-interpretation/">{$all} →</a>
  </div>
</details>
<script>
(function () {
  var menu = document.currentScript.previousElementSibling;
  document.addEventListener('click', function (e) { if (menu.open && !menu.contains(e.target)) menu.open = false; });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.open) { menu.open = false; menu.querySelector('summary').focus(); } });
})();
</script>
HTML;
}
