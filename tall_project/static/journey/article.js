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


/* Batch 2 interactive teaching widgets. */
(() => {
  const root = document.querySelector('.learning-journey');
  if (!root) return;

  // Sissel profile explorer
  const profile = root.querySelector('[data-profile-explorer]');
  if (profile) {
    const out = root.querySelector('[data-profile-output]');
    const copy = {
      '9':['9 — helhet og formidling','Åse bruker 9 som symbol på medfølelse, helhet og et ønske om å bidra utover seg selv.'],
      '11':['11/2 — sensitivitet og mottakelighet','Mestertallet 11 leses sammen med 2: inspirasjon, intuitiv oppmerksomhet og relasjonell følsomhet.'],
      '7':['7 — søken og fordypning','7 peker mot observasjon, analyse, stillhet og behovet for å forstå det som ligger under overflaten.'],
      '16':['16/7 — læring gjennom omstilling','16/7 brukes som et læretall: erfaring, korrigering av kurs og en stadig dypere søken etter mening.']
    };
    profile.querySelectorAll('button').forEach((b,i) => {
      if (!i) b.classList.add('is-active');
      b.addEventListener('click', () => {
        profile.querySelectorAll('button').forEach(x => x.classList.remove('is-active'));
        b.classList.add('is-active');
        const v = copy[b.dataset.profileKey];
        out.innerHTML = '<strong>'+v[0]+'</strong><span>'+v[1]+'</span>';
      });
    });
  }

  // Date / life-path demonstrator
  const life = root.querySelector('[data-life-calc]');
  if (life) {
    const input = life.querySelector('[data-life-date]');
    const result = life.querySelector('[data-life-result]');
    const reduce = n => {
      n = Number(n);
      while (n > 9 && ![11,22,33].includes(n)) n = String(n).split('').reduce((a,d)=>a+Number(d),0);
      return n;
    };
    life.querySelector('[data-life-go]').addEventListener('click', () => {
      if (!input.value) { result.textContent = 'Velg en dato først.'; return; }
      const [y,m,d] = input.value.split('-').map(Number);
      const rd=reduce(d), rm=reduce(m), ry=reduce(String(y).split('').reduce((a,x)=>a+Number(x),0));
      const total=rd+rm+ry, final=reduce(total);
      result.innerHTML = '<b>'+rd+' + '+rm+' + '+ry+' = '+total+(total!==final?' → '+final:'')+'</b><br>Dette er samme trinnvise metode som brukes i eksemplet over.';
    });
  }

  // Valentine's balance slider
  const love = root.querySelector('[data-love-slider]');
  if (love) {
    const range=love.querySelector('[data-love-range]'), output=love.querySelector('[data-love-output]');
    const paint=() => {
      const v=Number(range.value), freedom=100-v;
      let text='balanse mellom frihet og nærhet.';
      if (v < 35) text='mye frihet og variasjon — pass på at kontakten ikke blir for løs.';
      else if (v > 65) text='mye nærhet og samspill — pass på at begge fortsatt får eget rom.';
      output.textContent=freedom+'% frihet / '+v+'% nærhet — '+text;
    };
    range.addEventListener('input',paint); paint();
  }

  // Tesla fact / myth cards
  root.querySelectorAll('[data-tesla-card]').forEach(card => {
    card.addEventListener('click', () => {
      const fact = card.dataset.kind === 'fact';
      card.classList.toggle('is-open');
      card.querySelector('span').textContent = card.classList.contains('is-open')
        ? (fact ? 'Dokumentert del av Teslas tekniske arbeid.' : 'Senere populærkulturell påstand; sitatet er ikke sikkert dokumentert i primærkilder.')
        : 'Trykk for svar';
    });
  });

  // Fibonacci explorer
  const fibTool=root.querySelector('[data-fib-tool]');
  if (fibTool) {
    const range=fibTool.querySelector('[data-fib-range]');
    const value=fibTool.querySelector('[data-fib-value]'), ratio=fibTool.querySelector('[data-fib-ratio]'), dr=fibTool.querySelector('[data-fib-root]');
    const fib=n=>{let a=1,b=1;if(n<=2)return 1;for(let i=3;i<=n;i++){[a,b]=[b,a+b]}return b};
    const rootNum=n=>{while(n>9)n=String(n).split('').reduce((a,d)=>a+Number(d),0);return n};
    const paint=()=>{const n=Number(range.value), f=fib(n), prev=fib(n-1);value.textContent=f;ratio.textContent=(f/prev).toFixed(5);dr.textContent=rootNum(f)};
    range.addEventListener('input',paint); paint();
  }

  // Season wheel
  const season=root.querySelector('[data-season-wheel]');
  if (season) {
    const out=season.querySelector('[data-season-output]');
    const map={winter:['Vinter','Hvile · mørke · ny solsyklus'],spring:['Vår','Balanse · spiring · retning'],summer:['Sommer','Lys · vekst · maksimum'],autumn:['Høst','Innhøsting · balanse · overgang']};
    season.querySelectorAll('[data-season]').forEach(b=>b.addEventListener('click',()=>{
      season.querySelectorAll('[data-season]').forEach(x=>x.classList.remove('is-active'));b.classList.add('is-active');
      const v=map[b.dataset.season];out.innerHTML='<b>'+v[0]+'</b><span>'+v[1]+'</span>';
    }));
  }

  // Rune reflection draw
  const runeTool=root.querySelector('[data-rune-tool]');
  if (runeTool) {
    const runes=[
      ['ᚠ','Fehu','ressurser og hva du verdsetter'],['ᚢ','Uruz','kraft og utholdenhet'],['ᚦ','Thurisaz','grenser og friksjon'],['ᚨ','Ansuz','ord og kommunikasjon'],
      ['ᚱ','Raidho','retning og bevegelse'],['ᚲ','Kenaz','innsikt og skapende ild'],['ᚷ','Gebo','gave og gjensidighet'],['ᚹ','Wunjo','glede og tilhørighet'],
      ['ᚺ','Hagalaz','brudd og omstilling'],['ᚾ','Nauthiz','behov og begrensning'],['ᛁ','Isa','pause og konsentrasjon'],['ᛃ','Jera','syklus og resultat'],
      ['ᛇ','Eihwaz','utholdenhet og overgang'],['ᛈ','Perthro','det ukjente og mulighet'],['ᛉ','Algiz','vern og årvåkenhet'],['ᛋ','Sowilo','klarhet og retning'],
      ['ᛏ','Tiwaz','mot og prinsipp'],['ᛒ','Berkano','vekst og omsorg'],['ᛖ','Ehwaz','samarbeid og bevegelse'],['ᛗ','Mannaz','mennesket og fellesskapet'],
      ['ᛚ','Laguz','flyt og følelser'],['ᛜ','Ingwaz','modning og potensial'],['ᛞ','Dagaz','gjennombrudd og perspektiv'],['ᛟ','Othala','arv og tilhørighet']
    ];
    const out=runeTool.querySelector('[data-rune-results]');
    const pick=n=>{const pool=[...runes], chosen=[];for(let i=0;i<n;i++){const idx=Math.floor(Math.random()*pool.length);chosen.push(pool.splice(idx,1)[0])}return chosen};
    runeTool.querySelectorAll('[data-rune-draw]').forEach(b=>b.addEventListener('click',()=>{
      const chosen=pick(Number(b.dataset.runeDraw));
      out.innerHTML=chosen.map((r,i)=>'<div class="lj-rune-card"><span>'+r[0]+'</span><b>'+(chosen.length===3?['Fortid','Nåtid','Mulig retning'][i]+' · ':'')+r[1]+'</b><small>'+r[2]+'. Hva gjør dette temaet relevant akkurat nå?</small></div>').join('');
    }));
  }

  // Eclipse year explorer
  const eclipse=root.querySelector('[data-eclipse-tool]');
  if (eclipse) {
    const data={
      '2026':[['17. februar','Sol'],['3. mars','Måne'],['12. august','Sol'],['28. august','Måne']],
      '2027':[['6. februar','Sol'],['20. februar','Måne'],['18. juli','Måne'],['2. august','Sol'],['17. august','Måne']],
      '2028':[['11. januar','Måne'],['26. januar','Sol'],['6. juli','Måne'],['21. juli','Sol'],['31. desember','Måne']],
      '2029':[['14. januar','Sol'],['11. juni','Sol'],['25. juni','Måne'],['11. juli','Sol'],['5. desember','Sol'],['20. desember','Måne']],
      '2030':[['31. mai','Sol'],['15. juni','Måne'],['24. november','Sol'],['9. desember','Måne']]
    };
    const year=eclipse.querySelector('[data-eclipse-year]'), list=eclipse.querySelector('[data-eclipse-list]');
    const paint=()=>{list.innerHTML=data[year.value].map(x=>'<div class="lj-eclipse-event"><b>'+(x[1]==='Sol'?'☉':'☾')+' '+x[1]+'formørkelse</b><span>'+x[0]+' '+year.value+'</span></div>').join('')};
    year.addEventListener('change',paint);paint();
  }

  // Solfeggio audio demonstrator
  const tone=root.querySelector('[data-tone-tool]');
  if (tone) {
    const select=tone.querySelector('[data-tone-select]'), result=tone.querySelector('[data-tone-result]');
    const digitalRoot=n=>{const first=String(n).split('').map(Number), sum=first.reduce((a,b)=>a+b,0);let root=sum;while(root>9)root=String(root).split('').reduce((a,d)=>a+Number(d),0);return {digits:first,sum,root}};
    const paint=()=>{const n=Number(select.value),r=digitalRoot(n);result.textContent=n+' → '+r.digits.join('+')+' = '+r.sum+(r.sum!==r.root?' → '+r.root:'')};
    select.addEventListener('change',paint);paint();
    tone.querySelector('[data-tone-play]').addEventListener('click',()=>{
      const C=window.AudioContext||window.webkitAudioContext;if(!C)return;
      const ctx=new C(),osc=ctx.createOscillator(),gain=ctx.createGain();osc.type='sine';osc.frequency.value=Number(select.value);gain.gain.setValueAtTime(.0001,ctx.currentTime);gain.gain.exponentialRampToValueAtTime(.12,ctx.currentTime+.05);gain.gain.exponentialRampToValueAtTime(.0001,ctx.currentTime+1.9);osc.connect(gain).connect(ctx.destination);osc.start();osc.stop(ctx.currentTime+2);osc.onended=()=>ctx.close();
    });
  }

  // Primstav season switch
  const prim=root.querySelector('[data-primstav]');
  if (prim) {
    const track=prim.querySelector('[data-prim-track]'),copy=prim.querySelector('[data-prim-copy]');
    const state={
      winter:{track:'<span>🧤 14. okt</span><span>🪵 16. okt</span><span>❄ 14. jan</span><span>🌿 14. apr</span>',copy:'Vintersiden går tradisjonelt fra 14. oktober til 13. april. Vott/hanske kunne markere at vinterutstyret skulle være klart.'},
      summer:{track:'<span>🌿 14. apr</span><span>🌱 såtid</span><span>☀ midtsommer</span><span>✂ sesongarbeid</span>',copy:'Sommersiden går tradisjonelt fra 14. april til 13. oktober. Gren, løv og arbeidsmerker gjorde sesongen lesbar som symboler.'}
    };
    prim.querySelectorAll('[data-prim-side]').forEach(b=>b.addEventListener('click',()=>{prim.querySelectorAll('[data-prim-side]').forEach(x=>x.classList.remove('is-active'));b.classList.add('is-active');const v=state[b.dataset.primSide];track.innerHTML=v.track;copy.textContent=v.copy}));
  }
})();

