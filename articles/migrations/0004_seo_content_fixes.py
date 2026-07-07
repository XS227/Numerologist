"""Fix unrendered Markdown in two articles and add related-reading links.

navn-og-numerologi and master-number-33 were stored as raw Markdown
(``## heading``, ``**bold**``, a pipe table, ``[text](url)`` links) but the
template renders ``article.content`` directly as HTML with the ``safe``
filter and no Markdown conversion step. Live pages therefore showed literal
"##" characters instead of headings. This migration replaces the content
with equivalent hand-written HTML and appends a short FAQ + related-reading
block for internal linking, matching the pattern already used by the other
two articles in this app.
"""

from django.db import migrations


NAVN_SLUG = "navn-og-numerologi"
NAVN_OLD_CONTENT = """Har du noen gang lurt på hvorfor et navn føles riktig — eller galt — for en person? Numerologien gir et fascinerende svar: hvert navn bærer en numerisk vibrasjonen som former personligheten og uttrykksmåten.

## Uttrykkstallets grunnprinsipp

I numerologien tilsvarer hver bokstav i alfabetet et tall fra 1 til 9. Summen av tallverdiene i ditt fulle navn — slik det ble gitt deg ved fødsel — kalles **uttrykkstallets** (eller navnetallets) vibrasjon.

Dette tallet avslører din naturlige begavelse, din måte å uttrykke deg på i verden, og de egenskapene du ble gitt for å fullføre din livsoppgave.

## Slik beregner du uttrykkstallets

Bokstav-verdiene følger dette skjemaet:

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| A | B | C | D | E | F | G | H | I |
| J | K | L | M | N | O | P | Q | R |
| S | T | U | V | W | X | Y | Z |   |

**Eksempel:** Navn = ANNA
- A = 1, N = 5, N = 5, A = 1
- Sum: 1 + 5 + 5 + 1 = 12 → 1 + 2 = **3**

Anna har uttrykkstallets **3** — kreativitet, glede og kommunikasjon.

## Vokal- og konsonanttallene

Numerologien skiller mellom vokalene og konsonantene i navnet ditt:

- **Sjelstallets** (vokaler): avslører din indre motivasjon og hjertelengsel
- **Personlighetstallets** (konsonanter): viser det første inntrykket du gir andre

Til sammen utgjør disse tre tallene — uttrykk, sjel og personlighet — et komplett bilde av din navnevibrasjonen.

## Hvorfor føles noen navn «riktige»?

Åse Steinsland forklarer at vi instinktivt reagerer på navnevibrasjoner. Når et navn «klikker», er det fordi dets numeriske energi harmonerer med mottakerens eget tallmønster.

Dette er grunnen til at mange mennesker som bytter navn — etter ekteskap, transisjon eller personlig vekst — opplever at det nye navnet faktisk endrer noe i dem. Det er ikke bare symbolikk. Det er et skifte i vibrasjonsmønster.

## Utforsk ditt eget navn

Bruk vår [navnekalkulator](/compute-name-vowel-consonant/) for å beregne ditt uttrykkstall, sjelstallets og personlighetstallets — og forstå hvorfor akkurat ditt navn er akkurat deg."""

