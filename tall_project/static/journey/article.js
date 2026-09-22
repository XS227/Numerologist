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
