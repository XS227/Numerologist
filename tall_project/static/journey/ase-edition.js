(() => {
  const root = document.getElementById('ase-engine');
  if (!root) return;
  const form = root.querySelector('[data-engine-form]');
  const reading = root.querySelector('[data-reading]');
  const errorBox = root.querySelector('[data-form-error]');
  const langRaw = (root.dataset.lang || 'no').toLowerCase();
  const lang = langRaw.startsWith('fa') ? 'fa' : (langRaw.startsWith('en') ? 'en' : 'no');
  const MASTER = {11:1,22:1,33:1};
  const VALID = new Set([1,2,3,4,5,6,7,8,9,11,22,33]);
  const VALUES = {A:1,J:1,S:1,'Ø':1,B:2,K:2,T:2,'Å':2,C:3,L:3,U:3,D:4,M:4,V:4,E:5,N:5,W:5,F:6,O:6,X:6,G:7,P:7,Y:7,H:8,Q:8,Z:8,I:9,R:9,'Æ':9};
  const VOWELS = new Set(['A','E','I','O','U','Æ','Ø','Å']);
  const STORE = 'numerologist.aseedition.v1';

  const VOICE = {
    no:{
      1:{key:'initiativ og selvstendighet',gift:'du ser raskt hvor noen må ta initiativ og tør å være den som går først',shadow:'du kan presse tempoet så høyt at andre ikke rekker å komme med',work:'ledelse, oppstart og situasjoner der tydelige valg må tas'},
      2:{key:'samarbeid og finfølelse',gift:'du registrerer nyanser mellom mennesker og kan skape ro der andre skaper friksjon',shadow:'du kan tilpasse deg så mye at dine egne behov blir uklare',work:'samarbeid, diplomati og roller der tillit er avgjørende'},
      3:{key:'uttrykk og kreativitet',gift:'du kan gjøre tanker levende gjennom språk, humor, idéer og formidling',shadow:'du kan spre energien over for mange idéer før de får en tydelig form',work:'kommunikasjon, kreativitet, læring og synlig formidling'},
      4:{key:'struktur og gjennomføring',gift:'du kan bygge orden, system og noe som tåler tid',shadow:'du kan holde for hardt i planen når virkeligheten ber om fleksibilitet',work:'drift, økonomi, systembygging og langsiktig ansvar'},
      5:{key:'frihet og bevegelse',gift:'du tilpasser deg raskt, lærer gjennom erfaring og åpner dører andre ikke ser',shadow:'du kan bytte retning før en erfaring har fått modnes ferdig',work:'variasjon, salg, reise, media og miljøer med endring'},
      6:{key:'omsorg og ansvar',gift:'du har et sterkt instinkt for å skape trygghet, kvalitet og tilhørighet rundt deg',shadow:'du kan ta ansvar for mer enn det som egentlig tilhører deg',work:'veiledning, mennesker, estetikk, familie og ansvarsbærende roller'},
      7:{key:'dybde og analyse',gift:'du går under overflaten og trenger å forstå før du konkluderer',shadow:'du kan trekke deg så langt inn i refleksjon at andre ikke vet hvor de har deg',work:'analyse, forskning, spesialistarbeid og fordypning'},
      8:{key:'kraft og resultater',gift:'du kan omsette ambisjon til målbare resultater og forvalte ansvar, ressurser og makt',shadow:'du kan bli for hard mot deg selv eller måle egenverdien i prestasjon',work:'ledelse, økonomi, eierskap, forhandling og resultatansvar'},
      9:{key:'perspektiv og fullføring',gift:'du ser det større bildet og kan løfte erfaring til forståelse som også hjelper andre',shadow:'du kan holde fast i mennesker eller historier som egentlig er ferdige',work:'formidling, humanitært arbeid, kunst og roller med bredt perspektiv'},
      11:{key:'intuisjon og inspirasjon',gift:'du fanger opp stemninger, symboler og muligheter tidlig og kan tenne noe i andre',shadow:'den høye sensitiviteten kan gi uro når du mangler jordkontakt og rytme',work:'inspirasjon, kreativ ledelse, veiledning og arbeid med idéer som ennå ikke er fullt synlige'},
      22:{key:'stor visjon og byggkraft',gift:'du kan se stort uten å miste evnen til å gjøre visjonen konkret',shadow:'store forventninger kan bli så tunge at du utsetter første byggestein',work:'store prosjekter, organisasjon, entreprenørskap og varige strukturer'},
      33:{key:'omsorg, læring og løft',gift:'du kan lære bort gjennom eksempel og få andre til å føle seg sett og løftet',shadow:'du kan begynne å bære mennesker i stedet for å støtte dem',work:'undervisning, veiledning, omsorg og verdibasert formidling'}
    },
    en:{
      1:{key:'initiative and independence',gift:'you quickly see where someone has to take the first step and you are willing to be that person',shadow:'you can push the pace so hard that other people struggle to come with you',work:'leadership, starting things and roles that need decisive action'},
      2:{key:'cooperation and sensitivity',gift:'you notice subtle human dynamics and can create calm where others create friction',shadow:'you can adapt so much that your own needs become difficult to hear',work:'partnership, diplomacy and trust-based work'},
      3:{key:'expression and creativity',gift:'you make ideas vivid through language, humour, imagination and communication',shadow:'your energy can scatter across too many ideas before they take form',work:'communication, creativity, learning and visible expression'},
      4:{key:'structure and follow-through',gift:'you can build order, systems and foundations that last',shadow:'you can hold the plan too tightly when life asks for flexibility',work:'operations, finance, systems and long-term responsibility'},
      5:{key:'freedom and movement',gift:'you adapt quickly, learn through experience and notice openings other people miss',shadow:'you can change direction before an experience has had time to mature',work:'variety, sales, travel, media and changing environments'},
      6:{key:'care and responsibility',gift:'you have a strong instinct for creating safety, quality and belonging',shadow:'you can carry responsibilities that never truly belonged to you',work:'guidance, people, aesthetics, family and responsibility'},
      7:{key:'depth and analysis',gift:'you go beneath the surface and need to understand before you conclude',shadow:'you can retreat so far into reflection that others no longer know where they stand with you',work:'analysis, research, specialism and deep work'},
      8:{key:'power and results',gift:'you can turn ambition into measurable results and handle responsibility, resources and influence',shadow:'you can become too hard on yourself or tie self-worth to achievement',work:'leadership, finance, ownership, negotiation and measurable outcomes'},
      9:{key:'perspective and completion',gift:'you see the bigger picture and can turn experience into understanding that helps others',shadow:'you can hold on to people or stories that are already complete',work:'communication, humanitarian work, art and broad perspective'},
      11:{key:'intuition and inspiration',gift:'you notice patterns, moods and possibilities early and can ignite something in other people',shadow:'high sensitivity can turn into nervous overload without grounding',work:'inspiration, creative leadership, guidance and emerging ideas'},
      22:{key:'large vision and building power',gift:'you can think on a large scale without losing the ability to make the vision concrete',shadow:'the size of the vision can make the first step feel too heavy',work:'large projects, organisations, entrepreneurship and lasting structures'},
      33:{key:'care, teaching and uplift',gift:'you can teach by example and make people feel seen, held and elevated',shadow:'you can start carrying people instead of supporting them',work:'teaching, guidance, care and values-led communication'}
    },
    fa:{
      1:{key:'آغازگری و استقلال',gift:'خیلی زود می‌بینید کجا باید کسی قدم اول را بردارد و از پیش‌قدم شدن نمی‌ترسید',shadow:'ممکن است سرعت را آن‌قدر بالا ببرید که دیگران نتوانند همراه شوند',work:'رهبری، شروع پروژه و موقعیت‌هایی که تصمیم روشن می‌خواهند'},
      2:{key:'همکاری و حساسیت',gift:'ظرافت‌های انسانی را می‌بینید و می‌توانید تنش را به آرامش تبدیل کنید',shadow:'گاهی آن‌قدر سازگار می‌شوید که نیازهای خودتان کمرنگ می‌شوند',work:'همکاری، دیپلماسی و نقش‌های مبتنی بر اعتماد'},
      3:{key:'بیان و خلاقیت',gift:'فکر را با زبان، شوخ‌طبعی و خلاقیت زنده می‌کنید',shadow:'ممکن است انرژی میان ایده‌های زیاد پخش شود',work:'ارتباطات، خلاقیت، آموزش و بیان'},
      4:{key:'ساختار و استمرار',gift:'می‌توانید نظم و پایه‌ای بسازید که دوام بیاورد',shadow:'گاهی برنامه را بیش از حد محکم نگه می‌دارید',work:'عملیات، مالی، سیستم‌سازی و مسئولیت بلندمدت'},
      5:{key:'آزادی و حرکت',gift:'سریع سازگار می‌شوید و از تجربه یاد می‌گیرید',shadow:'ممکن است پیش از کامل شدن تجربه جهت را عوض کنید',work:'تنوع، فروش، سفر، رسانه و محیط‌های متغیر'},
      6:{key:'مراقبت و مسئولیت',gift:'غریزه قوی برای ساختن امنیت و تعلق دارید',shadow:'ممکن است مسئولیت‌هایی را بردارید که متعلق به شما نیست',work:'راهنمایی، مردم، زیبایی و نقش‌های مسئولیت‌محور'},
      7:{key:'عمق و تحلیل',gift:'زیر سطح را می‌بینید و پیش از نتیجه‌گیری می‌خواهید بفهمید',shadow:'ممکن است آن‌قدر در فکر فرو بروید که دیگران فاصله احساس کنند',work:'تحلیل، پژوهش و کار تخصصی'},
      8:{key:'قدرت و نتیجه',gift:'بلندپروازی را به نتیجه قابل اندازه‌گیری تبدیل می‌کنید',shadow:'ممکن است ارزش خود را بیش از حد با عملکرد بسنجید',work:'رهبری، مالی، مالکیت و مذاکره'},
      9:{key:'دید وسیع و تکمیل',gift:'تصویر بزرگ را می‌بینید و تجربه را به فهم تبدیل می‌کنید',shadow:'گاهی چیزی را که تمام شده دیر رها می‌کنید',work:'هنر، ارتباطات، خدمت و نگاه گسترده'},
      11:{key:'شهود و الهام',gift:'الگوها و امکان‌ها را زود حس می‌کنید و در دیگران جرقه می‌زنید',shadow:'حساسیت بالا بدون زمین‌گیری می‌تواند به آشفتگی تبدیل شود',work:'الهام، رهبری خلاق و راهنمایی'},
      22:{key:'چشم‌انداز بزرگ و ساختن',gift:'بزرگ فکر می‌کنید و در عین حال می‌توانید آن را واقعی کنید',shadow:'بزرگی چشم‌انداز گاهی قدم اول را سنگین می‌کند',work:'پروژه‌های بزرگ، سازمان و ساختار ماندگار'},
      33:{key:'مراقبت و آموزش',gift:'با الگو بودن آموزش می‌دهید و دیگران را بالا می‌برید',shadow:'ممکن است به‌جای حمایت، بار دیگران را حمل کنید',work:'آموزش، راهنمایی و خدمت ارزش‌محور'}
    }
  };

  const UI = {
    no:{title:n=>`${n}, du er ikke bare ett tall.`,core:'Det er samspillet mellom tallene som gjør kartet ditt personlig.',strength:'Her ligger den naturlige styrken din.',friction:'Her vil livet oftest be deg justere.',now:'Dette er energien som er aktiv rundt deg nå.',long:'Dette er den lengre utviklingslinjen jeg ser.',env:'Også tallene rundt deg legger et lite ekstra lag.',partner:n=>`Når jeg legger ${n} inn i kartet ditt, ser jeg dette.`,required:'Jeg trenger fornavn, etternavn og en gyldig fødselsdato før jeg kan bygge kartet.',read:'Les om',dominant:'gjentar seg',personalYear:'Personlig år',personalMonth:'Personlig måned',essence:'Essenstall',physical:'Fysisk transitt',mental:'Mental transitt',spiritual:'Spirituell transitt',name:'Navnetall',soul:'Vokaltall / indre drivkraft',personality:'Konsonanttall / ytre uttrykk',destiny:'Skjebnetall / livsvei',birthday:'Fødselsdagstall',currentName:'Nåværende navnetall',currentVowel:'Nåværende vokaltall',cornerstone:'Hjørnestein',bridge:'Livsvei ↔ navn',vcBridge:'Vokal ↔ konsonant',balance:'Balansetall',address:'Adressetall',health:'Helseprofil (symbolsk)',pinnacles:'4 utviklingstrinn',lifeCycles:'3 livsperioder',maturity:'Realiseringstall',challenges:'4 utfordringstall',lucky:'Lykketall',phone:'Telefonnummer',karmicDebt:'Karmisk gjeld',karmicLessons:'Karmiske læringstall'},
    en:{title:n=>`${n}, you are not one number.`,core:'It is the interaction between the numbers that makes your chart personal.',strength:'This is where your natural strength gathers.',friction:'This is where life most often asks you to adjust.',now:'This is the timing active around you now.',long:'This is the longer developmental arc I see.',env:'The numbers around you add another small layer.',partner:n=>`When I place ${n} into your chart, this is what stands out.`,required:'I need your first name, surname and a valid date of birth before I can build the chart.',read:'Read about',dominant:'repeats',personalYear:'Personal Year',personalMonth:'Personal Month',essence:'Essence Number',physical:'Physical Transit',mental:'Mental Transit',spiritual:'Spiritual Transit',name:'Name Number',soul:'Vowel / inner drive',personality:'Consonant / outer expression',destiny:'Destiny / Life Path',birthday:'Birthday Number',currentName:'Current Name Number',currentVowel:'Current Vowel Number',cornerstone:'Cornerstone',bridge:'Life Path ↔ Name',vcBridge:'Vowel ↔ Consonant',balance:'Balance Number',address:'Address Number',health:'Health profile (symbolic)',pinnacles:'4 Pinnacles',lifeCycles:'3 Life Cycles',maturity:'Maturity Number',challenges:'4 Challenge Numbers',lucky:'Lucky Number',phone:'Telephone Number',karmicDebt:'Karmic Debt',karmicLessons:'Karmic Lessons'},
    fa:{title:n=>`${n}، شما فقط یک عدد نیستید.`,core:'شخصی بودن نمودار از تعامل میان عددها می‌آید.',strength:'قدرت طبیعی شما بیشتر اینجا جمع می‌شود.',friction:'زندگی بیشتر در اینجا از شما تنظیم و رشد می‌خواهد.',now:'این ریتمی است که اکنون پیرامون شما فعال است.',long:'این مسیر بلندتر رشد شماست.',env:'عددهای پیرامون شما هم لایه دیگری اضافه می‌کنند.',partner:n=>`وقتی ${n} را در کنار نمودار شما می‌گذارم، این نکات برجسته می‌شوند.`,required:'برای ساختن نمودار به نام، نام خانوادگی و تاریخ تولد معتبر نیاز دارم.',read:'بخوانید درباره',dominant:'تکرار می‌شود',personalYear:'سال شخصی',personalMonth:'ماه شخصی',essence:'عدد جوهره',physical:'ترانزیت جسمی',mental:'ترانزیت ذهنی',spiritual:'ترانزیت معنوی',name:'عدد نام',soul:'عدد واکه / انگیزه درونی',personality:'عدد همخوان / بیان بیرونی',destiny:'عدد سرنوشت / مسیر زندگی',birthday:'عدد روز تولد',currentName:'عدد نام فعلی',currentVowel:'عدد واکه فعلی',cornerstone:'سنگ بنا',bridge:'پل مسیر ↔ نام',vcBridge:'پل واکه ↔ همخوان',balance:'عدد تعادل',address:'عدد آدرس',health:'پروفایل سلامت (نمادین)',pinnacles:'۴ مرحله رشد',lifeCycles:'۳ دوره زندگی',maturity:'عدد تحقق',challenges:'۴ عدد چالش',lucky:'عدد شانس',phone:'عدد تلفن',karmicDebt:'بدهی کارمایی',karmicLessons:'درس‌های کارمایی'}
  }[lang];

  const COMPAT_PERSONAL=[
    ['B','A','B','D','C','B','C','A/D','D'],['A','A','B','B','D','B','B','B','A'],['B','B','D','C','C','B','B','C','A'],
    ['D','B','C','B','C','B','A','B','B'],['C','D','C','C','A/D','B','D','A','B'],['B','B','B','B','B','A','D','A','A'],
    ['C','B','B','A','D','D','A','B','A'],['A/D','A','C','B','A','A','B','A/D','B'],['D','A','A','B','B','A','A','B','A']
  ];
  const COMPAT_WORK=[
    ['B','A','C','B','B','B','C','A','C'],['A','C','C','B','D','D','D','B','A'],['C','C','D','C','B','B','B','A','D'],
    ['B','B','C','A','C','B','A','A','C'],['B','D','B','C','D','C','D','A','B'],['B','D','B','B','C','D','D','B','A'],
    ['C','D','B','A','D','D','D','A','C'],['A','B','A','A','A','B','A','A/D','C'],['C','A','D','C','B','A','C','C','B']
  ];
  const COMPAT_TEXT = {
    no:{A:['Svært harmonisk','Åses kart viser en svært harmonisk kombinasjon med god naturlig flyt.'],B:['God dynamikk','Dette er en god kombinasjon som vanligvis har et støttende grunnlag.'],C:['Blandet / lærende','Her finnes mer forskjell i tempo eller behov, og bevisst kommunikasjon blir viktig.'],D:['Krevende','Denne kombinasjonen kan kreve tydelige grenser, timing og vilje til å forstå ulikheter.'],'A/D':['Sterk polaritet','Dette kan kjennes svært godt eller svært krevende. Intensiteten er selve kjennetegnet.']},
    en:{A:['Very harmonious','Åse’s chart shows a very harmonious pairing with naturally good flow.'],B:['Good dynamic','A supportive combination with a generally good foundation.'],C:['Mixed / learning','Different needs or pace make conscious communication more important.'],D:['Demanding','This pairing can require clear boundaries, timing and active understanding.'],'A/D':['Strong polarity','This can feel exceptionally supportive or exceptionally demanding; intensity is the signature.']},
    fa:{A:['بسیار هماهنگ','در جدول Åse این ترکیب جریان طبیعی و هماهنگی زیادی دارد.'],B:['دینامیک خوب','ترکیبی حمایتگر با پایه‌ای عموماً خوب.'],C:['ترکیبی / آموزشی','تفاوت در نیاز یا سرعت، گفت‌وگوی آگاهانه‌تری می‌خواهد.'],D:['چالش‌برانگیز','مرزها، زمان‌بندی و درک فعال تفاوت‌ها اهمیت بیشتری دارند.'],'A/D':['قطبیت قوی','این ترکیب می‌تواند بسیار حمایتگر یا بسیار دشوار حس شود؛ شدت ویژگی اصلی آن است.']}
  }[lang];

  function norm(v){return String(v||'').toUpperCase().normalize('NFC').trim()}
  function words(v){return norm(v).split(/\s+/).map(w=>w.replace(/[-'’]/g,'')).filter(Boolean)}
  function rootDigit(n){n=Math.abs(Number(n)||0);while(n>9)n=String(n).split('').reduce((a,c)=>a+Number(c),0);return n}
  function reduceMaster(n){n=Math.abs(Number(n)||0);while(n>9&&!MASTER[n])n=String(n).split('').reduce((a,c)=>a+Number(c),0);return n}
  function notation(raw){const kept=reduceMaster(raw),root=rootDigit(kept);return{raw,kept,root,label:(raw>9?raw+'/'+root:String(root))}}
  function vowelAt(word,i){const ch=word[i];if(VOWELS.has(ch))return true;if(ch!=='Y')return false;const prev=word[i-1]||'',next=word[i+1]||'';return !((i===0&&VOWELS.has(next))||VOWELS.has(prev)||VOWELS.has(next))}
  function nameCalc(value,mode='all'){const parts=[];words(value).forEach(word=>{let sum=0;Array.from(word).forEach((ch,i)=>{if(!(ch in VALUES))return;const vowel=vowelAt(word,i);if(mode==='vowels'&&!vowel)return;if(mode==='consonants'&&vowel)return;sum+=VALUES[ch]});if(sum)parts.push({word,sum,reduced:reduceMaster(sum)})});const raw=parts.reduce((a,p)=>a+p.reduced,0),n=notation(raw);n.parts=parts;return n}
  function dateParts(iso){const m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(iso||'');if(!m)return null;const y=+m[1],month=+m[2],day=+m[3],d=new Date(Date.UTC(y,month-1,day));if(d.getUTCFullYear()!==y||d.getUTCMonth()!==month-1||d.getUTCDate()!==day)return null;return{year:y,month,day}}
  function destiny(iso){const p=dateParts(iso);if(!p)return null;const d=reduceMaster(p.day),m=reduceMaster(p.month),y=reduceMaster(String(p.year).split('').reduce((a,c)=>a+Number(c),0));const n=notation(d+m+y);n.day=p.day;n.month=p.month;n.year=p.year;return n}
  function initialsCalc(value){let raw=0;const parts=[];words(value).forEach(w=>{const ch=Array.from(w).find(c=>c in VALUES);if(ch){raw+=VALUES[ch];parts.push(ch)}});const n=notation(raw);n.parts=parts;return n}
  function addressCalc(value){const s=norm(value),digits=s.match(/\d+/);let raw=0,explain='';if(digits){raw=digits[0].split('').reduce((a,c)=>a+Number(c),0);const tail=s.slice((digits.index||0)+digits[0].length),letter=Array.from(tail).find(c=>c in VALUES);if(letter)raw+=VALUES[letter];explain=digits[0]+(letter?' + '+letter:'')}else Array.from(s).forEach(c=>{if(c in VALUES)raw+=VALUES[c]});const n=notation(raw);n.explain=explain;return n}
  function phoneCalc(v){const digits=String(v||'').match(/\d/g)||[];if(!digits.length)return null;const raw=digits.reduce((a,c)=>a+Number(c),0);return{raw,root:rootDigit(raw),digits:digits.join('')}}
  function currentAge(birth,at){const b=dateParts(birth),a=dateParts(at);if(!b||!a)return null;let age=a.year-b.year;if(a.month<b.month||(a.month===b.month&&a.day<b.day))age--;return age>=0?age:null}
  function personalYear(birth,year){const p=dateParts(birth);if(!p)return null;const y=rootDigit(String(year).split('').reduce((a,c)=>a+Number(c),0));return rootDigit(rootDigit(p.day)+rootDigit(p.month)+y)}
  function personalMonth(birth,analysis){const a=dateParts(analysis);if(!a)return null;const py=personalYear(birth,a.year);return{year:py,month:rootDigit(py+rootDigit(a.month))}}
  function transit(value,age){const letters=Array.from(norm(value)).filter(c=>c in VALUES);if(!letters.length||!Number.isInteger(age)||age<0)return null;const total=letters.reduce((a,c)=>a+VALUES[c],0),pos=age%total;let cum=0;for(const letter of letters){const start=cum,end=cum+VALUES[letter]-1;if(pos>=start&&pos<=end){const cycleStart=age-pos;return{letter,value:VALUES[letter],start:cycleStart+start,end:cycleStart+end,total}}cum+=VALUES[letter]}return null}
  function pinnacleCycles(birth){const p=dateParts(birth),life=destiny(birth);if(!p||!life)return null;const d=reduceMaster(p.day),m=reduceMaster(p.month),y=reduceMaster(String(p.year).split('').reduce((a,c)=>a+Number(c),0));const vals=[notation(d+m),notation(y+d)];vals.push(notation(vals[0].kept+vals[1].kept),notation(y+m));const firstEnd=36-life.root;return{values:vals,ranges:[`0–${firstEnd}`,`${firstEnd+1}–${firstEnd+9}`,`${firstEnd+10}–${firstEnd+18}`,`${firstEnd+19}+`]}}
  function lifeCycles(birth){const p=dateParts(birth),life=destiny(birth);if(!p||!life)return null;const firstEnd=36-life.root;return{values:[reduceMaster(p.month),reduceMaster(p.day),reduceMaster(String(p.year).split('').reduce((a,c)=>a+Number(c),0))],ranges:[`0–${firstEnd}`,`${firstEnd+1}–${firstEnd+27}`,`${firstEnd+28}+`]}}
  function maturityCalc(name,birth){const n=nameCalc(name),d=destiny(birth);if(!n.raw||!d)return null;const r=notation(n.kept+d.kept);r.name=n;r.destiny=d;return r}
  function challenges(birth){const p=dateParts(birth);if(!p)return null;const d=rootDigit(p.day),m=rootDigit(p.month),y=rootDigit(String(p.year).split('').reduce((a,c)=>a+Number(c),0)),c1=Math.abs(m-d),c2=Math.abs(y-d);return[Math.abs(m-d),Math.abs(y-d),Math.abs(c1-c2),Math.abs(y-m)]}
  function karmicDebts(calcs){return calcs.map(x=>{const c=Number(x.calc.raw>9?x.calc.raw:x.calc.kept);return[13,14,16,19].includes(c)?{label:x.label,value:c+'/'+rootDigit(c)}:null}).filter(Boolean)}
  function karmicLessons(name,core){const present={};words(name).forEach(w=>Array.from(w).forEach(c=>{if(c in VALUES)present[VALUES[c]]=1}));const roots=core.map(x=>rootDigit(x)).filter(Boolean);return[1,2,3,4,5,6,7,8,9].filter(n=>!present[n]&&!roots.includes(n))}
  function compatGrade(a,b,context){a=rootDigit(a);b=rootDigit(b);return(context==='work'?COMPAT_WORK:COMPAT_PERSONAL)[a-1][b-1]}
  function voice(n){return VOICE[lang][VALID.has(Number(n))?Number(n):rootDigit(n)]||VOICE[lang][rootDigit(n)]}
  function linkNumber(n,label){const v=Number(n),target=VALID.has(v)?v:rootDigit(v);return target? `<a href="/numbers/${target}/">${label??n}</a>` : String(label??n)}
  function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
  function setText(sel,v){const el=root.querySelector(sel);if(el)el.textContent=v}
  function setHtml(sel,v){const el=root.querySelector(sel);if(el)el.innerHTML=v}
  function card(label,value,desc=''){return `<article class="ae-mini-card"><small>${esc(label)}</small><b>${value}</b>${desc?`<p>${desc}</p>`:''}</article>`}
  function cycle(label,value,desc){return `<article class="ae-cycle"><small>${esc(label)}</small><b>${value}</b><p>${esc(desc)}</p></article>`}
  function list(items){return items.map((x,i)=>`<div class="ae-list-item"><span>${String(i+1).padStart(2,'0')}</span><p>${x}</p></div>`).join('')}
  function ledger(label,value,desc=''){return `<article class="ae-ledger-card"><small>${esc(label)}</small><b>${value}</b>${desc?`<p>${esc(desc)}</p>`:''}</article>`}
  function dominant(nums){const counts={},order=[];nums.map(Number).filter(n=>VALID.has(n)).forEach(n=>{if(!(n in counts)){counts[n]=0;order.push(n)}counts[n]++});return order.sort((a,b)=>counts[b]-counts[a])[0]||1}
  function todayIso(){const d=new Date(),z=n=>String(n).padStart(2,'0');return `${d.getFullYear()}-${z(d.getMonth()+1)}-${z(d.getDate())}`}
  if(form.elements.analysisDate&&!form.elements.analysisDate.value)form.elements.analysisDate.value=todayIso();

  try{const saved=JSON.parse(localStorage.getItem(STORE)||'{}');root.querySelectorAll('input[name],select[name]').forEach(el=>{if(saved[el.name]&&!el.value)el.value=saved[el.name]})}catch(e){}
  form.addEventListener('input',saveForm);form.addEventListener('change',saveForm);
  function saveForm(){const data={};root.querySelectorAll('input[name],select[name]').forEach(el=>data[el.name]=el.value);try{localStorage.setItem(STORE,JSON.stringify(data))}catch(e){}}

  form.addEventListener('submit',e=>{
    e.preventDefault();
    errorBox.classList.remove('is-visible'); errorBox.textContent='';
    const first=form.elements.birthFirst.value.trim(),middle=form.elements.birthMiddle.value.trim(),last=form.elements.birthLast.value.trim(),birth=form.elements.birthDate.value,analysis=form.elements.analysisDate.value||todayIso();
    if(!first||!last||!dateParts(birth)){errorBox.textContent=UI.required;errorBox.classList.add('is-visible');return}
    const birthName=[first,middle,last].filter(Boolean).join(' ');
    const current=form.elements.currentName.value.trim()||birthName;
    const expression=nameCalc(birthName),soul=nameCalc(birthName,'vowels'),personality=nameCalc(birthName,'consonants'),life=destiny(birth),birthday=dateParts(birth).day;
    const currentName=nameCalc(current),currentVowel=nameCalc(current,'vowels'),corner=Array.from(norm(first)).find(c=>c in VALUES),cornerValue=corner?VALUES[corner]:0;
    const bridge=Math.abs(expression.root-life.root),vcBridge=Math.abs(soul.root-personality.root),balance=initialsCalc(birthName);
    const pm=personalMonth(birth,analysis),age=currentAge(birth,analysis);
    const physical=transit(first,age),mental=middle?transit(middle,age):null,spiritual=transit(last,age);
    const active=[physical,mental,spiritual].filter(Boolean),essence=notation(active.reduce((a,t)=>a+t.value,0));
    const pinnacles=pinnacleCycles(birth),cycles=lifeCycles(birth),maturity=maturityCalc(birthName,birth),challengeValues=challenges(birth),lucky=life;
    const addressRaw=form.elements.address.value.trim(),address=addressRaw?addressCalc(addressRaw):null,phoneRaw=form.elements.phone.value.trim(),phone=phoneRaw?phoneCalc(phoneRaw):null;
    const debtCalcs=[{label:UI.name,calc:expression},{label:UI.soul,calc:soul},{label:UI.personality,calc:personality},{label:UI.destiny,calc:life},{label:UI.currentName,calc:currentName}],debts=karmicDebts(debtCalcs);
    const lessons=karmicLessons(birthName,[expression.root,soul.root,personality.root,life.root,rootDigit(birthday)]);
    const coreNums=[life.kept,expression.kept,soul.kept,personality.kept,currentName.kept,currentVowel.kept,balance.kept,maturity.kept,rootDigit(birthday)],dom=dominant(coreNums);
    const firstDisplay=first.split(/\s+/)[0];

    const repeatCount=coreNums.filter(n=>Number(n)===dom).length;
    let opening='';
    if(lang==='no'){
      opening+=`<p>Når jeg ser på tallkartet ditt, <strong>${esc(firstDisplay)}</strong>, er det første jeg legger merke til spennet mellom <strong>${linkNumber(life.kept,life.label)}</strong> i livsveien og <strong>${linkNumber(expression.kept,expression.label)}</strong> i fødselsnavnet ditt. Livsveien din handler mye om ${voice(life.kept).key}, mens navnet ditt viser hvordan du naturlig forsøker å uttrykke ${voice(expression.kept).key}.</p>`;
      opening+=life.root===expression.root?`<p>Her gjentas samme grunntall i to av de tyngste posisjonene. Da blir temaet vanskelig å overse: det er ikke bare en side ved deg, men en tydelig signatur i kartet.</p>`:`<p>De to tallene er ikke identiske, og det er viktig. Du skal ikke presses inn i én type. Du bærer både behovet for ${voice(life.kept).key} og måten ${voice(expression.kept).key} kommer frem gjennom identiteten din.</p>`;
      opening+=`<p>På innsiden ligger <strong>${linkNumber(soul.kept,soul.label)}</strong>: ${voice(soul.kept).key}. Utad møter andre oftere <strong>${linkNumber(personality.kept,personality.label)}</strong>: ${voice(personality.kept).key}. ${soul.root===personality.root?'Det er en ganske tydelig linje mellom det du vil på innsiden og det andre oppfatter utenfra.':'Det betyr at mennesker ikke alltid ser med én gang hva som egentlig driver deg.'}</p>`;
      if(repeatCount>1)opening+=`<p>Og så er det <strong>${dom}</strong>. Det tallet gjentar seg flere steder. Når et tall gjør det, lytter jeg ekstra nøye til det: ${voice(dom).gift}.</p>`;
    }else if(lang==='fa'){
      opening+=`<p>وقتی به نمودار شما نگاه می‌کنم، <strong>${esc(firstDisplay)}</strong>، اولین چیزی که می‌بینم فاصله و گفت‌وگو میان <strong>${linkNumber(life.kept,life.label)}</strong> در مسیر زندگی و <strong>${linkNumber(expression.kept,expression.label)}</strong> در نام تولد است. مسیر زندگی شما بر ${voice(life.kept).key} تأکید دارد و نام شما ${voice(expression.kept).key} را وارد شیوه بیان هویت می‌کند.</p>`;
      opening+=`<p>در لایه درونی <strong>${linkNumber(soul.kept,soul.label)}</strong> دیده می‌شود: ${voice(soul.kept).key}. دیگران در برخورد اول بیشتر <strong>${linkNumber(personality.kept,personality.label)}</strong> و کیفیت ${voice(personality.kept).key} را می‌بینند.</p>`;
      if(repeatCount>1)opening+=`<p>عدد <strong>${dom}</strong> در چند جای نمودار تکرار می‌شود. این تکرار مهم است: ${voice(dom).gift}.</p>`;
    }else{
      opening+=`<p>When I look at your chart, <strong>${esc(firstDisplay)}</strong>, the first thing I notice is the conversation between <strong>${linkNumber(life.kept,life.label)}</strong> in your life path and <strong>${linkNumber(expression.kept,expression.label)}</strong> in your birth name. Your path leans toward ${voice(life.kept).key}, while your name expresses ${voice(expression.kept).key}.</p>`;
      opening+=`<p>Inside, <strong>${linkNumber(soul.kept,soul.label)}</strong> points toward ${voice(soul.kept).key}. Other people initially meet <strong>${linkNumber(personality.kept,personality.label)}</strong>: ${voice(personality.kept).key}. ${soul.root===personality.root?'Your inner drive and outer impression are unusually aligned.':'People may not immediately see what is actually driving you underneath.'}</p>`;
      if(repeatCount>1)opening+=`<p><strong>${dom}</strong> repeats in several important positions. Repetition matters here: ${voice(dom).gift}.</p>`;
    }

    setText('[data-reading-title]',UI.title(firstDisplay));setHtml('[data-reading-opening]',opening);setText('[data-dominant-number]',dom);
    setHtml('[data-core-strip]',[
      [UI.destiny,life],[UI.name,expression],[UI.soul,soul],[UI.personality,personality]
    ].map(([l,n])=>`<span class="ae-core-chip">${esc(l)} <b>${linkNumber(n.kept,n.label)}</b></span>`).join(''));

    setText('[data-core-heading]',UI.core);
    const coreStory = lang==='no'
      ? `<p>Livsveien forteller hva slags læring og retning som følger deg over tid. Navnet viser hvordan du uttrykker potensialet. Vokaltallet sier noe om hva som trekker deg innenfra, mens konsonanttallet beskriver inngangen andre ofte møter først.</p><p>Hos deg er avstanden mellom livsvei og navn <strong>${bridge}</strong>, og mellom vokal og konsonant <strong>${vcBridge}</strong>. Små broer betyr at lagene ligger tett; større broer peker mot mer bevisst oversettelse mellom dem.</p>`
      : lang==='fa'
      ? `<p>مسیر زندگی جهت و درس بلندمدت را نشان می‌دهد. نام شیوه بیان این ظرفیت است؛ واکه انگیزه درونی و همخوان برداشت اولیه دیگران را نشان می‌دهد.</p><p>فاصله مسیر و نام شما <strong>${bridge}</strong> و فاصله واکه و همخوان <strong>${vcBridge}</strong> است.</p>`
      : `<p>The life path describes the long developmental direction. The name shows how you express potential, the vowel number points to inner motivation, and the consonant number describes the doorway other people usually meet first.</p><p>Your Life Path / Name bridge is <strong>${bridge}</strong>, while the Vowel / Consonant bridge is <strong>${vcBridge}</strong>.</p>`;
    setHtml('[data-core-story]',coreStory);
    setHtml('[data-core-cards]',[
      card(UI.destiny,linkNumber(life.kept,life.label),voice(life.kept).key),
      card(UI.name,linkNumber(expression.kept,expression.label),voice(expression.kept).key),
      card(UI.soul,linkNumber(soul.kept,soul.label),voice(soul.kept).key),
      card(UI.personality,linkNumber(personality.kept,personality.label),voice(personality.kept).key)
    ].join(''));

    setText('[data-strength-heading]',UI.strength);
    const strengths=[voice(life.kept).gift,voice(expression.kept).gift,voice(soul.kept).gift];
    if(repeatCount>1)strengths.push(lang==='no'?`At ${dom} gjentas, forsterker særlig dette: ${voice(dom).gift}.`:lang==='fa'?`تکرار ${dom} این کیفیت را تقویت می‌کند: ${voice(dom).gift}.`:`Because ${dom} repeats, this quality is amplified: ${voice(dom).gift}.`);
    strengths.push(lang==='no'?`Balansetallet ditt er ${balance.label}; under press vil du ofte finne fotfeste igjen gjennom ${voice(balance.kept).key}.`:lang==='fa'?`عدد تعادل شما ${balance.label} است؛ زیر فشار، ${voice(balance.kept).key} می‌تواند مسیر بازگشت به تعادل باشد.`:`Your Balance Number is ${balance.label}; under pressure, ${voice(balance.kept).key} is often part of the route back to equilibrium.`);
    setHtml('[data-strengths]',list(strengths));

    setText('[data-friction-heading]',UI.friction);
    const frictions=[voice(life.kept).shadow,voice(personality.kept).shadow];
    if(challengeValues)frictions.push(lang==='no'?`Utfordringstallene ${challengeValues.join(' · ')} viser at de samme læringstemaene kan komme tilbake i forskjellige livsfaser.`:lang==='fa'?`اعداد چالش ${challengeValues.join(' · ')} نشان می‌دهند برخی موضوع‌ها در دوره‌های مختلف بازمی‌گردند.`:`Challenge Numbers ${challengeValues.join(' · ')} suggest that related lessons can reappear in different life phases.`);
    if(debts.length)frictions.push((lang==='no'?'Karmiske sammentall i kartet: ':lang==='fa'?'اعداد مرکب کارمایی در نمودار: ':'Karmic compound numbers in the chart: ')+debts.map(x=>`${x.label} ${x.value}`).join(', ')+'.');
    if(lessons.length)frictions.push((lang==='no'?'Karmiske læringstall som ikke er representert i fødselsnavnet eller kjernekartet: ':lang==='fa'?'درس‌های کارمایی غایب از نام تولد و هسته نمودار: ':'Karmic lesson values missing from the birth name and core chart: ')+lessons.join(', ')+'.');
    setHtml('[data-frictions]',list(frictions));
    setHtml('[data-friction-story]',lang==='no'? `<p>Dette er ikke en liste over feil. Jeg leser disse tallene som steder der du må være mer bevisst enn ellers. Det som føles som friksjon tidlig i livet, kan senere bli en svært presis styrke.</p>`:lang==='fa'?'<p>این بخش فهرست نقص‌ها نیست؛ جاهایی است که آگاهی بیشتری می‌خواهد و همان چالش می‌تواند بعدها به توانایی تبدیل شود.</p>':'<p>This is not a list of flaws. These are places that ask for more awareness. What begins as friction can become a highly refined strength over time.</p>');

    setText('[data-practical-heading]',lang==='no'?'Slik merkes tallene dine når livet faktisk skjer.':lang==='fa'?'عددهای شما در زندگی واقعی این‌طور دیده می‌شوند.':'This is how your numbers tend to show up in real life.');
    const practicalStory = lang==='no'
      ? `<p>I arbeid trenger du særlig rom for ${voice(life.kept).work}. Navnet ditt legger i tillegg vekt på ${voice(expression.kept).work}. Det betyr at du fungerer best når både retningen og måten du uttrykker deg på får plass.</p><p>I nære relasjoner er vokaltallet viktigere enn mange tror. Innerst søker du ${voice(soul.kept).key}, mens andre først kan møte ${voice(personality.kept).key}. Når de to lagene er forskjellige, trenger du mennesker som er nysgjerrige nok til å bli kjent med mer enn førsteinntrykket.</p>`
      : lang==='fa'
      ? `<p>در کار، شما به فضایی برای ${voice(life.kept).work} نیاز دارید و عدد نام نیز بر ${voice(expression.kept).work} تأکید می‌کند.</p><p>در رابطه نزدیک، درون شما به ${voice(soul.kept).key} کشیده می‌شود، در حالی که دیگران ابتدا ${voice(personality.kept).key} را می‌بینند.</p>`
      : `<p>At work, you need room for ${voice(life.kept).work}, while your Name Number adds an emphasis on ${voice(expression.kept).work}. You tend to do best when both the direction and your natural way of expressing it are allowed to coexist.</p><p>In close relationships, the Vowel Number matters more than many people realise. Inside you seek ${voice(soul.kept).key}, while other people may initially meet ${voice(personality.kept).key}. When those layers differ, you benefit from people who are curious enough to look beyond the first impression.</p>`;
    setHtml('[data-practical-story]',practicalStory);
    setHtml('[data-practical-cards]',[
      card(lang==='no'?'Arbeid':lang==='fa'?'کار':'Work',linkNumber(life.kept,life.label),voice(life.kept).work),
      card(lang==='no'?'Nære relasjoner':lang==='fa'?'رابطه نزدیک':'Close relationships',linkNumber(soul.kept,soul.label),voice(soul.kept).key)
    ].join(''));

    setText('[data-now-heading]',UI.now);
    const nowStory = lang==='no'
      ? `<p>På analysedatoen er du ${age} år. Det personlige året ditt er <strong>${pm.year}</strong>, og måneden ligger på <strong>${pm.month}</strong>. Samtidig er essenstallet <strong>${essence.label}</strong>. Når jeg ser disse sammen, får jeg en mer presis følelse av hva som er i bevegelse akkurat nå: ${voice(pm.year).key} ligger som årsrytme, mens ${voice(pm.month).key} farger den kortere perioden.</p>`
      : lang==='fa'
      ? `<p>در تاریخ این خوانش ${age} ساله هستید. سال شخصی <strong>${pm.year}</strong> و ماه شخصی <strong>${pm.month}</strong> است و عدد جوهره <strong>${essence.label}</strong>. سال ریتم بزرگ‌تر و ماه لحن کوتاه‌تر را می‌دهد.</p>`
      : `<p>On the reading date you are ${age}. Your Personal Year is <strong>${pm.year}</strong> and your Personal Month is <strong>${pm.month}</strong>, while the Essence Number is <strong>${essence.label}</strong>. The year sets the larger rhythm; the month colours the shorter period.</p>`;
    setHtml('[data-now-story]',nowStory);
    const nowCards=[
      cycle(UI.personalYear,linkNumber(pm.year,pm.year),voice(pm.year).key),
      cycle(UI.personalMonth,linkNumber(pm.month,pm.month),voice(pm.month).key),
      cycle(UI.essence,linkNumber(essence.kept,essence.label),voice(essence.kept).key),
      physical?cycle(UI.physical,`${esc(physical.letter)} · ${linkNumber(physical.value,physical.value)}`,`${physical.start}–${physical.end}`):''
    ];
    if(mental)nowCards.push(cycle(UI.mental,`${esc(mental.letter)} · ${linkNumber(mental.value,mental.value)}`,`${mental.start}–${mental.end}`));
    if(spiritual)nowCards.push(cycle(UI.spiritual,`${esc(spiritual.letter)} · ${linkNumber(spiritual.value,spiritual.value)}`,`${spiritual.start}–${spiritual.end}`));
    setHtml('[data-now-grid]',nowCards.join(''));

    setText('[data-long-heading]',UI.long);
    setHtml('[data-long-story]',lang==='no'?`<p>De korte syklusene forteller om timingen. De lange syklusene forteller om modningen. Utviklingstrinnene dine beveger seg gjennom <strong>${pinnacles.values.map(x=>x.label).join(' → ')}</strong>, mens realiseringstallet lander på <strong>${maturity.label}</strong>. Det siste tallet blir ofte tydeligere jo mer erfaring du får.</p>`:lang==='fa'?`<p>چرخه‌های کوتاه زمان‌بندی را نشان می‌دهند و چرخه‌های بلند، روند پختگی را. مراحل رشد شما <strong>${pinnacles.values.map(x=>x.label).join(' ← ')}</strong> است و عدد تحقق <strong>${maturity.label}</strong>.</p>`:`<p>The short cycles describe timing; the long cycles describe maturation. Your Pinnacles move through <strong>${pinnacles.values.map(x=>x.label).join(' → ')}</strong>, while your Maturity Number lands on <strong>${maturity.label}</strong>.</p>`);
    const seq=(vals,ranges)=>vals.map((x,i)=>`<a href="/numbers/${VALID.has(Number(x.kept??x))?Number(x.kept??x):rootDigit(x.kept??x)}/" title="${ranges?ranges[i]:''}">${esc(x.label??x)}</a>`).join('');
    setHtml('[data-long-grid]',[
      `<article class="ae-long-card"><small>${esc(UI.pinnacles)}</small><b>${pinnacles.values.map(x=>x.label).join(' · ')}</b><div class="ae-long-card__sequence">${seq(pinnacles.values,pinnacles.ranges)}</div><p>${pinnacles.ranges.join(' · ')}</p></article>`,
      `<article class="ae-long-card"><small>${esc(UI.lifeCycles)}</small><b>${cycles.values.join(' · ')}</b><div class="ae-long-card__sequence">${cycles.values.map((x,i)=>`<a href="/numbers/${VALID.has(x)?x:rootDigit(x)}/" title="${cycles.ranges[i]}">${x}</a>`).join('')}</div><p>${cycles.ranges.join(' · ')}</p></article>`,
      `<article class="ae-long-card"><small>${esc(UI.maturity)}</small><b>${linkNumber(maturity.kept,maturity.label)}</b><p>${esc(voice(maturity.kept).key)}</p></article>`
    ].join(''));

    const envSec=root.querySelector('[data-environment-section]'),env=[];
    if(address&&address.raw)env.push(card(UI.address,linkNumber(address.kept,address.label),voice(address.kept).key));
    if(phone)env.push(card(UI.phone,linkNumber(phone.root,phone.root),voice(phone.root).key));
    if(env.length){envSec.hidden=false;setText('[data-environment-heading]',UI.env);setHtml('[data-environment]',env.join(''))}else envSec.hidden=true;

    const partnerName=form.elements.partnerName.value.trim(),partnerDate=form.elements.partnerDate.value,partnerSec=root.querySelector('[data-partner-section]');
    let partnerData=null;
    if(partnerName&&dateParts(partnerDate)){
      const pn=nameCalc(partnerName),pd=destiny(partnerDate),ctx=form.elements.partnerContext.value,gn=compatGrade(expression.root,pn.root,ctx),gd=compatGrade(life.root,pd.root,ctx),tn=COMPAT_TEXT[gn],td=COMPAT_TEXT[gd];
      partnerData={name:pn,destiny:pd,gn,gd,ctx};
      partnerSec.hidden=false;setText('[data-partner-heading]',UI.partner(partnerName.split(/\s+/)[0]));
      setHtml('[data-partner-story]',lang==='no'?`<p>Jeg ville ikke vurdert en relasjon ut fra ett tall. Derfor ser jeg både på navnelaget og livsveien. Navnene deres gir <strong>${gn}</strong>, mens skjebnetallene gir <strong>${gd}</strong>. Det er samspillet mellom de to som er interessant.</p>`:lang==='fa'?`<p>رابطه را با یک عدد نمی‌سنجم. لایه نام <strong>${gn}</strong> و لایه مسیر زندگی <strong>${gd}</strong> است؛ تعامل این دو مهم‌تر از یک امتیاز واحد است.</p>`:`<p>I would never judge a relationship from one number. The name layer gives <strong>${gn}</strong>, while the life-path layer gives <strong>${gd}</strong>. The interaction between both is more useful than one single score.</p>`);
      setHtml('[data-partner-grid]',`<article class="ae-compat-card"><div class="ae-compat-grade">${gn}</div><h3>${esc(tn[0])} · ${esc(UI.name)}</h3><p>${esc(tn[1])}</p></article><article class="ae-compat-card"><div class="ae-compat-grade">${gd}</div><h3>${esc(td[0])} · ${esc(UI.destiny)}</h3><p>${esc(td[1])}</p></article>`);
    }else partnerSec.hidden=true;

    const ledgerItems=[
      [UI.name,linkNumber(expression.kept,expression.label),birthName],
      [UI.soul,linkNumber(soul.kept,soul.label),''],
      [UI.personality,linkNumber(personality.kept,personality.label),''],
      [UI.currentName,linkNumber(currentName.kept,currentName.label),current],
      [UI.currentVowel,linkNumber(currentVowel.kept,currentVowel.label),''],
      [UI.destiny,linkNumber(life.kept,life.label),birth],
      [UI.birthday,String(birthday),`root ${rootDigit(birthday)}`],
      [UI.cornerstone,`${esc(corner||'–')} · ${cornerValue||'–'}`,''],
      [UI.bridge,String(bridge),''],
      [UI.vcBridge,String(vcBridge),''],
      [UI.balance,linkNumber(balance.kept,balance.label),''],
      [UI.karmicDebt,debts.length?debts.map(x=>esc(x.value)).join(' · '):'–',''],
      [UI.karmicLessons,lessons.length?lessons.join(' · '):'–',''],
      [UI.health,`${expression.root} · ${life.root}`,''],
      [UI.personalYear,linkNumber(pm.year,pm.year),dateParts(analysis).year],
      [UI.personalMonth,linkNumber(pm.month,pm.month),analysis.slice(0,7)],
      [UI.physical,physical?`${esc(physical.letter)} · ${linkNumber(physical.value,physical.value)}`:'–',physical?`${physical.start}–${physical.end}`:''],
      [UI.mental,mental?`${esc(mental.letter)} · ${linkNumber(mental.value,mental.value)}`:'–',mental?`${mental.start}–${mental.end}`:''],
      [UI.spiritual,spiritual?`${esc(spiritual.letter)} · ${linkNumber(spiritual.value,spiritual.value)}`:'–',spiritual?`${spiritual.start}–${spiritual.end}`:''],
      [UI.essence,linkNumber(essence.kept,essence.label),''],
      [UI.pinnacles,pinnacles.values.map(x=>x.label).join(' · '),''],
      [UI.lifeCycles,cycles.values.join(' · '),''],
      [UI.maturity,linkNumber(maturity.kept,maturity.label),''],
      [UI.challenges,challengeValues.join(' · '),''],
      [UI.lucky,linkNumber(lucky.kept,lucky.label),'']
    ];
    if(address&&address.raw)ledgerItems.push([UI.address,linkNumber(address.kept,address.label),addressRaw]);
    if(phone)ledgerItems.push([UI.phone,linkNumber(phone.root,phone.root),phoneRaw]);
    if(partnerData)ledgerItems.push([lang==='no'?'Partner · navn / livsvei':lang==='fa'?'شریک · نام / مسیر':'Partner · name / life path',`${partnerData.gn} · ${partnerData.gd}`,partnerName]);
    setHtml('[data-ledger]',ledgerItems.map(x=>ledger(x[0],x[1],x[2])).join(''));

    const allNums=[life.kept,expression.kept,soul.kept,personality.kept,currentName.kept,currentVowel.kept,balance.kept,maturity.kept,pm.year,pm.month,essence.kept,...pinnacles.values.map(x=>x.kept),...cycles.values,...challengeValues];
    if(address)allNums.push(address.kept);if(phone)allNums.push(phone.root);if(partnerData)allNums.push(partnerData.name.kept,partnerData.destiny.kept);
    const unique=[...new Set(allNums.map(Number).map(n=>VALID.has(n)?n:rootDigit(n)).filter(n=>VALID.has(n)))];
    setHtml('[data-number-links]',unique.map(n=>`<a href="/numbers/${n}/">${esc(UI.read)} ${n} →</a>`).join(''));

    reading.hidden=false;
    setTimeout(()=>reading.scrollIntoView({behavior:'smooth',block:'start'}),60);
  });

  root.querySelector('[data-print]')?.addEventListener('click',()=>window.print());
  root.querySelector('[data-new-reading]')?.addEventListener('click',()=>{reading.hidden=true;document.getElementById('ae-intake')?.scrollIntoView({behavior:'smooth'})});
})();