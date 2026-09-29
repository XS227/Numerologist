(() => {
  const root = document.querySelector('.n-story');
  if (!root) return;

  const media = matchMedia('(prefers-reduced-motion: reduce)');
  const chapters = [...root.querySelectorAll('[data-number-chapter]')];
  const figures = chapters.map(ch => ch.querySelector('.j-figure')).filter(Boolean);
  let scheduled = false;
  let pointerX = 0;
  let pointerY = 0;

  const clamp = (min, max, value) => Math.max(min, Math.min(max, value));

  function paint() {
    scheduled = false;
    if (media.matches || root.classList.contains('j-paused')) return;

    const vh = innerHeight || document.documentElement.clientHeight;
    const rect = root.getBoundingClientRect();
    const travel = Math.max(1, rect.height - vh);
    const amount = clamp(0, 1, (-rect.top) / travel);

    root.style.setProperty('--n-scroll', amount.toFixed(4));

    const turn = (-26 + amount * 52) + pointerX * 6;
    const tilt = Math.sin(amount * Math.PI * 2) * 8 + pointerY * -4;
    root.style.setProperty('--n-turn', turn.toFixed(2) + 'deg');
    root.style.setProperty('--n-tilt', tilt.toFixed(2) + 'deg');

    chapters.forEach(chapter => {
      const r = chapter.getBoundingClientRect();
      const centerDistance = (vh * .5) - (r.top + r.height * .5);
      const local = clamp(-1, 1, centerDistance / Math.max(1, r.height * .55));
      chapter.style.setProperty('--n-local', local.toFixed(4));
      chapter.classList.toggle('is-active', r.bottom > vh * .18 && r.top < vh * .82);

      const fig = chapter.querySelector('.j-figure');
      if (fig) {
        const isNear = Math.abs(r.top + r.height * .5 - vh * .5) < vh * .48;
        fig.classList.toggle('is-near', isNear);
      }
    });
  }

  function schedule() {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(paint);
    }
  }

  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule, {passive:true});

  if (matchMedia('(pointer:fine)').matches) {
    addEventListener('pointermove', event => {
      pointerX = (event.clientX / innerWidth - .5) * 2;
      pointerY = (event.clientY / innerHeight - .5) * 2;
      schedule();
    }, {passive:true});
  }

  media.addEventListener?.('change', schedule);
  schedule();
})();

(() => {
  const nav = document.querySelector('.n-editorial-tabs');
  if (!nav) return;

  const links = [...nav.querySelectorAll('a[href^="#"]')];
  const targets = links.map(link => {
    const id = link.getAttribute('href');
    const node = id ? document.querySelector(id) : null;
    return { link, node: node?.closest('section') || node };
  }).filter(item => item.node);

  const setActive = (link) => {
    links.forEach(item => {
      const active = item === link;
      item.classList.toggle('is-active', active);
      if (active) item.setAttribute('aria-current', 'location');
      else item.removeAttribute('aria-current');
    });
  };

  const updateProgress = () => {
    const article = document.querySelector('.n-story');
    if (!article) return;
    const rect = article.getBoundingClientRect();
    const travel = Math.max(1, rect.height - innerHeight);
    const progress = Math.max(0, Math.min(1, -rect.top / travel));
    nav.style.setProperty('--n-page-progress', progress.toFixed(4));
  };

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries
        .filter(entry => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      const match = targets.find(item => item.node === visible.target);
      if (match) {
        setActive(match.link);
        if (matchMedia('(max-width:760px)').matches) {
          nav.scrollTo({left: match.link.offsetLeft - nav.clientWidth / 2 + match.link.clientWidth / 2, behavior:'smooth'});
        }
      }
    }, {rootMargin:'-24% 0px -54% 0px', threshold:[0,.08,.18,.35,.55]});
    targets.forEach(item => observer.observe(item.node));
  }

  addEventListener('scroll', updateProgress, {passive:true});
  addEventListener('resize', updateProgress, {passive:true});
  updateProgress();
})();
