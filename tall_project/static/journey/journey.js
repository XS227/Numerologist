(() => {
  const root = document.querySelector('.j-story');
  if (!root) return;
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  const toggle = root.querySelector('.j-motion');
  const pictures = [...root.querySelectorAll('.j-parallax')];
  const chapters = [...root.querySelectorAll('[data-chapter]')];
  const links = [...root.querySelectorAll('.j-chapter-nav a')];
  const progress = root.querySelector('.j-progress');
  let paused = media.matches, scheduled = false;
  const reveals = [...root.querySelectorAll('.j-reveal')];
  let observer;
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) {entry.target.classList.remove('j-waiting');observer.unobserve(entry.target);}
    }), {threshold: .08});
    reveals.forEach(el => {el.classList.add('j-waiting');observer.observe(el);});
  }
  root.classList.add('j-animate');
  function paint() {
    scheduled = false;
    const vh = innerHeight;
    if (!paused) pictures.forEach(img => {
      const rect = img.parentElement.getBoundingClientRect();
      if (rect.bottom > -100 && rect.top < vh + 100) {
        const max = rect.height * .09;
        const shift = Math.max(-max, Math.min(max, (vh / 2 - rect.top - rect.height / 2) * Number(img.dataset.speed)));
        img.style.transform = `translate3d(0,${shift}px,0)`;
      }
    });
    const top = root.getBoundingClientRect().top + scrollY;
    const amount = Math.max(0,Math.min(1,(scrollY-top) / Math.max(1,root.offsetHeight-vh)));
    progress.style.transform = `scaleX(${amount})`;
    let current = chapters[0];
    for (const chapter of chapters) if (chapter.getBoundingClientRect().top < vh * .48) current = chapter;
    links.forEach(link => {
      if (link.hash === `#${current.id}`) link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    });
  }
  function schedule() {if (!scheduled) {scheduled = true;requestAnimationFrame(paint);}}
  function setMotion(value) {
    paused = value;root.classList.toggle('j-paused',paused);
    toggle.setAttribute('aria-pressed',String(paused));
    toggle.textContent = paused ? toggle.dataset.resume : toggle.dataset.pause;
    schedule();
  }
  toggle.addEventListener('click',()=>setMotion(!paused));
  media.addEventListener('change',event=>setMotion(event.matches));
  root.querySelectorAll('a[href^="#"]').forEach(link=>link.addEventListener('click',event=>{
    const target = document.getElementById(link.hash.slice(1));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({behavior:paused?'instant':'smooth',block:'start'});
    history.replaceState(null,'',link.hash);
    target.setAttribute('tabindex','-1');target.focus({preventScroll:true});
  }));
  addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});
  setMotion(paused);
})();
