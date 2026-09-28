(() => {
  const article = document.querySelector('.j-article .article-detail');
  if (!article) return;
  const chapters = [...article.querySelectorAll('.chapter')];
  const links = [...document.querySelectorAll('.article-toc a, .mb-toc a')];

  // Reading progress bar across the top.
  const bar = document.createElement('div');
  bar.className = 'ja-progress';
  bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  let scheduled = false;
  function paint() {
    scheduled = false;
    const rect = article.getBoundingClientRect();
    const total = rect.height - innerHeight;
    const amount = total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 1;
    bar.style.transform = `scaleX(${amount})`;
  }
  addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(paint); } }, {passive: true});
  addEventListener('resize', paint);
  paint();

  if (!('IntersectionObserver' in window)) return;

  // Highlight the chapter being read and keep its chip in view.
  const byId = new Map(links.map(a => [decodeURIComponent(a.hash.slice(1)), a]));
  let current;
  const spy = new IntersectionObserver(entries => entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const link = byId.get(entry.target.id);
    if (!link || link === current) return;
    if (current) current.classList.remove('is-active');
    link.classList.add('is-active');
    current = link;
    const nav = link.parentElement;
    nav.scrollTo({left: link.offsetLeft - nav.clientWidth / 2 + link.clientWidth / 2, behavior: 'smooth'});
  }), {rootMargin: '-45% 0px -50% 0px'});
  chapters.forEach(c => spy.observe(c));

  // Reveal text blocks, visuals and quotes as they scroll in.
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const blocks = chapters.flatMap(c => [...c.children].filter(el => !el.classList.contains('chapter-head')));
  const reveal = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('is-in'); reveal.unobserve(entry.target); }
  }), {threshold: .08, rootMargin: '0px 0px -40px 0px'});
  blocks.forEach(el => { el.classList.add('ja-reveal'); reveal.observe(el); });
  document.documentElement.classList.add('ja-motion');
})();

// Learning-journey reveals + interactive compatibility lab.
(() => {
  const learning = document.querySelector('.learning-journey');
  if (!learning) return;

  const reduceMaster = value => ({11:2, 22:4, 33:6}[Number(value)] || Number(value));

  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('ja-motion');
    const reveal = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-in');
      reveal.unobserve(entry.target);
    }), {threshold:.12, rootMargin:'0px 0px -50px 0px'});
    learning.querySelectorAll('.lj-reveal').forEach(el => reveal.observe(el));
  } else {
    learning.querySelectorAll('.lj-reveal').forEach(el => el.classList.add('is-in'));
  }

  const lab = learning.querySelector('[data-compat-lab]');
  if (!lab) return;

  const context = lab.querySelector('[data-compat-context]');
  const me = lab.querySelector('[data-compat-me]');
  const other = lab.querySelector('[data-compat-other]');
  const grade = lab.querySelector('[data-compat-grade]');
  const title = lab.querySelector('[data-compat-title]');
  const copy = lab.querySelector('[data-compat-text]');
  const tables = [...learning.querySelectorAll('[data-compat-table]')];

  const meanings = {
    'A': ['Utmerket flyt', 'I Åses kart er dette en svært harmonisk kombinasjon. Bruk styrken til å bygge tillit, men ikke ta god kjemi for gitt.'],
    'B': ['Bra dynamikk', 'Kartet viser et godt utgangspunkt. Forskjellene kan være nyttige når begge gir hverandre rom.'],
    'C': ['Middels / lærende', 'Denne kombinasjonen krever mer bevisst kommunikasjon. Se særlig etter ulike behov, tempo eller prioriteringer.'],
    'D': ['Krevende dynamikk', 'Åses kart markerer mer friksjon her. Det betyr ikke at relasjonen er dømt, men at tydelighet og respekt blir ekstra viktig.'],
    'A/D': ['Sterk polaritet', 'Denne kombinasjonen kan oppleves svært god eller svært krevende. Intensiteten gjør grenser, timing og kommunikasjon viktige.']
  };

  function update() {
    const r = reduceMaster(me.value);
    const c = reduceMaster(other.value);
    const kind = context.value;
    let match = null;
    tables.forEach(table => {
      table.querySelectorAll('td').forEach(td => td.classList.remove('is-axis','is-match'));
      if (table.dataset.compatTable !== kind) return;
      table.querySelectorAll(`td[data-r="${r}"],td[data-c="${c}"]`).forEach(td => td.classList.add('is-axis'));
      match = table.querySelector(`td[data-r="${r}"][data-c="${c}"]`);
      if (match) match.classList.add('is-match');
    });
    const key = match ? match.textContent.trim() : 'B';
    const meaning = meanings[key] || meanings.B;
    grade.textContent = key;
    title.textContent = meaning[0];
    copy.textContent = `Grunntall ${r} × ${c}: ${meaning[1]}`;
    if (match) match.scrollIntoView({block:'nearest', inline:'center', behavior:'smooth'});
  }

  [context, me, other].forEach(el => el.addEventListener('change', update));
  other.value = '2';
  update();
})();