NAVN_NEW_CONTENT = """
<p>
  Har du noen gang lurt på hvorfor et navn føles riktig — eller galt — for en
  person? Numerologien gir et fascinerende svar: hvert navn bærer en numerisk
  vibrasjon som former personligheten og uttrykksmåten.
</p>

<h2>Uttrykkstallets grunnprinsipp</h2>
<p>
  I numerologien tilsvarer hver bokstav i alfabetet et tall fra 1 til 9.
  Summen av tallverdiene i ditt fulle navn — slik det ble gitt deg ved
  fødsel — kalles <strong>uttrykkstallets</strong> (eller navnetallets)
  vibrasjon.
</p>
<p>
  Dette tallet avslører din naturlige begavelse, din måte å uttrykke deg på
  i verden, og de egenskapene du ble gitt for å fullføre din livsoppgave.
</p>

<h2>Slik beregner du uttrykkstallets</h2>
<p>Bokstav-verdiene følger dette skjemaet:</p>
<table>
  <tbody>
    <tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr>
    <tr><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td><td>H</td><td>I</td></tr>
    <tr><td>J</td><td>K</td><td>L</td><td>M</td><td>N</td><td>O</td><td>P</td><td>Q</td><td>R</td></tr>
    <tr><td>S</td><td>T</td><td>U</td><td>V</td><td>W</td><td>X</td><td>Y</td><td>Z</td><td></td></tr>
  </tbody>
</table>
<p><strong>Eksempel:</strong> Navn = ANNA</p>
<ul>
  <li>A = 1, N = 5, N = 5, A = 1</li>
  <li>Sum: 1 + 5 + 5 + 1 = 12 → 1 + 2 = <strong>3</strong></li>
</ul>
<p>Anna har uttrykkstallets <strong>3</strong> — kreativitet, glede og kommunikasjon.</p>

<h2>Vokal- og konsonanttallene</h2>
<p>Numerologien skiller mellom vokalene og konsonantene i navnet ditt:</p>
<ul>
  <li><strong>Sjelstallets</strong> (vokaler): avslører din indre motivasjon og hjertelengsel.</li>
  <li><strong>Personlighetstallets</strong> (konsonanter): viser det første inntrykket du gir andre.</li>
</ul>
<p>
  Til sammen utgjør disse tre tallene — uttrykk, sjel og personlighet — et
  komplett bilde av din navnevibrasjon.
</p>

<h2>Hvorfor føles noen navn «riktige»?</h2>
<p>
  Åse Steinsland forklarer at vi instinktivt reagerer på navnevibrasjoner.
  Når et navn «klikker», er det fordi dets numeriske energi harmonerer med
  mottakerens eget tallmønster.
</p>
<p>
  Dette er grunnen til at mange mennesker som bytter navn — etter ekteskap,
  transisjon eller personlig vekst — opplever at det nye navnet faktisk
  endrer noe i dem. Det er ikke bare symbolikk. Det er et skifte i
  vibrasjonsmønster.
</p>

<h2>Utforsk ditt eget navn</h2>
<p>
  Bruk vår <a href="/compute-name-vowel-consonant/">navnekalkulator</a> for
  å beregne ditt uttrykkstall, sjelstallets og personlighetstallets — og
  forstå hvorfor akkurat ditt navn er akkurat deg.
</p>

<h2>Ofte stilte spørsmål</h2>
<p>
  <strong>Endrer navnet mitt seg hvis jeg bruker et kallenavn i hverdagen?</strong><br>
  Den klassiske beregningen bruker navnet slik det står i fødselsattesten,
  fordi det er den opprinnelige vibrasjonen. Kallenavn kan ha sin egen,
  separate vibrasjon som virker ved siden av den.
</p>
<p>
  <strong>Bør jeg bytte navn hvis uttrykkstallet ikke «passer» meg?</strong><br>
  Ikke nødvendigvis. De fleste bruker uttrykkstallet som et tolkningsverktøy,
  ikke som en grunn til å endre identitet. Snakk med Åse i en
  <a href="/guidance-support/">veiledningssamtale</a> hvis du vurderer det.
</p>

<p><em>Skrevet av Khabat Setaei.</em></p>
""".strip()


MASTER33_SLUG = "master-number-33"
MASTER33_OLD_CONTENT = """Mestertallet 33 er et av de mest sjeldne og kraftfulle tallene i numerologien. Det kalles ofte «den kosmiske læreren» — et tall som kombinerer den kreative kraften til 3 med dobbeltkraften av medfølelse og heling.

## Hva er et mestertall?

I numerologien er mestertallene 11, 22 og 33 tall som ikke reduseres til et enkelt siffer. De bærer en høyere vibrasjon og en større livsoppgave enn vanlige tall.

Tallet 33 oppstår i et kart når livstallets beregning gir summen 33 før den reduseres til 6. Det er viktig å skille mellom de som virkelig har 33 som mestertall, og de som har livstallets grunnvibrasjonen 6.

## Egenskapene til 33

Mennesker med 33 i kartet sitt har en medfødt evne til å helbrede, undervise og løfte andre. De kjenner en dyp kalling mot tjeneste og omsorg for menneskeheten.

**Styrker:**
- Emosjonell dybde og empati utover det vanlige
- En naturlig evne til å formidle komplekse sannheter på enkelt vis
- Sterk kreativ kraft kombinert med åndelig innsikt
- Evnen til å inspirere og løfte dem rundt seg

**Utfordringer:**
- Tendens til å ofre egne behov for andres skyld
- Perfeksjonisme og høye forventninger til seg selv
- Risiko for utbrenthet uten regelmessig hvile og selvpleie

## Åses veiledning for 33-energi

Åse Steinsland understreker at 33-energi er helligst når den er forankret i egenlæring. Du kan ikke gi fra en tom kilde. Den viktigste leksjonen for alle med 33 i kartet: din egen helbredelsesreise er selve fundamentet for din tjeneste til andre.

Praksisen er enkel — men ikke lett: led med eksempel, bevar dine grenser, og ta vare på ditt eget hjerte like omsorgsfullt som du tar vare på andres.

## Sjekk ditt eget kart

Vil du vite om du har 33 som mestertall? Bruk vår [kalkulator](/calculators/) for å beregne ditt livstall basert på fødselsdato."""

