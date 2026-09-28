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