MASTER33_NEW_CONTENT = """
<p>
  Mestertallet 33 er et av de mest sjeldne og kraftfulle tallene i
  numerologien. Det kalles ofte «den kosmiske læreren» — et tall som
  kombinerer den kreative kraften til 3 med dobbeltkraften av medfølelse og
  heling.
</p>

<h2>Hva er et mestertall?</h2>
<p>
  I numerologien er mestertallene 11, 22 og 33 tall som ikke reduseres til
  et enkelt siffer. De bærer en høyere vibrasjon og en større livsoppgave
  enn vanlige tall.
</p>
<p>
  Tallet 33 oppstår i et kart når livstallets beregning gir summen 33 før
  den reduseres til 6. Det er viktig å skille mellom de som virkelig har 33
  som mestertall, og de som har livstallets grunnvibrasjon 6. Se
  <a href="/numbers/33/">Mestertall 33</a> for den kortfattede
  oversikten, eller <a href="/numbers/6/">Tall 6</a> for grunnvibrasjonen
  den bygger på.
</p>

<h2>Egenskapene til 33</h2>
<p>
  Mennesker med 33 i kartet sitt har en medfødt evne til å helbrede,
  undervise og løfte andre. De kjenner en dyp kalling mot tjeneste og
  omsorg for menneskeheten.
</p>
<p><strong>Styrker:</strong></p>
<ul>
  <li>Emosjonell dybde og empati utover det vanlige.</li>
  <li>En naturlig evne til å formidle komplekse sannheter på enkelt vis.</li>
  <li>Sterk kreativ kraft kombinert med åndelig innsikt.</li>
  <li>Evnen til å inspirere og løfte dem rundt seg.</li>
</ul>
<p><strong>Utfordringer:</strong></p>
<ul>
  <li>Tendens til å ofre egne behov for andres skyld.</li>
  <li>Perfeksjonisme og høye forventninger til seg selv.</li>
  <li>Risiko for utbrenthet uten regelmessig hvile og selvpleie.</li>
</ul>

<h2>Åses veiledning for 33-energi</h2>
<p>
  Åse Steinsland understreker at 33-energi er helligst når den er forankret
  i egenlæring. Du kan ikke gi fra en tom kilde. Den viktigste leksjonen for
  alle med 33 i kartet: din egen helbredelsesreise er selve fundamentet for
  din tjeneste til andre.
</p>
<p>
  Praksisen er enkel — men ikke lett: led med eksempel, bevar dine grenser,
  og ta vare på ditt eget hjerte like omsorgsfullt som du tar vare på andres.
</p>

<h2>Sjekk ditt eget kart</h2>
<p>
  Vil du vite om du har 33 som mestertall? Bruk vår
  <a href="/calculators/">kalkulator</a> for å beregne ditt livstall basert
  på fødselsdato.
</p>

<h2>Ofte stilte spørsmål</h2>
<p>
  <strong>Er 33 sjeldnere enn 11 og 22?</strong><br>
  Ja. 33 krever en spesifikk kombinasjon av fødselsdato-tall for å oppstå
  før reduksjon, og forekommer sjeldnere i beregninger enn 11 og 22.
</p>
<p>
  <strong>Hva om jeg egentlig bare har grunnvibrasjonen 6?</strong><br>
  De fleste med livstall 6 har ikke passert gjennom en faktisk sum på 33
  underveis i beregningen. Se <a href="/numbers/6/">Tall 6</a> for hva den
  vibrasjonen betyr på egen hånd, eller book en
  <a href="/guidance-support/">personlig gjennomgang</a> for å være sikker.
</p>

<p><em>Skrevet av Khabat Setaei.</em></p>
""".strip()


def apply_fixes(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.filter(slug=NAVN_SLUG).update(content=NAVN_NEW_CONTENT)
    Article.objects.filter(slug=MASTER33_SLUG).update(content=MASTER33_NEW_CONTENT)


def revert_fixes(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.filter(slug=NAVN_SLUG).update(content=NAVN_OLD_CONTENT)
    Article.objects.filter(slug=MASTER33_SLUG).update(content=MASTER33_OLD_CONTENT)


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0003_add_numerological_reflection_article"),
    ]

    operations = [
        migrations.RunPython(apply_fixes, revert_fixes),
    ]
